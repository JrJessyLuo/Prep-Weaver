"""Stage 2: aggregate the keyphrase-column retrieval into a table ranking.

Input  (results/):  question_keywords_top{N}_columns.json   (stage 1)
       (profiles/): dev_tables.json                          (schema text)
Output (results/):  question_ranked_tables_only_C.json

Scoring (the "only_C" ranking, purely column-similarity based):

    score(q, t) = max_k C_rel(k, t)

    C_rel(k, t) = the best column similarity between keyphrase k and any column
                  of table t among k's top-`top_col_k` retrieved columns,
                  min-max normalized into [0.5, 1].

This stage is embedding-free: all similarities were already computed in stage 1
and are only read back and aggregated here. Each ranked table carries the
evidence (matched keyphrase, matched column, similarity) that produced its
score, which stage 3 shows to the LLM and stage 5 uses for candidate selection.

Run:
    python -m table_discovery.table_rerank --dataset Beaver-Prep --kc-top-k 100
"""

from __future__ import annotations

import argparse
import json
import os
import re
import time
from typing import Any, Dict, List, Optional, Set

from tqdm import tqdm

from common import paths as P
from common.io_utils import read_json, write_json

# ============================================================

def minmax_normalize_to_half_one(
    value,
    min_value,
    max_value,
    default_value: float = 0.5,
    eps: float = 1e-8,
) -> float:
    """Min-max normalize into [0,1], then smooth to [0.5,1.0].
    If max == min, the signal has no discriminative power -> default_value.
    """
    if max_value - min_value < eps:
        return float(default_value)
    norm = (value - min_value) / (max_value - min_value + eps)
    norm = max(0.0, min(1.0, norm))
    return float(0.5 + 0.5 * norm)


def serialize_table_schema(table_id: str, table: Dict[str, Any]) -> str:
    """table_name + column names. Used as table_schema_text in the step3 LLM prompt."""
    table_name = table.get("table_name_original") or table.get("table_name") or table_id
    cols = table.get("column_names_original", [])
    col_texts = []
    for col in cols:
        if col is None:
            continue
        if isinstance(col, str):
            col_texts.append(col)
        elif isinstance(col, (list, tuple)) and len(col) > 0:
            col_texts.append(str(col[-1]))
        else:
            col_texts.append(str(col))
    return " ".join(str(x) for x in ([table_name] + col_texts) if x is not None)


def get_keyword_candidate_tables(
    retrieved_columns: List[Dict[str, Any]],
    top_col_k: int = 100,
):
    """For one keyphrase, dedupe its retrieved columns by table_id, keeping the
    highest-similarity column per table as that table's evidence.
    """
    table_to_best_col = {}
    for col in retrieved_columns[:top_col_k]:
        table_id = col["table_id"]
        sim = float(col["similarity"])
        if (
            table_id not in table_to_best_col
            or sim > float(table_to_best_col[table_id]["similarity"])
        ):
            table_to_best_col[table_id] = col
    return table_to_best_col


