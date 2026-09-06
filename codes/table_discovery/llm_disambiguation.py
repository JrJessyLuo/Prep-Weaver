"""Stage 3: LLM distractor pruning behind an ambiguity gate.

Input  (results/):  question_keywords_top{N}_columns.json   (stage 1, gate signal)
                    question_ranked_tables_only_C.json      (stage 2, candidate pool)
Output (results/):  question_ranked_tables_gated.json       (the mainline ranking)
                    question_ranked_tables_llm.json         (LLM pruning on every question)
                    gating_decisions.json                   (gate audit trail)
                    llm_records.json                        (raw LLM outputs + token usage)

Calling the LLM on every question is wasteful: most questions have an
unambiguous column match and the LLM has nothing to remove. The gate decides
which questions are worth the call, using a similarity-margin ambiguity signal
computed from stage 1 alone:

    A(k) = number of distinct tables among keyphrase k's top-W retrieved columns
           whose similarity is within `delta` of that keyphrase's best match

A question is routed to the LLM when ambiguity is concentrated in one keyphrase
(max_k A(k) >= GATE_T) or, with the aggregate gate on, when it is spread across
several keyphrases. Routed questions take the LLM-pruned ranking; the rest keep
the stage 2 ranking unchanged.

Reruns are cheap: per-question LLM outputs are cached in llm_records.json, and
an existing question_ranked_tables_llm.json is reused instead of re-calling the
LLM, so the gate can be re-tuned for free.

Run:
    python -m table_discovery.llm_disambiguation --dataset Beaver-Prep
"""

from __future__ import annotations

import argparse
import json
import os
import re
import time
from typing import Any, Dict, List, Optional, Tuple

from tqdm import tqdm

from common import paths as P
from common.io_utils import read_json, write_json, write_json_atomic
from common.llm_client import llm_generate_setup

DEFAULT_LLM_MODEL = "gpt-5.2"

# ============================================================
# Gating hyperparameters
# ============================================================
# Selected by grid search on Beaver-Prep for the largest complete-recall gain.
#
#   AMBIGUITY_W     per keyphrase, only inspect its top-W retrieved columns
#   AMBIGUITY_DELTA a column is a near-tie if sim >= top1_sim - delta
#   GATE_T          route if max_k A(k) >= GATE_T (concentrated ambiguity)
#   USE_AGGREGATE_GATE
#                   also route when ambiguity is distributed: at least two
#                   keyphrases with A(k) >= max(3, GATE_T-2), or
#                   sum_k max(0, A(k)-1) >= GATE_T + 4
#
# A cheaper, slightly weaker setting from the same grid: W=10, delta=0.02, T=5.
# The earlier conservative gate was: W=15, delta=0.03, T=6, aggregate off.
AMBIGUITY_W = 10
AMBIGUITY_DELTA = 0.05
GATE_T = 8
USE_AGGREGATE_GATE = True

def extract_json_from_llm_output(output: str):
    output = (output or "").strip()
    output = re.sub(r"^```json\s*", "", output)
    output = re.sub(r"^```\s*", "", output)
    output = re.sub(r"\s*```$", "", output)
    output = output.strip()
    try:
        return json.loads(output)
    except json.JSONDecodeError:
        m = re.search(r"\{.*\}", output, flags=re.DOTALL)
        if m:
            return json.loads(m.group(0))
    raise ValueError(f"Cannot parse JSON from LLM output:\n{output}")


# ============================================================
# (a) Prune prompt + parsing
# ============================================================

PRUNE_PROMPT = """You are removing DISTRACTOR tables from a candidate list for a question. Keep everything else — most candidates should be kept.

Question: {question}

The question was decomposed into these KEY PHRASES (each is one piece of information the question needs):
{keyphrases}

HOW CANDIDATES WERE RETRIEVED: each table was retrieved by matching a key phrase against table COLUMN NAMES using embedding similarity. A table can therefore rank high purely because one of its column NAMES is textually/semantically similar to a key phrase (we show the match and its similarity score), even when the table's actual subject is unrelated to the question.

Each candidate below shows: TABLE_ID | match: 'key phrase' ~ COLUMN (sim=score) | columns.
{table_block}

A DISTRACTOR is a table that earned a high column-name match score but does not actually belong to this question. Remove a table only when ALL of the following hold:
  1. it was pulled in mainly by a strong column-NAME similarity to a key phrase (a generic/shared column name, not a column that uniquely defines this table's own subject);
  2. considering the full question intent, the table's subject — what each row represents — is not actually relevant; AND
  3. it is an OUTLIER relative to the rest of the candidates: the genuinely relevant tables for a question tend to form a coherent, connected group (same domain, joinable, pointing at the same entities across the different key phrases), whereas this table stands alone and has no real relationship to the tables retrieved by the OTHER key phrases.

Do NOT remove a table for any other reason:
  - Keep a table that fits the coherent group of relevant tables, could supply a needed attribute, or could serve as a join/bridge between relevant tables.
  - If two tables have very similar schemas and both relate to the question (e.g. different source systems, or current vs. historical), keep both — do not try to pick the "right" one.
  - When in doubt, KEEP.

Output JSON only: {{"remove": [TABLE_ID, ...]}}"""


