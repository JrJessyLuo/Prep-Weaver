"""Online: select the tables a question needs, from offline table metadata.

Input  : datasets/<Dataset>/benchmark.jsonl              (questions)
         results/table_discovery/metadata/<Dataset>/table_metadata.jsonl
                                                          (meta_inferrence.py)
         Beaver only, as the candidate pool:
           results/table_discovery/offline_online/<Dataset>/exp_g_domain_10.json
           (falling back to each task's `retrieved_table`)
Output : results/table_discovery/selection/<Dataset>/table_selection.jsonl
         one record per task:
           {task_id, question, candidate_tables, selected_tables,
            subquestions, hallucinated_tables, usage}

Candidate pool
--------------
Synth-Bird / Synth-Spider ship a per-task candidate pool in `input_table`, so
the whole pool goes into the prompt. Beaver's collection is a 96-table
warehouse, far too large for one prompt, so the pool is the top-k tables from
the retrieval stages of this module (exp_g_domain_10.json).

Recovered headers, not raw ones
-------------------------------
Candidates are described by the RECOVERED schema from meta_inferrence.py, never
the raw header row, because a raw header is often not a header. `--on-missing`
controls what happens to a table with no metadata: error (default), fall back to
its raw headers, or drop it. A fallback is always recorded in
`fell_back_to_original`, so a run is never quietly half-recovered.

Run:
    python -m table_discovery.table_selection --dataset Beaver-Prep
    python -m table_discovery.table_selection --dataset Synth-Bird --limit 5
"""

from __future__ import annotations

import argparse
import json
import re
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

import pandas as pd
from tqdm import tqdm

from common import dataset as DS
from common import paths as P
from common.io_utils import append_jsonl, load_jsonl_by_key
from common.llm_client import llm_generate_setup
from .meta_inferrence import default_metadata_path, load_table_metadata

DEFAULT_MODEL = "gpt-5-2025-08-07"
MAX_COLUMNS_PER_TABLE = 40
MAX_COLUMN_NAME_CHARS = 120

# Upper bound on how many tables the model may select. These are the datasets'
# own join arities: Synth-* questions join a handful of tables, while Beaver
# questions routinely need bridge tables that carry no question semantics.
MAX_TABLES = {"Synth-Bird": 4, "Synth-Spider": 4, "Beaver-Prep": 7}


PROMPT = """You are performing schema linking for a data-preparation benchmark.

Given a user question and a set of candidate input table files, identify the minimal set of table files needed to answer the question. The number of selected tables may range from 2 to {max_tables}.

First select the relevant tables based on the full question. Then, for each selected table, describe the part of the question it supports as one or more subquestions. If a meaningful subquestion cannot be formed, provide the corresponding question keywords instead.

Your tasks:
1. Select the relevant table files based on the full question.
2. For each selected table, generate the subquestions/keywords that can be supported by that table.
3. Ensure that the selected tables collectively preserve the important semantics of the question.

Question:
{question}

Candidate table files:
{tables_text}

Return only valid JSON:
{{
"relevant_table_files": ["..."],
"table_matches": [
{{
"table_file": "...",
"subquestions_or_keywords": ["..."]
}}
]
}}
"""