def normalize_text(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", str(text).lower()).strip()


def table_name_from_id(table_id: str, table: Optional[Dict[str, Any]] = None) -> str:
    if table:
        return str(table.get("table_name_original") or table.get("table_name") or table_id.split("#sep#")[-1])
    return str(table_id).split("#sep#")[-1]


def aggregate_table_score(
    table_id: str,
    evidences: List[Dict[str, Any]],
    keywords: List[str],
    table_name: str,
) -> Dict[str, Any]:
    """only_C aggregation: score(q, t) = max over keyphrases of C_rel(k, t).

    The auxiliary statistics (top-2, keyphrase coverage) are reported alongside
    the score because stage 3 and stage 5 read them, but they do not enter the
    ranking.
    """
    best = max(evidences, key=lambda x: x["score_only_c_keyword"])
    rels = [float(e["score_only_c_keyword"]) for e in evidences]
    max_rel = max(rels)
    avg_rel = sum(rels) / len(rels)
    top2_rel = sum(sorted(rels, reverse=True)[:2]) / min(2, len(rels))
    support_frac = len({e["keyword"] for e in evidences}) / max(1, len(keywords))

    return {
        "score": float(max_rel),
        "best_keyword": best["keyword"],
        "best_column_similarity_raw": float(best["column_similarity_raw"]),
        "best_column_similarity_rel": float(best["column_similarity_rel"]),
        "num_supporting_keywords": len(evidences),
        "support_frac": float(support_frac),
        "avg_keyword_score": float(avg_rel),
        "top2_keyword_score": float(top2_rel),
        "scoring_method": "only_C: score(q,t) = max_k [C_rel(keyphrase, column)]",
    }


# ============================================================
# only_C ranking
# ============================================================

def rank_tables_for_questions(
    question_topk_columns_path: str,
    table_schema_path: str,
    out_dir: str,
    top_col_k: int = 100,
    top_table_k: int = 50,
):
    os.makedirs(out_dir, exist_ok=True)

    if not os.path.exists(question_topk_columns_path):
        raise FileNotFoundError(
            f"Missing stage 1 output: {question_topk_columns_path}\n"
            f"Run column_retrieval.py first with the same --dataset and --top-k."
        )
    if not os.path.exists(table_schema_path):
        raise FileNotFoundError(f"Missing table schema file: {table_schema_path}")

    # Step1 output already contains BOTH the keyphrases and their retrieved columns.
    question_topk_columns = read_json(question_topk_columns_path)
    tables = read_json(table_schema_path)

    # Pre-serialize schema text once (string only, no embedding).
    table_schema_texts = {
        tid: serialize_table_schema(tid, t)
        for tid, t in tables.items()
    }

    results_only_c = {}

    for qid, rec in tqdm(question_topk_columns.items(), desc="Stage2 only_C ranking"):
        t0 = time.perf_counter()

        question = rec.get("question", "")
        keywords = rec.get("keywords", [])
        keyword_column_retrieval = rec.get("keyword_column_retrieval", {})

        table_evidence = {}      # table_id -> [evidence per keyphrase]
        candidate_tables_all = set()

        for keyword in keywords:
            retrieved_columns = keyword_column_retrieval.get(keyword, [])
            top_retrieved_columns = retrieved_columns[:top_col_k]
            if len(top_retrieved_columns) == 0:
                continue

            col_sims = [float(c.get("similarity", 0.0)) for c in top_retrieved_columns]
            min_col_sim, max_col_sim = min(col_sims), max(col_sims)

            table_to_best_col = get_keyword_candidate_tables(
                retrieved_columns,
                top_col_k=top_col_k,
            )

            for table_id, best_col in table_to_best_col.items():
                candidate_tables_all.add(table_id)
                raw_column_sim = float(best_col.get("similarity", 0.0))
                C_rel = minmax_normalize_to_half_one(
                    raw_column_sim,
                    min_col_sim,
                    max_col_sim,
                    0.5,
                )

                table_evidence.setdefault(table_id, []).append({
                    "keyword": keyword,
                    "column_similarity_raw": raw_column_sim,
                    "column_similarity_rel": C_rel,
                    "score_only_c_keyword": float(C_rel),
                    "best_column_for_keyword": {
                        "rank": best_col.get("rank"),
                        "similarity": raw_column_sim,
                        "column_id": best_col.get("column_id"),
                        "table_id": best_col.get("table_id"),
                        "table_name": best_col.get("table_name"),
                        "column_name": best_col.get("column_name"),
                        "embedding_text": best_col.get("embedding_text"),
                    },
                })

        # aggregate the per-keyphrase evidence of each table into one score
        table_scores = {}
        for table_id, evidences in table_evidence.items():
            table_scores[table_id] = aggregate_table_score(
                table_id=table_id,
                evidences=evidences,
                keywords=keywords,
                table_name=table_name_from_id(table_id, tables.get(table_id, {})),
            )

        ranked = sorted(
            table_scores.items(),
            key=lambda x: x[1]["score"],
            reverse=True,
        )

        top_tables = []
        for rank, (table_id, si) in enumerate(ranked[:top_table_k], start=1):
            evidence = sorted(
                table_evidence[table_id],
                key=lambda x: x["score_only_c_keyword"],
                reverse=True,
            )
            top_tables.append({
                "rank": rank,
                "table_id": table_id,
                "score": float(si["score"]),
                "best_keyword": si["best_keyword"],
                "best_column_similarity_raw": si["best_column_similarity_raw"],
                "best_column_similarity_rel": si["best_column_similarity_rel"],
                "num_supporting_keywords": int(si["num_supporting_keywords"]),
                "support_frac": float(si.get("support_frac", 0.0)),
                "avg_keyword_score": float(si.get("avg_keyword_score", 0.0)),
                "top2_keyword_score": float(si.get("top2_keyword_score", 0.0)),
                "table_schema_text": table_schema_texts.get(table_id, ""),
                "evidence": evidence,
            })

        step2_time = time.perf_counter() - t0

        results_only_c[qid] = {
            "question_id": rec.get("question_id", qid),
            "question": question,
            "keywords": keywords,
            "top_col_k": top_col_k,
            "top_table_k": top_table_k,
            "scoring_method": "only_C: score(q,t) = max_k [C_rel(keyphrase, column)]",
            "num_candidate_tables_from_columns": len(candidate_tables_all),
            "num_final_ranked_tables": len(table_scores),
            "step2_time_sec": step2_time,
            "ranked_tables": top_tables,
        }

    out_path = f"{out_dir}/question_ranked_tables_only_C.json"
    write_json(results_only_c, out_path)
    print(f"Saved: {out_path}")
    return results_only_c


# ============================================================
# Entry point
# ============================================================

def parse_args():
    parser = argparse.ArgumentParser(
        description="Stage 2: aggregate keyphrase-column retrieval into a table ranking.")
    P.add_arguments(parser)
    parser.add_argument("--kc-top-k", type=int, default=100,
                        help="The N in question_keywords_top{N}_columns.json, i.e. "
                             "the --top-k used in stage 1.")
    parser.add_argument("--top-col-k", type=int, default=100,
                        help="Retrieved columns per keyphrase used for aggregation.")
    parser.add_argument("--top-table-k", type=int, default=50,
                        help="Candidate tables kept per question.")
    return parser.parse_args()


if __name__ == "__main__":
    a = parse_args()
    paths = P.from_args(a)
    rank_tables_for_questions(
        question_topk_columns_path=str(paths.question_topk_columns(a.kc_top_k)),
        table_schema_path=str(paths.tables),
        out_dir=str(paths.out_dir),
        top_col_k=a.top_col_k,
        top_table_k=a.top_table_k,
    )