def _matched_column_and_sim(item):
    """The column + similarity that caused this table to be retrieved (from evidence)."""
    ev = item.get("evidence") or []
    if ev:
        bc = ev[0].get("best_column_for_keyword", {})
        return bc.get("column_name", "?"), bc.get("similarity", item.get("best_column_similarity_raw"))
    return "?", item.get("best_column_similarity_raw")


def build_prune_prompt(question: str, keyphrases: List[str],
                       ranked_tables: List[Dict[str, Any]], max_info_chars: int = 400):
    lines = []
    for item in ranked_tables:
        tid = item["table_id"]
        kw = item.get("best_keyword", "?")
        col, sim = _matched_column_and_sim(item)
        sim_s = f"{sim:.2f}" if isinstance(sim, (int, float)) else "?"
        info = (item.get("table_schema_text") or "")[:max_info_chars]
        lines.append(f"- {tid} | match: '{kw}' ~ {col} (sim={sim_s}) | columns: {info}")
    return PRUNE_PROMPT.format(
        question=question,
        keyphrases="\n".join(f"  - {k}" for k in keyphrases),
        table_block="\n".join(lines),
    )


def parse_remove(llm_output: str, candidate_ids):
    cand = set(candidate_ids)
    try:
        d = extract_json_from_llm_output(llm_output)
        remove = set(d.get("remove", [])) & cand
        # safety: if model removed almost everything, treat as no-op
        if len(remove) >= len(cand) - 2:
            return set()
        return remove
    except Exception:
        return set()


def prune_and_topk(ranked_tables: List[Dict[str, Any]], remove_set, k: int):
    """Keep only_C order; move removed tables to bottom; cut top-k."""
    survivors = [t for t in ranked_tables if t["table_id"] not in remove_set]
    pruned = [t for t in ranked_tables if t["table_id"] in remove_set]
    out = []
    for rank, item in enumerate((survivors + pruned)[:k], start=1):
        rec = dict(item)
        rec["rank"] = rank
        rec["llm_pruned"] = item["table_id"] in remove_set
        out.append(rec)
    return out


def generate_llm_ranking_if_needed(
    ranking: Dict[str, Any],
    paths: Dict[str, str],
    llm_model: str = DEFAULT_LLM_MODEL,
    force_regenerate: bool = False,
):
    """Prune distractors with the LLM for every question in the ranking.

    Per-question raw outputs are cached in llm_records.json; only questions
    missing from that cache trigger an API call.
    """
    records_path = paths["llm_records_path"]
    records = read_json(records_path) if (os.path.exists(records_path) and not force_regenerate) else {}

    for qid, rec in tqdm(ranking.items(), desc="Stage3 LLM pruning"):
        question = rec["question"]
        cand = rec["ranked_tables"]
        cand_ids = [c["table_id"] for c in cand]

        if not force_regenerate and qid in records:
            output = records[qid].get("raw_output", "")
            in_tok = records[qid].get("input_tokens", 0)
            out_tok = records[qid].get("output_tokens", 0)
            latency = records[qid].get("latency_sec", 0.0)
        else:
            prompt = build_prune_prompt(question, rec.get("keywords", []), cand)
            t0 = time.perf_counter()
            resp = llm_generate_setup(prompt, model=llm_model, json_format=True)
            latency = time.perf_counter() - t0
            output = resp.get("text", "")
            in_tok = int(resp.get("input_tokens", 0) or 0)
            out_tok = int(resp.get("output_tokens", 0) or 0)

        remove = parse_remove(output, cand_ids)
        records[qid] = {
            "raw_output": output,
            "input_tokens": in_tok,
            "output_tokens": out_tok,
            "total_tokens": in_tok + out_tok,
            "latency_sec": latency,
            "remove": sorted(remove),
            "num_removed": len(remove),
            "num_candidates": len(cand_ids),
        }
        write_json_atomic(records, records_path)

    KPOOL = max((len(r["ranked_tables"]) for r in ranking.values()), default=50)
    llm_full = {}
    for qid, rec in ranking.items():
        remove = set(records[qid]["remove"])
        llm_full[qid] = {
            "question_id": rec.get("question_id", qid),
            "question": rec["question"],
            "num_llm_removed": len(remove),
            "scoring_method": "only_C + LLM disambiguation (prune->demote)",
            "ranked_tables": prune_and_topk(rec["ranked_tables"], remove, KPOOL),
        }
    write_json(llm_full, paths["llm_rank_path"] )
    return llm_full