# Beaver alone gets join evidence and few-shots. Its tables come in near-duplicate
# families (FAC_* vs FCLT_*, SIS_* vs COURSE_CATALOG_*) that are not
# interchangeable, and its questions often need a bridge table that supports no
# part of the question by itself — neither is inferable from headers alone.
BEAVER_PROMPT = """You are performing schema linking for the Beaver data-preparation benchmark.

Given a user question, a set of candidate table files with recovered column headers, and predicted joinable table-file pairs, identify the minimal set of table files needed to answer the question. The number of selected tables may range from 2 to {max_tables}.

Use the predicted joinable pairs as structural evidence:
- Select tables that jointly cover the full question semantics.
- Prefer selected table sets that can be connected through the predicted joinable pairs.
- Do not select a table only because it is joinable; it must support part of the question or act as a necessary bridge.
- If two semantic tables are both relevant but are not directly joinable, include a bridge table when it is needed to connect them and it contributes the join path.
- Treat file_name as table identity. Near-duplicate families such as FAC_* vs FCLT_*, SIS_* vs COURSE_CATALOG_* vs SUBJECT_*, TIP_* vs LIBRARY_* are not interchangeable by default.

Few-shot examples:

Example 1: Directly joinable relevant tables
Question:
For each building, list the building name and the number of rooms in that building.

Candidate table files:
1. file_name: BUILDINGS.pkl
   columns: [BUILDING_KEY, BUILDING_NAME, BUILDING_NUMBER]

2. file_name: ROOMS.pkl
   columns: [ROOM_KEY, BUILDING_KEY, ROOM_NUMBER]

3. file_name: EMPLOYEES.pkl
   columns: [EMPLOYEE_KEY, EMPLOYEE_NAME, DEPARTMENT_KEY]

Predicted joinable table-file pairs:
- BUILDINGS.pkl <-> ROOMS.pkl
- EMPLOYEES.pkl <-> DEPARTMENTS.pkl

Output:
{{
"relevant_table_files": ["BUILDINGS.pkl", "ROOMS.pkl"],
"table_matches": [
{{"table_file": "BUILDINGS.pkl", "subquestions_or_keywords": ["building name", "join to rooms by BUILDING_KEY"]}},
{{"table_file": "ROOMS.pkl", "subquestions_or_keywords": ["count rooms per building", "BUILDING_KEY connects to BUILDINGS.pkl"]}}
]
}}

Example 2: Relevant tables require a bridge table
Question:
For each instructor, list the titles of library reserve materials assigned to their courses.

Candidate table files:
1. file_name: LIBRARY_COURSE_INSTRUCTOR.pkl
   columns: [LIBRARY_COURSE_INSTRUCTOR_KEY, INSTRUCTOR_NAME, COURSE_NAME]

2. file_name: LIBRARY_RESERVE_CATALOG.pkl
   columns: [LIBRARY_RESERVE_CATALOG_KEY, CATALOG_TITLE, CATALOG_ISBN]

3. file_name: LIBRARY_RESERVE_MATRL_DETAIL.pkl
   columns: [LIBRARY_COURSE_INSTRUCTOR_KEY, LIBRARY_RESERVE_CATALOG_KEY, TERM_CODE]

4. file_name: TIP_MATERIAL.pkl
   columns: [TIP_MATERIAL_KEY, TITLE, ISBN]

Predicted joinable table-file pairs:
- LIBRARY_COURSE_INSTRUCTOR.pkl <-> LIBRARY_RESERVE_MATRL_DETAIL.pkl
- LIBRARY_RESERVE_MATRL_DETAIL.pkl <-> LIBRARY_RESERVE_CATALOG.pkl
- TIP_MATERIAL.pkl <-> TIP_DETAIL.pkl

Output:
{{
"relevant_table_files": ["LIBRARY_COURSE_INSTRUCTOR.pkl", "LIBRARY_RESERVE_MATRL_DETAIL.pkl", "LIBRARY_RESERVE_CATALOG.pkl"],
"table_matches": [
{{"table_file": "LIBRARY_COURSE_INSTRUCTOR.pkl", "subquestions_or_keywords": ["instructor name", "course identity", "join to reserve detail by LIBRARY_COURSE_INSTRUCTOR_KEY"]}},
{{"table_file": "LIBRARY_RESERVE_MATRL_DETAIL.pkl", "subquestions_or_keywords": ["bridge between instructors/courses and reserve catalog materials"]}},
{{"table_file": "LIBRARY_RESERVE_CATALOG.pkl", "subquestions_or_keywords": ["library reserve material title", "join to reserve detail by LIBRARY_RESERVE_CATALOG_KEY"]}}
]
}}

Question:
{question}

Candidate table files:
{tables_text}

Predicted joinable table-file pairs:
{join_pairs_text}

Return only valid JSON:
{{
"relevant_table_files": ["..."],
"table_matches": [
{{
"table_file": "...",
"subquestions_or_keywords": ["..."]
}}
]
}}
"""


def _truncate(text: Any, max_chars: int) -> str:
    out = str(text).replace("\n", "\\n")
    return out[: max_chars - 3] + "..." if max_chars != -1 and len(out) > max_chars else out


_QUESTION_STOPWORDS = frozenset("""
a an the of in on for and or to all any what which who whom whose how many much
list state give show me is are was were be been with without their there that
this these those has have had from by at as not only can do does did if then
than more most least less between during before after each per number count
""".split())


def question_terms(question: str) -> List[str]:
    """Content words of the question, for matching against column names."""
    words = re.findall(r"[A-Za-z][A-Za-z0-9]+", str(question or "").lower())
    return [w for w in words if len(w) > 2 and w not in _QUESTION_STOPWORDS]


def _matches_question(header: Any, terms: Sequence[str]) -> bool:
    h = re.sub(r"[^a-z0-9]", "", str(header).lower())
    if not h:
        return False
    return any(t in h or (len(h) > 2 and h in t) for t in terms)


def trim_headers(headers: Sequence[Any],
                 max_columns: int = MAX_COLUMNS_PER_TABLE,
                 max_column_chars: int = MAX_COLUMN_NAME_CHARS,
                 question: str = "") -> List[str]:
    """Keep the head, the tail, and any column the QUESTION names.

    Head-and-tail rather than the first N: wide tables put identifiers first and
    measures last, so a prefix hides every measure column.

    The question-aware part is not a refinement — positional trimming was
    dropping the one column that decides the answer. `bird_496c969d` asks about
    "anti-SSA" and its gold table has 44 columns of which 21 were shown; `SSA`
    was in the omitted middle, while a distractor table 11 columns wide showed
    `anticardiolipin_IgG` and `ANA_titer` in full. Schema linking picked the
    distractor, and no downstream evidence could have recovered from that,
    because the deciding column was never in the prompt. Three of the 32
    revise_table failures are exactly this shape (SSA, IGG, TP), all on the same
    44-column table.

    Matched columns are inserted in their original position, so the ordering
    still carries the table's structure.
    """
    headers = list(headers)
    if max_columns == -1 or len(headers) <= max_columns:
        return [_truncate(h, max_column_chars) for h in headers]

    head = max_columns // 2
    tail = max_columns - head
    keep = set(range(head)) | set(range(len(headers) - tail, len(headers)))
    terms = question_terms(question)
    if terms:
        keep |= {i for i, h in enumerate(headers) if _matches_question(h, terms)}

    picked: List[Any] = []
    prev = -1
    for i in sorted(keep):
        if i > prev + 1:
            picked.append(f"... {i - prev - 1} columns omitted ...")
        picked.append(headers[i])
        prev = i
    if prev < len(headers) - 1:
        picked.append(f"... {len(headers) - 1 - prev} columns omitted ...")
    return [_truncate(h, max_column_chars) for h in picked]




# ============================================================
# Candidate tables
# ============================================================

@dataclass
class CandidateTable:
    """One table as the prompt sees it."""
    file_name: str
    headers: List[str] = field(default_factory=list)
    recovered: bool = False
    original_header_count: int = 0
    recovered_header_count: int = 0
    omitted_header_count: int = 0

    def to_dict(self) -> dict:
        return {
            "file_name": self.file_name,
            "headers": self.headers,
            "used_recovered_headers": self.recovered,
            "original_header_count": self.original_header_count,
            "recovered_header_count": self.recovered_header_count,
            "omitted_header_count": self.omitted_header_count,
        }