# ============================================================
# (b) New gating signal
# ============================================================

def _get_similarity(e: Dict[str, Any]) -> Optional[float]:
    """Robustly read similarity from several possible field names."""
    for key in ("similarity", "score", "sim", "column_similarity", "best_column_similarity_raw"):
        v = e.get(key)
        if isinstance(v, (int, float)):
            return float(v)
        if isinstance(v, str):
            try:
                return float(v)
            except ValueError:
                pass
    return None


def compute_ambiguity_details(
    keyphrases,
    kw_cols,
    W=None,
    delta=None,
    gate_t=None,
    use_aggregate_gate=None,
):
    """Compute ambiguity details for the gate.

    Per-keyphrase ambiguity:
      A(k) = #distinct tables in top-W whose similarity is within delta of
             the top-1 similarity.

    Base route:
      max_k A(k) >= gate_t

    Aggregate/distributed route:
      If enabled, also route when ambiguity is spread across several keyphrases:
        - at least two keyphrases have A(k) >= max(3, gate_t-2); OR
        - sum_k max(0, A(k)-1) >= gate_t + 4

    This avoids dataset-specific generic-token rules while capturing the case
    where no single keyphrase is extremely ambiguous, but several information
    needs are moderately ambiguous.
    """
    # Read the module-level defaults at call time, so a CLI override applies.
    W = AMBIGUITY_W if W is None else W
    delta = AMBIGUITY_DELTA if delta is None else delta
    gate_t = GATE_T if gate_t is None else gate_t
    use_aggregate_gate = USE_AGGREGATE_GATE if use_aggregate_gate is None else use_aggregate_gate

    max_amb = 0
    max_kw = None
    per_keyphrase = {}
    ambiguity_counts = []

    for kw in keyphrases:
        L = kw_cols.get(kw) or []
        L = L[:W]
        if not L:
            per_keyphrase[kw] = {
                "ambiguity": 0,
                "top1_similarity": None,
                "threshold": None,
                "near_tie_tables": [],
            }
            ambiguity_counts.append(0)
            continue

        sims = [_get_similarity(e) for e in L]
        valid_sims = [s for s in sims if s is not None]
        if not valid_sims:
            per_keyphrase[kw] = {
                "ambiguity": 0,
                "top1_similarity": None,
                "threshold": None,
                "near_tie_tables": [],
            }
            ambiguity_counts.append(0)
            continue

        # Usually L[0] is top-1. max() makes the function safer if the list is not sorted.
        top1_sim = max(valid_sims)
        threshold = top1_sim - delta

        near_tie_tables = []
        seen = set()
        for e in L:
            sim = _get_similarity(e)
            tid = e.get("table_id")
            if tid is None or sim is None or sim < threshold:
                continue
            if tid in seen:
                continue
            seen.add(tid)
            near_tie_tables.append({
                "table_id": tid,
                "column_name": e.get("column_name"),
                "similarity": sim,
            })

        amb = len(seen)
        ambiguity_counts.append(amb)
        per_keyphrase[kw] = {
            "ambiguity": amb,
            "top1_similarity": top1_sim,
            "threshold": threshold,
            "near_tie_tables": near_tie_tables,
        }

        if amb > max_amb:
            max_amb = amb
            max_kw = kw

    sum_excess_ambiguity = sum(max(0, c - 1) for c in ambiguity_counts)
    mean_ambiguity = (
        sum(ambiguity_counts) / len(ambiguity_counts)
        if ambiguity_counts else 0.0
    )

    # Base concentrated-ambiguity gate.
    base_route = max_amb >= gate_t

    # Aggregate distributed-ambiguity gate.
    mid_t = max(3, gate_t - 2)
    num_mid_ambiguous_keyphrases = sum(1 for c in ambiguity_counts if c >= mid_t)
    aggregate_route = (
        use_aggregate_gate
        and (
            num_mid_ambiguous_keyphrases >= 2
            or sum_excess_ambiguity >= gate_t + 4
        )
    )

    routed = bool(base_route or aggregate_route)

    if base_route:
        route_reason = "max_ambiguity"
    elif aggregate_route and num_mid_ambiguous_keyphrases >= 2:
        route_reason = "distributed_keyphrases"
    elif aggregate_route:
        route_reason = "sum_excess_ambiguity"
    else:
        route_reason = "not_routed"

    return {
        "ambiguity": max_amb,  # kept for backward compatibility
        "max_ambiguity": max_amb,
        "max_keyphrase": max_kw,
        "sum_excess_ambiguity": sum_excess_ambiguity,
        "mean_ambiguity": mean_ambiguity,
        "ambiguity_counts": ambiguity_counts,
        "mid_threshold": mid_t,
        "num_mid_ambiguous_keyphrases": num_mid_ambiguous_keyphrases,
        "base_route": bool(base_route),
        "aggregate_route": bool(aggregate_route),
        "route_reason": route_reason,
        "routed_to_llm": routed,
        "per_keyphrase": per_keyphrase,
    }