def build_candidates(table_files: Sequence[str],
                     metadata: Dict[str, dict],
                     question: str = "",
                     on_missing: str = "error",
                     max_columns_per_table: int = MAX_COLUMNS_PER_TABLE,
                     max_column_name_chars: int = MAX_COLUMN_NAME_CHARS,
                     ) -> List[CandidateTable]:
    """Assemble the prompt's candidate list from the offline metadata.

    on_missing="error"    raise when a table has no metadata (default)
    on_missing="original" fall back to its raw header row, and flag it
    on_missing="skip"     drop the table from the pool
    """
    out: List[CandidateTable] = []
    missing: List[str] = []

    for tf in table_files:
        record = metadata.get(tf) or {}
        original = list(record.get("original_headers") or [])
        recovered = list(record.get("recovered_schema") or [])

        if not recovered:
            missing.append(tf)
            if on_missing == "skip":
                continue
            if on_missing == "error":
                continue                       # collected, raised together below
            headers, used = original, False
        else:
            headers, used = recovered, True

        out.append(CandidateTable(
            file_name=tf,
            headers=trim_headers(headers, max_columns_per_table,
                                 max_column_name_chars, question),
            recovered=used,
            original_header_count=len(original),
            recovered_header_count=len(recovered),
            omitted_header_count=(max(0, len(headers) - max_columns_per_table)
                                  if max_columns_per_table != -1 else 0),
        ))

    if missing and on_missing == "error":
        raise LookupError(
            f"no metadata for {len(missing)} table(s): {missing[:5]}. "
            f"Run meta_inferrence.py for this dataset, or pass "
            f"--on-missing original to fall back (the fallback is recorded, not silent)."
        )
    return out


def format_tables(tables: Sequence[CandidateTable]) -> str:
    blocks = []
    for i, t in enumerate(tables, 1):
        note = (f"\n   note: {t.omitted_header_count} columns were omitted from this preview."
                if t.omitted_header_count else "")
        blocks.append(f"{i}. file_name: {t.file_name}\n"
                      f"   columns: [{', '.join(t.headers)}]{note}")
    return "\n\n".join(blocks)


# ============================================================
# Join evidence (warehouse datasets only)
# ============================================================

def _table_of(column_ref: str) -> str:
    """"TABLE.COLUMN" -> "TABLE" (upper case, no path or #sep# prefix)."""
    name = str(column_ref).split(".", 1)[0].strip().split("/")[-1]
    if "#sep#" in name:
        name = name.split("#sep#")[-1]
    return name.upper()


def _file_stem(table_file: str) -> str:
    name = str(table_file).split("/")[-1]
    return (name[:-4] if name.lower().endswith(".pkl") else name).upper()


def join_table_pairs(table_files: Sequence[str], join_keys_path: Path) -> List[List[str]]:
    """Predicted joinable file pairs among the candidates.

    Reads the join graph built by build_join_graph.py, which lists column pairs
    as ["T1.C1", "T2.C2"], and lifts them to file pairs. Returns [] when the
    graph is absent, in which case the prompt says so rather than misleading.
    """
    join_keys_path = Path(join_keys_path)
    if not join_keys_path.exists():
        return []
    try:
        pairs = json.loads(join_keys_path.read_text())
    except Exception:
        return []

    by_stem = {_file_stem(tf): tf for tf in table_files}
    seen, out = set(), []
    for pair in pairs:
        if not (isinstance(pair, (list, tuple)) and len(pair) == 2):
            continue
        a, b = _table_of(pair[0]), _table_of(pair[1])
        if a == b or a not in by_stem or b not in by_stem:
            continue
        key = tuple(sorted((a, b)))
        if key in seen:
            continue
        seen.add(key)
        out.append([by_stem[a], by_stem[b]])
    return out


def format_join_pairs(pairs: Sequence[Sequence[str]]) -> str:
    lines = [f"- {p[0]} <-> {p[1]}" for p in pairs
             if isinstance(p, (list, tuple)) and len(p) == 2]
    return "\n".join(lines) or "No predicted joinable table-file pairs found among the candidate tables."


# ============================================================
# Selection
# ============================================================

def build_prompt(dataset: str, question: str, tables: Sequence[CandidateTable],
                 pairs: Optional[Sequence[Sequence[str]]] = None) -> str:
    max_tables = MAX_TABLES.get(dataset, 4)
    if DS.SOURCE_NAME.get(dataset, dataset) == "beaver":
        return BEAVER_PROMPT.format(max_tables=max_tables, question=question,
                                    tables_text=format_tables(tables),
                                    join_pairs_text=format_join_pairs(pairs or []))
    return PROMPT.format(max_tables=max_tables, question=question,
                         tables_text=format_tables(tables))


def _parse_json(text: Any) -> dict:
    if isinstance(text, dict):
        return text
    body = str(text or "").strip()
    if body.startswith("```"):
        body = body.strip("`").strip()
        if body.lower().startswith("json"):
            body = body[4:].strip()
    return json.loads(body)


def select_tables(question: str,
                  table_files: Sequence[str],
                  metadata: Dict[str, dict],
                  *,
                  dataset: str = "Synth-Bird",
                  model: str = DEFAULT_MODEL,
                  on_missing: str = "error",
                  join_keys_path: Optional[Path] = None,
                  prompt_suffix: str = "",
                  ) -> Dict[str, Any]:
    """Select the tables one question needs, with a subquestion for each.

    prompt_suffix  text appended verbatim after the standard prompt. This is the
                   only hook the self-correction module's `revise_table` uses: a
                   repair must differ from the first pass by the diagnostic
                   evidence and NOTHING else, or an A/B measures the prompt
                   rewrite instead of the evidence.

    Returns {selected_tables, subquestions, table_matches, candidates,
             hallucinated_tables, fell_back_to_original, usage}.
    """
    candidates = build_candidates(table_files, metadata, question=question,
                                  on_missing=on_missing)
    if not candidates:
        raise ValueError("no candidate tables survived; nothing to select from")

    pairs: List[List[str]] = []
    if DS.SOURCE_NAME.get(dataset, dataset) == "beaver" and join_keys_path:
        pairs = join_table_pairs([c.file_name for c in candidates], join_keys_path)

    prompt = build_prompt(dataset, question, candidates, pairs) + (prompt_suffix or "")

    t0 = time.perf_counter()
    resp = llm_generate_setup(prompt, model=model, json_format=True)
    usage = {
        "calls": 1,
        "input": int(resp.get("input_tokens") or 0),
        "output": int(resp.get("output_tokens") or 0),
        "elapsed_seconds": round(time.perf_counter() - t0, 3),
        "model": model,
    }
    out = _parse_json(resp.get("text"))

    offered = {c.file_name for c in candidates}

    def _resolve(name: Any) -> Optional[str]:
        """Map the model's answer back to an offered file name.

        The prompt lists candidates as `file_name: X.pkl` and the model
        sometimes echoes that label back; treating those as hallucinations would
        empty the selection and fail the task outright.
        """
        raw = str(name).strip()
        if raw in offered:
            return raw
        stripped = re.sub(r"^\s*file_name\s*:\s*", "", raw).strip().strip("`'\"")
        if stripped in offered:
            return stripped
        base = stripped.split("/")[-1]
        return base if base in offered else None

    selected, hallucinated = [], []
    for f in (out.get("relevant_table_files") or []):
        r = _resolve(f)
        (selected if r else hallucinated).append(r or str(f))

    matches = out.get("table_matches") or []
    subquestions = {}
    for m in matches:
        r = _resolve(m.get("table_file")) if m.get("table_file") else None
        if r:
            subquestions[r] = list(m.get("subquestions_or_keywords") or [])

    return {
        "dataset": dataset,
        "question": question,
        "candidate_tables": [c.file_name for c in candidates],
        "selected_tables": selected,
        "hallucinated_tables": hallucinated,
        "table_matches": matches,
        "subquestions": subquestions,
        "candidates": [c.to_dict() for c in candidates],
        "fell_back_to_original": [c.file_name for c in candidates if not c.recovered],
        "usage": usage,
    }