def build_gate_decisions(kc_path):
    """{qid: detailed gate decision} from the step1 unified file."""
    qcols = read_json(kc_path)
    decisions = {}
    for qid, rec in qcols.items():
        kw_cols = rec.get("keyword_column_retrieval", {})
        keyphrases = rec.get("keywords", list(kw_cols.keys()))
        d = compute_ambiguity_details(keyphrases, kw_cols)
        decisions[qid] = d
    return decisions


# ============================================================
# Entry point
# ============================================================

def make_paths(paths: "P.Paths", kc_top_k: int = 100) -> Dict[str, str]:
    """Collect the input/output file names this stage reads and writes."""
    return {
        "out_dir": str(paths.out_dir),
        "kc_path": str(paths.question_topk_columns(kc_top_k)),
        "only_c_topk1": str(paths.out("question_ranked_tables_only_C.json")),
        "llm_rank_path": str(paths.out("question_ranked_tables_llm.json")),
        "gated_path": str(paths.out("question_ranked_tables_gated.json")),
        "gate_dbg_path": str(paths.out("gating_decisions.json")),
        "llm_records_path": str(paths.out("llm_records.json")),
    }


def run_disambiguation(
    paths: "P.Paths",
    kc_top_k: int = 100,
    llm_model: str = DEFAULT_LLM_MODEL,
    reuse_existing_llm: bool = True,
    force_regenerate_records: bool = False,
):
    """Run stage 3: recompute the gate, and prune the routed questions."""
    fp = make_paths(paths, kc_top_k=kc_top_k)
    ranking = read_json(fp["only_c_topk1"])  # stage 2 candidate pool

    # ---- LLM-pruned ranking: reuse the cached file only when it is COMPLETE ----
    # A partial file is the normal state after a --limit smoke test. Reusing it
    # on a full run would silently drop every routed question it does not cover
    # back to only_C, quietly turning off this stage for most of the dataset.
    # Regenerating is cheap: llm_records.json caches the per-question outputs,
    # so only the questions that were never processed cost an API call.
    cached = (read_json(fp["llm_rank_path"])
              if os.path.exists(fp["llm_rank_path"]) else {})
    covers_all = cached and set(ranking).issubset(cached)

    if reuse_existing_llm and covers_all:
        print(f"Reusing existing LLM ranking: {fp['llm_rank_path']}")
        llm_full = cached
    else:
        if cached and reuse_existing_llm:
            print(f"Existing LLM ranking covers {len(cached)}/{len(ranking)} questions; "
                  f"regenerating the missing ones (cached outputs are reused).")
        print(f"Generating LLM ranking: {fp['llm_rank_path']}")
        llm_full = generate_llm_ranking_if_needed(
            ranking=ranking,
            paths=fp,
            llm_model=llm_model,
            force_regenerate=force_regenerate_records,
        )

    # ---- ambiguity gate ----
    decisions = build_gate_decisions(fp["kc_path"])
    ranking_qids = set(ranking.keys())
    routed_qids = {qid for qid, d in decisions.items() if d.get("routed_to_llm")}
    n = len(ranking)
    n_routed = len(routed_qids & ranking_qids)
    print(
        f"Gate: W={AMBIGUITY_W}, delta={AMBIGUITY_DELTA}, T>={GATE_T}, "
        f"aggregate={USE_AGGREGATE_GATE}: "
        f"route {n_routed}/{n} questions to the LLM ({n_routed / max(n, 1) * 100:.1f}%)"
    )
    write_json(decisions, fp["gate_dbg_path"])
    print(f"Saved gate decisions: {fp['gate_dbg_path']}")

    # ---- gated ranking: routed questions take the LLM ranking, the rest only_C ----
    gated_full = {}
    missing_llm_qids = []

    for qid, rec in ranking.items():
        route = qid in routed_qids

        if route and qid in llm_full:
            src_tables = llm_full[qid]["ranked_tables"]
            route_used = True
        else:
            # Not routed, or the cached LLM file is incomplete: keep only_C.
            if route:
                missing_llm_qids.append(qid)
            src_tables = rec["ranked_tables"]
            route_used = False

        d = decisions.get(qid, {})
        gated_full[qid] = {
            "question_id": rec.get("question_id", qid),
            "question": rec["question"],
            "gating": {
                "method": "near_tie_similarity_margin_with_aggregate",
                "W": AMBIGUITY_W,
                "delta": AMBIGUITY_DELTA,
                "threshold": GATE_T,
                "use_aggregate_gate": USE_AGGREGATE_GATE,
                "max_ambiguity": d.get("max_ambiguity", d.get("ambiguity", 0)),
                "max_keyphrase": d.get("max_keyphrase"),
                "sum_excess_ambiguity": d.get("sum_excess_ambiguity"),
                "mean_ambiguity": d.get("mean_ambiguity"),
                "ambiguity_counts": d.get("ambiguity_counts"),
                "mid_threshold": d.get("mid_threshold"),
                "num_mid_ambiguous_keyphrases": d.get("num_mid_ambiguous_keyphrases"),
                "base_route": d.get("base_route"),
                "aggregate_route": d.get("aggregate_route"),
                "route_reason": d.get("route_reason"),
                "routed_to_llm": bool(route_used),
            },
            "ranked_tables": src_tables,
        }

    write_json(gated_full, fp["gated_path"])
    print(f"Saved gated ranking: {fp['gated_path']}")

    if missing_llm_qids:
        print(
            f"Warning: {len(missing_llm_qids)} routed questions were missing from "
            f"{fp['llm_rank_path']} and fell back to only_C. "
            f"Examples: {missing_llm_qids[:5]}"
        )

    return decisions, gated_full