# ============================================================
# Candidate pool per dataset
# ============================================================

def load_retrieved_pool(dataset: str, retrieval_path: Optional[Path] = None,
                        top_k: int = 10) -> Dict[str, List[str]]:
    """{question: [table files]} from this module's retrieval output.

    Reads exp_g_domain_{top_k}.json, which expand_compare.py keys by question
    text and whose entries are bare table names. Returns {} when absent, and the
    caller then falls back to each task's own `retrieved_table`.
    """
    if retrieval_path is None:
        paths = P.resolve(dataset, group="offline_online")
        retrieval_path = paths.out_dir / f"exp_g_domain_{top_k}.json"
    retrieval_path = Path(retrieval_path)
    if not retrieval_path.exists():
        return {}
    raw = json.loads(retrieval_path.read_text())
    return {q: [str(t) for t in tables] for q, tables in raw.items()}


def candidate_pool_for_task(task: Dict[str, Any], dataset: str,
                            retrieved_by_question: Dict[str, List[str]],
                            known_tables: Sequence[str],
                            top_k: int = 10) -> List[str]:
    """The candidate tables shown to the model for one task.

    Synth-*  : the task's own `input_table` pool.
    Beaver   : the top-k retrieved tables — from exp_g_domain_{k}.json when this
               module's retrieval has been run, otherwise the `retrieved_table`
               recorded in benchmark.jsonl.
    """
    if DS.SOURCE_NAME.get(dataset, dataset) != "beaver":
        return list(task.get("input_table") or [])

    retrieved = retrieved_by_question.get(task.get("question", ""))
    if retrieved:
        # Retrieval reports bare table names; map them back to file names.
        #
        # Retrieval ranges over dev_tables.json, which describes 97 tables,
        # while the materialized collection holds 96 files: SUBJECT_SUMMARY has
        # a profile but no .pkl. A retrieved name with no file is dropped here
        # rather than passed through, because passing it on would either abort
        # the task under on_missing="error" or silently offer the model a table
        # it cannot see. Dropping shortens the pool, which is reported.
        by_stem = {_file_stem(t): t for t in known_tables}
        pool, seen, unresolved = [], set(), []
        for name in retrieved[:top_k]:
            f = by_stem.get(_file_stem(name))
            if f is None:
                unresolved.append(str(name))
                continue
            if f not in seen:
                seen.add(f)
                pool.append(f)
        if unresolved:
            print(f"[select] task {task.get('task_id')}: {len(unresolved)} retrieved "
                  f"table(s) have no file in the collection, dropped: {unresolved}")
        return pool

    return list(task.get("retrieved_table") or task.get("input_table") or [])[:top_k]


# ============================================================
# Entry point
# ============================================================

def run_selection(dataset: str, out_path: Path, model: str = DEFAULT_MODEL,
                  metadata_path: Optional[Path] = None,
                  retrieval_path: Optional[Path] = None,
                  join_keys_path: Optional[Path] = None,
                  top_k: int = 10, on_missing: str = "error",
                  task_ids: Optional[Sequence[str]] = None, limit: int = 0,
                  overwrite: bool = False) -> Path:
    """Select tables for every task of one dataset, one JSONL record each.

    The output file doubles as the cache: a task already present is skipped, so
    an interrupted run resumes without paying for it twice.
    """
    ds = DS.resolve(dataset)
    tasks = ds.select(task_ids=task_ids)

    metadata_path = Path(metadata_path or default_metadata_path(dataset))
    metadata = load_table_metadata(metadata_path)
    if not metadata:
        raise FileNotFoundError(
            f"no table metadata at {metadata_path}. "
            f"Run: python -m table_discovery.meta_inferrence --dataset {dataset}")

    is_warehouse = DS.SOURCE_NAME.get(dataset, dataset) == "beaver"
    retrieved_by_question = (load_retrieved_pool(dataset, retrieval_path, top_k)
                             if is_warehouse else {})
    if is_warehouse and join_keys_path is None:
        join_keys_path = (P.resolve(dataset, group="offline_online").out_dir
                          / "dw_join_keys_g_domain.json")

    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    if overwrite and out_path.exists():
        out_path.unlink()

    done = load_jsonl_by_key(out_path, "task_id")
    pending = [t for t in tasks if str(t.get("task_id")) not in done]
    if limit and limit > 0:
        pending = pending[:limit]

    print(f"[select] dataset={dataset} warehouse_prompt={is_warehouse}")
    print(f"[select] metadata:  {metadata_path} ({len(metadata)} tables)")
    if is_warehouse:
        src = "exp_g_domain" if retrieved_by_question else "benchmark.jsonl retrieved_table"
        print(f"[select] pool:      top-{top_k} from {src}")
    print(f"[select] tasks={len(tasks)} cached={len(done)} to_process={len(pending)}")
    print(f"[select] output:    {out_path}")

    known_tables = sorted(metadata.keys())
    written, failed = 0, []

    for task in tqdm(pending, desc="Selecting tables"):
        task_id = str(task.get("task_id"))
        pool = candidate_pool_for_task(task, dataset, retrieved_by_question,
                                       known_tables, top_k=top_k)
        try:
            result = select_tables(
                question=task.get("question", ""),
                table_files=pool,
                metadata=metadata,
                dataset=dataset,
                model=model,
                on_missing=on_missing,
                join_keys_path=join_keys_path,
            )
        except Exception as exc:  # noqa: BLE001 - record and continue
            failed.append((task_id, str(exc)))
            print(f"[select] task {task_id} failed: {exc}")
            continue

        result["task_id"] = task_id
        append_jsonl(out_path, result)
        written += 1

    print(f"[select] wrote {written} records; {len(failed)} failed")
    if failed:
        print(f"[select] failures: {failed[:5]}")
    return out_path


def default_selection_path(dataset: str, out_dir: str | None = None) -> Path:
    return P.resolve(dataset, out_dir=out_dir, group="selection").out("table_selection.jsonl")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Online: select the relevant tables for each question.")
    parser.add_argument("--dataset", type=str, default="Beaver-Prep",
                        help="Dataset name, e.g. Beaver-Prep, Synth-Bird, Synth-Spider.")
    parser.add_argument("--metadata", type=Path, default=None,
                        help="Override the table metadata JSONL from meta_inferrence.py.")
    parser.add_argument("--retrieval", type=Path, default=None,
                        help="Beaver only: override the retrieval output "
                             "(exp_g_domain_<top_k>.json) used as the candidate pool.")
    parser.add_argument("--join-keys", type=Path, default=None,
                        help="Beaver only: override the join graph shown as evidence.")
    parser.add_argument("--out", type=Path, default=None,
                        help="Override the output JSONL. Default: "
                             "results/table_discovery/selection/<Dataset>/table_selection.jsonl")
    parser.add_argument("--model", type=str, default=DEFAULT_MODEL)
    parser.add_argument("--top-k", type=int, default=10,
                        help="Beaver only: candidate tables taken from retrieval.")
    parser.add_argument("--on-missing", choices=["error", "original", "skip"],
                        default="error",
                        help="What to do with a table that has no metadata.")
    parser.add_argument("--task-ids", type=str, nargs="+", default=None,
                        help="Only these task ids.")
    parser.add_argument("--limit", type=int, default=0,
                        help="Process at most N not-yet-done tasks (0 = all).")
    parser.add_argument("--overwrite", action="store_true",
                        help="Discard existing results and start over.")
    return parser.parse_args()


if __name__ == "__main__":
    a = parse_args()
    run_selection(
        dataset=a.dataset,
        out_path=a.out or default_selection_path(a.dataset),
        model=a.model,
        metadata_path=a.metadata,
        retrieval_path=a.retrieval,
        join_keys_path=a.join_keys,
        top_k=a.top_k,
        on_missing=a.on_missing,
        task_ids=a.task_ids,
        limit=a.limit,
        overwrite=a.overwrite,
    )