def parse_args():
    parser = argparse.ArgumentParser(
        description="Stage 3: LLM distractor pruning behind an ambiguity gate.")
    P.add_arguments(parser)
    parser.add_argument("--kc-top-k", type=int, default=100,
                        help="The N in question_keywords_top{N}_columns.json (stage 1 --top-k).")
    parser.add_argument("--llm-model", type=str, default=DEFAULT_LLM_MODEL,
                        help="LLM used for distractor pruning.")
    parser.add_argument("--regenerate-llm", action="store_true",
                        help="Rebuild question_ranked_tables_llm.json instead of "
                             "reusing an existing one. Cached per-question outputs "
                             "in llm_records.json are still reused.")
    parser.add_argument("--force-regenerate-records", action="store_true",
                        help="Also discard the cached per-question LLM outputs and "
                             "call the LLM again for every question.")

    # Gate hyperparameters, overridable without editing the file.
    parser.add_argument("--ambiguity-w", type=int, default=AMBIGUITY_W)
    parser.add_argument("--ambiguity-delta", type=float, default=AMBIGUITY_DELTA)
    parser.add_argument("--gate-t", type=int, default=GATE_T)
    parser.add_argument("--no-aggregate-gate", action="store_true")
    return parser.parse_args()


if __name__ == "__main__":
    a = parse_args()

    AMBIGUITY_W = a.ambiguity_w
    AMBIGUITY_DELTA = a.ambiguity_delta
    GATE_T = a.gate_t
    USE_AGGREGATE_GATE = not a.no_aggregate_gate

    run_disambiguation(
        P.from_args(a),
        kc_top_k=a.kc_top_k,
        llm_model=a.llm_model,
        reuse_existing_llm=not a.regenerate_llm,
        force_regenerate_records=a.force_regenerate_records,
    )
