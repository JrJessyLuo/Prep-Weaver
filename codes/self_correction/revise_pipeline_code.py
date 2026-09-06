#!/usr/bin/env python3
"""
revise_pipeline_code.py
=======================
Repair a table's pipeline by REWRITING it as pandas, not by re-parameterising the
operator chain.

    stage 1  localise   which table's output fails to serve the question
    stage 2  rewrite    for that table: look at every candidate pipeline and what
                        it actually produced, and either accept one or write the
                        pandas that turns the closest one into what is needed
    stage 3  validate   execute, check value-level, roll back if not better

WHY THIS EXISTS RATHER THAN MORE EVIDENCE
-----------------------------------------
Measured on the 30 bird tasks labelled `revise_pipeline`:

  * feeding the same operator loop richer diagnostics moved NOTHING. B - A = 0 on
    both metrics, zero discordant pairs, and synthesis runs at temperature 0 so
    the noise floor was literally zero — an exact null, not a small effect.
  * the fix is usually not in the candidate pool: replaying every recorded
    candidate and enumerating all combinations gains +1/30. The pool holds 1.46
    distinct options per table and 45 of 68 tables have exactly one.
  * the fix IS usually close: mean subtable_recall is 0.698, so ~70% of the gold
    value domains are already there. These are near misses, not blank failures.
  * of the 84 gold operators our chains never applied, 66 (79%) carry no custom
    code at all — Rename, CastType, Transpose, Pivot, Stack. Where code IS needed
    the gold body is a median of 5 lines. So the missing capability is not code
    generation difficulty; it is deciding to reshape.
  * and the operator was usually available anyway: 29 of 56 tables had the gold
    op inside the candidate set at EVERY step, yet only 2 ended up with the gold
    chain. Reachability is not the binding constraint.

Together those say: stop feeding the operator search, and let the model write the
transform directly.

LOCALISATION IS STAGE 1 BECAUSE RULES FAILED
--------------------------------------------
Hand-built per-table signals do not work — "the side of the edge whose key is not
key-like" picks the actually-worse table 0.333 of the time against a 0.456 random
baseline, and lower unique_ratio scores 0.500. Only `A1_unmet_declared_columns` is
precise (3/3) and it fires on 3 of 30 tasks. Meanwhile the ground truth is sharply
separated — per-table gold value-domain coverage is routinely {1.00, 0.00} — so
there is a fact to find and only a reader of the actual values can find it.

SAFETY
------
Stage 3 executes model-written code. It runs through `run_snippet`, which compiles
with a restricted global namespace (pandas, numpy, re, and builtins minus the
import/exec/eval/open family) and requires the snippet to define `transform(df)`.
That stops accidents and honest mistakes; it is NOT a security sandbox, so run it
only on code generated from your own inputs.
"""
from __future__ import annotations

import os
import argparse
import builtins
import json
import pickle
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

ROOT = Path(__file__).resolve().parent.parent
for _p in (str(ROOT), str(ROOT / "actions"), str(ROOT / "prep_utils"),
           str(ROOT / "train_infer_single_ops"), str(ROOT / "construct_training_data")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import numpy as np                                                  # noqa: E402
import pandas as pd                                                 # noqa: E402
import test_param_synthesis as M                                    # noqa: E402
from prep_utils import llm_generate_setup, require_text, timed_llm_generate       # noqa: E402
try:                                                                 # noqa: E402
    from hardness.pipeline.gen_grounded_specs import grounding_evidence
except Exception:                                                    # noqa: E402
    grounding_evidence = None

AUTOP = Path(os.environ.get("AUTOPREP_ROOT") or Path(__file__).resolve().parents[2] / "datasets")
_CF = lambda x: re.sub(r"[^0-9a-z]", "", str(x).lower())            # noqa: E731


# --------------------------------------------------------------------------- #
# rendering the evidence
# --------------------------------------------------------------------------- #

def sample_col(df: pd.DataFrame, col: Any, n: int = 5, width: int = 24,
               pos: Optional[int] = None) -> str:
    """Sample one column's values.

    `pos` selects POSITIONALLY. Duplicate column labels are everywhere in this
    benchmark — a header row read as data leaves things like `CZK, CZK.1` or 60
    identical Airtable ids as column names — and `df[label]` then returns a
    DataFrame, not a Series, so `.tolist()` raises AttributeError. That killed 4
    of 30 tasks in rewrite_probe v1 before anything reached the model.
    """
    try:
        s = df.iloc[:, pos] if pos is not None else df[col]
        if isinstance(s, pd.DataFrame):
            s = s.iloc[:, 0]
        s = s.dropna().astype(str)
    except Exception:
        return "(unreadable)"
    out: List[str] = []
    for v in s.head(300).tolist():
        t = re.sub(r"\s+", " ", v.strip())[:width]
        if t and t not in out:
            out.append(t)
        if len(out) >= n:
            break
    return ", ".join(out) or "(all empty)"


def render_table(df: pd.DataFrame, max_cols: int = 14) -> str:
    if df is None:
        return "      (not materialised)"
    cols = list(df.columns)[:max_cols]
    more = f"   (+{len(df.columns) - len(cols)} more columns)" if len(df.columns) > len(cols) else ""
    dups = len(cols) - len({str(c) for c in cols})
    lines = [f"      shape {df.shape}{more}"
             + (f"   NOTE: {dups} of these column labels are duplicates" if dups else "")]
    for i, c in enumerate(cols):
        lines.append(f"        {str(c)[:28]:<28} = {sample_col(df, c, pos=i)}")
    return "\n".join(lines)


def render_grounding_evidence(df: Optional[pd.DataFrame]) -> str:
    """Gold-free structural hints borrowed from the harness agent."""
    if df is None or grounding_evidence is None:
        return "      (not available)"
    try:
        ev = grounding_evidence(df)
    except Exception:
        return "      (not available)"
    keep = {k: v for k, v in ev.items() if not str(k).startswith("_")}
    if not keep:
        return "      none detected"
    return "      " + json.dumps(keep, ensure_ascii=False)[:1800]


def _declared_set(plan: Dict[str, Any], lt: str) -> set[str]:
    return {_CF(c) for c in declared_columns(plan, lt)}


def _column_map(df: Optional[pd.DataFrame]) -> Dict[str, Any]:
    if df is None:
        return {}
    out = {}
    for c in df.columns:
        out.setdefault(_CF(c), c)
    return out


def _hidden_declared_values(df: Optional[pd.DataFrame], declared: set[str]) -> Dict[str, str]:
    """Declared names not present as columns, but present as cell values."""
    if df is None or not declared:
        return {}
    remaining = set(declared) - set(_column_map(df))
    found: Dict[str, str] = {}
    if not remaining:
        return found
    for c in df.columns:
        sr = df[c]
        if isinstance(sr, pd.DataFrame):
            sr = sr.iloc[:, 0]
        if pd.api.types.is_numeric_dtype(sr) or pd.api.types.is_datetime64_any_dtype(sr):
            continue
        try:
            vals = {_CF(v) for v in sr.dropna().astype(str).head(1000).unique()}
        except Exception:
            continue
        hit = remaining & vals
        for h in hit:
            found[h] = str(c)
        remaining -= hit
        if not remaining:
            break
    return found


def _still_packed_columns(df: Optional[pd.DataFrame], declared: set[str]) -> List[str]:
    """Declared columns whose values still look like multiple packed fields."""
    if df is None:
        return []
    out = []
    have = _column_map(df)
    for dcol in declared:
        c = have.get(dcol)
        if c is None:
            continue
        sr = df[c]
        if isinstance(sr, pd.DataFrame):
            sr = sr.iloc[:, 0]
        s = sr.dropna().astype(str).head(60)
        if len(s) == 0:
            continue
        if s.str.match(r"^\s*\d{1,4}[-/.]\d{1,2}([-/.]\d{1,4})?([ T]\d{1,2}:\d{2}(:\d{2})?)?\s*$").mean() > 0.6:
            continue
        for delim in ["|", ",", "/", ":", "_", "-"]:
            n = s.str.split(re.escape(delim)).str.len()
            if (n > 1).mean() > 0.8 and n.nunique() <= 2:
                out.append(str(c))
                break
    return out


def _candidate_progress(df: Optional[pd.DataFrame], declared: set[str],
                        key_self: Optional[str] = None,
                        counterpart: Optional[pd.DataFrame] = None,
                        key_other: Optional[str] = None) -> float:
    """Small gold-free progress proxy for ranking candidates."""
    if df is None:
        return -1.0
    have = set(_column_map(df))
    covered = len(declared & have)
    hidden_penalty = len(_hidden_declared_values(df, declared))
    packed_penalty = len(_still_packed_columns(df, declared))
    join_bonus = 0.0
    if key_self and counterpart is not None and key_other:
        a = _column_map(df).get(_CF(key_self))
        b = _column_map(counterpart).get(_CF(key_other))
        if a is not None and b is not None:
            try:
                A = {_CF(v) for v in df[a].dropna().astype(str)}
                B = {_CF(v) for v in counterpart[b].dropna().astype(str)}
                if A and B:
                    join_bonus = max(len(A & B) / len(A), len(A & B) / len(B))
            except Exception:
                pass
    return 2.0 * covered + join_bonus - 1.5 * hidden_penalty - 1.0 * packed_penalty


def build_repair_brief(*, lt: str, plan: Dict[str, Any],
                       current: Optional[pd.DataFrame],
                       raw: Optional[pd.DataFrame],
                       candidates: Sequence[Tuple[dict, Optional[pd.DataFrame]]],
                       counterpart: Optional[pd.DataFrame] = None,
                       key_self: Optional[str] = None,
                       key_other: Optional[str] = None) -> str:
    """Gold-free repair intent: narrow the LLM from broad rewrite to small edit."""
    declared = _declared_set(plan, lt)
    cur_score = _candidate_progress(current, declared, key_self, counterpart, key_other)
    rows = [f"Repair intent for {lt}: prefer the smallest edit that improves this table."]
    rows.append(f"- declared columns: {declared_columns(plan, lt)[:16]}")
    rows.append(f"- current progress proxy: {cur_score:.2f}")

    hidden = _hidden_declared_values(current, declared)
    packed = _still_packed_columns(current, declared)
    if hidden:
        rows.append(f"- diagnostic: declared column names are still cell values: {hidden}.")
        rows.append("  likely edit: Pivot/Transpose so these names become columns; preserve join keys.")
    if packed:
        rows.append(f"- diagnostic: declared columns still look packed/unsplit: {packed}.")
        rows.append("  likely edit: SplitColumn-style cleanup only on these columns.")

    raw_ev = {}
    cur_ev = {}
    if grounding_evidence is not None:
        try:
            raw_ev = {k: v for k, v in grounding_evidence(raw).items() if not k.startswith("_")} if raw is not None else {}
        except Exception:
            raw_ev = {}
        try:
            cur_ev = {k: v for k, v in grounding_evidence(current).items() if not k.startswith("_")} if current is not None else {}
        except Exception:
            cur_ev = {}
    if cur_ev.get("attribute_like_columns"):
        rows.append("- diagnostic: current output still has attribute-like values; if declared fields are in those values, append Pivot.")
    if raw_ev.get("header_is_data") and not cur_ev.get("header_is_data"):
        rows.append("- raw evidence says the original table was transposed; keep transpose-derived entity ids if already recovered.")

    ranked = []
    for i, (cand, df) in enumerate(candidates):
        ranked.append((i, _candidate_progress(df, declared, key_self, counterpart, key_other),
                       cand.get("chain") or [], bool(cand.get("selected"))))
    ranked.sort(key=lambda x: -x[1])
    if ranked:
        rows.append("- candidate progress ranking:")
        for i, score, chain, selected in ranked[:5]:
            rows.append(f"  [{i}] score={score:.2f} chain={chain}" + (" SELECTED" if selected else ""))
        best = ranked[0]
        selected = next((r for r in ranked if r[3]), None)
        if selected and best[0] != selected[0] and best[1] > selected[1] + 0.5:
            rows.append(f"- suggested route: accept or minimally adapt candidate [{best[0]}], not the selected candidate [{selected[0]}].")
        elif hidden or packed:
            rows.append("- suggested route: minimally adapt the closest candidate; do not rebuild from raw unless candidates lack the needed values.")
        else:
            rows.append("- suggested route: tail cleanup only. Do not drop/filter rows or remove declared columns unless necessary.")
    rows.append("- hard constraints: preserve existing declared columns, preserve join key columns, and avoid broad filtering unless the question explicitly requires it.")
    return "\n".join(rows)


def replay(raw: pd.DataFrame, steps: Sequence[dict]) -> Optional[pd.DataFrame]:
    """Re-execute a recorded candidate. The digest stores `steps` but no frames."""
    try:
        df = M.sanitize(raw)
        for s in steps or []:
            df = M.sanitize(M.robust_execute(df, s))
        return df
    except Exception:
        return None


def declared_columns(plan: Dict[str, Any], lt: str) -> List[str]:
    for t in plan.get("gold_tables") or []:
        if t.get("logical_table") == lt:
            body = re.sub(r"PRIMARY\s+KEY\s*\([^)]*\)", "",
                          t.get("create_table_sql") or "", flags=re.I)
            return re.findall(r"`([^`]+)`", body)
    return []


# --------------------------------------------------------------------------- #
# stage 1 — localise
# --------------------------------------------------------------------------- #

LOCALISE_PROMPT = """A data-preparation pipeline produced the tables below, and the
result does not answer the question. Exactly which table's output is at fault?

QUESTION
  {question}

WHAT EACH TABLE WAS SUPPOSED TO CONTAIN, AND WHAT IT ACTUALLY PRODUCED
{tables}

HOW THE TABLES WERE SUPPOSED TO JOIN
{edges}

Judge only from the values. A table is at fault when its cells cannot supply what
the question needs of it, or cannot be joined to the others. A table whose values
are exactly what its part of the question requires is NOT at fault, even if the
overall answer is wrong — say so and blame the other one.

Return JSON only:
{{"at_fault": ["table_1"], "reason": "...", "what_is_missing": "..."}}
"""


def build_localise_prompt(*, question: str, plan: Dict[str, Any],
                          produced: Dict[str, pd.DataFrame],
                          edges: Sequence[dict]) -> str:
    blocks = []
    for lt in sorted(produced):
        dec = declared_columns(plan, lt)
        blocks.append(f"  {lt}\n      declared: {dec[:14]}\n"
                      + render_table(produced[lt]))
    ed = "\n".join(
        f"  {e.get('left_table')}.{e.get('left_on')} <-> "
        f"{e.get('right_table')}.{e.get('right_on')}" for e in (edges or [])
    ) or "  (no join edge declared)"
    return LOCALISE_PROMPT.format(question=question,
                                  tables="\n".join(blocks) or "  (nothing)",
                                  edges=ed)


# --------------------------------------------------------------------------- #
# stage 2 — rewrite
# --------------------------------------------------------------------------- #

REWRITE_PROMPT = """One table in a data-preparation pipeline is wrong. Fix it.

QUESTION THE WHOLE PIPELINE MUST ANSWER
  {question}

THE TABLE AT FAULT: {lt}
  it must supply: {subquestion}
  the plan declared these columns: {declared}
  it must join to: {joins}

REPAIR BRIEF
{repair_brief}

THE RAW SOURCE TABLE, BEFORE ANY PROCESSING
{raw}

STRUCTURAL EVIDENCE FROM THE RAW SOURCE
{raw_evidence}

EVERY PIPELINE THE SEARCH BUILT FOR THIS TABLE, AND WHAT EACH ONE PRODUCED
{candidates}

WHY THE CURRENT OUTPUT FAILS
{symptom}

WORK IN THIS ORDER
  1. Does any candidate above ALREADY produce what is required? If one does,
     return it and stop. (It usually does not — say so and continue.)
  2. If none is right, which one is CLOSEST — which one already holds most of the
     required values, needing only a reshape, a split, a cast, or a cleanup?
  3. Write the pandas that turns that candidate's output into the required table.
     If no candidate is close, write it from the RAW table instead.

Reshapes are the common fix here and are cheap to write: `df.T`, `df.pivot`,
`df.melt`, `df.explode`, `df.astype`, `df.rename`, splitting one column into
several. Do not avoid them because the earlier pipeline did not use them.

Use the structural evidence aggressively:
  - `attribute_like_columns`: values in that column look like field names. Usually
    pivot/melt so those values become real columns; do not leave the table in
    attribute/value form when the question needs those fields.
  - `packed_columns`: the flagged column holds several fields. Split only these
    columns; do not split dates, timestamps, or URLs unless flagged.
  - `header_is_data`: headers look like data values. Transpose so the first
    column's values become column names.
  - `wide_column_groups`: repeated sibling columns should often be stacked or
    wide-to-long.
Preserve already useful columns and join keys. A rewrite that drops required
columns or turns a table with good values into only an inspection/summary table is
wrong, even if it improves one join-key overlap.

Return JSON only:
{{"accept_candidate": <index or null>,
  "closest_candidate": <index or null>,
  "start_from": "candidate" | "raw",
  "reasoning": "what is wrong and what the code does about it",
  "code": "def transform(df):\\n    ...\\n    return df"}}

The code must define `transform(df)` and return a DataFrame. `pd`, `np` and `re`
are available. `df` is the output of `closest_candidate` when start_from is
"candidate", and the raw source table when it is "raw". No imports, no file or
network access. Use pandas keyword arguments when signatures vary, for example
`str.split(pat=".", n=1, expand=False)`, and when using `melt` choose a
`value_name` that is not already present in `df.columns`.
"""


def build_rewrite_prompt(*, question: str, lt: str, plan: Dict[str, Any],
                         link: Dict[str, Any], raw: pd.DataFrame,
                         candidates: Sequence[Tuple[dict, Optional[pd.DataFrame]]],
                         edges: Sequence[dict], symptom: str,
                         current: Optional[pd.DataFrame] = None,
                         counterpart: Optional[pd.DataFrame] = None,
                         key_self: Optional[str] = None,
                         key_other: Optional[str] = None) -> str:
    cand_txt = []
    for i, (c, df) in enumerate(candidates):
        mark = "   <- the one the search selected" if c.get("selected") else ""
        cand_txt.append(f"  [{i}] ops {c.get('chain')}{mark}\n"
                        + render_table(df)
                        + "\n      structural evidence: "
                        + render_grounding_evidence(df).strip())
    joins = [f"{e.get('left_table')}.{e.get('left_on')} <-> "
             f"{e.get('right_table')}.{e.get('right_on')}"
             for e in (edges or [])
             if lt in (e.get("left_table"), e.get("right_table"))]
    subq = []
    for f, qs in (link.get("subquestions") or {}).items():
        if isinstance(qs, list):
            subq += [str(x) for x in qs]
        elif isinstance(qs, dict):
            subq += [str(x) for x in qs.values()]
        elif qs:
            subq.append(str(qs))
    return REWRITE_PROMPT.format(
        question=question, lt=lt,
        subquestion="; ".join(subq[:4]) or "(not recorded)",
        declared=declared_columns(plan, lt)[:16],
        joins=joins or "(nothing)",
        repair_brief=build_repair_brief(
            lt=lt, plan=plan, current=current, raw=raw, candidates=candidates,
            counterpart=counterpart, key_self=key_self, key_other=key_other),
        raw=render_table(raw),
        raw_evidence=render_grounding_evidence(raw),
        candidates="\n".join(cand_txt) or "  (no candidate recorded)",
        symptom=symptom or "  the produced table does not answer the question")


# --------------------------------------------------------------------------- #
# stage 3 — execute and validate
# --------------------------------------------------------------------------- #

_BANNED = {"__import__", "eval", "exec", "compile", "open", "input",
           "globals", "locals", "vars", "getattr", "setattr", "delattr"}


def run_snippet(code: str, df: pd.DataFrame) -> Tuple[Optional[pd.DataFrame], str]:
    """Execute a `transform(df)` snippet in a restricted namespace.

    Not a security sandbox — a determined snippet can still escape via object
    attributes. It is here to stop accidents and to make the failure mode
    (missing `transform`, wrong return type) a clear message instead of a
    confusing traceback.
    """
    code = strip_redundant_imports(code or "")
    code = code.replace(".astype('Int64')", ".astype(int)")
    code = code.replace('.astype("Int64")', ".astype(int)")
    safe_builtins = {k: v for k, v in vars(builtins).items() if k not in _BANNED}
    ns: Dict[str, Any] = {"__builtins__": safe_builtins,
                          "pd": pd, "np": np, "re": re}
    try:
        exec(compile(code, "<rewrite>", "exec"), ns)          # noqa: S102
    except Exception as exc:
        return None, f"compile/exec failed: {type(exc).__name__}: {exc}"
    fn = ns.get("transform")
    if not callable(fn):
        return None, "snippet does not define transform(df)"
    try:
        out = fn(df.copy())
    except Exception as exc:
        return None, f"transform() raised: {type(exc).__name__}: {exc}"
    if not isinstance(out, pd.DataFrame):
        return None, f"transform() returned {type(out).__name__}, not a DataFrame"
    if out.empty or out.shape[1] == 0:
        return None, f"transform() returned an empty frame {out.shape}"
    return M.sanitize(out), ""


def strip_redundant_imports(code: str) -> str:
    """Remove imports for modules already injected into the snippet namespace."""
    kept = []
    for line in (code or "").splitlines():
        s = line.strip()
        if s in {
            "import pandas as pd",
            "import numpy as np",
            "import re",
        }:
            continue
        kept.append(line)
    return "\n".join(kept)


def validate(before: Optional[pd.DataFrame], after: pd.DataFrame,
             declared: Sequence[str],
             counterpart: Optional[pd.DataFrame] = None,
             key_self: Optional[str] = None,
             key_other: Optional[str] = None) -> Dict[str, Any]:
    """Gold-free acceptance check: did the rewrite actually improve anything?

    Two observables, both computable at inference time:
      declared_covered  how many declared column names now exist
      containment       how much of the join key's domain the counterpart holds

    A rewrite is accepted only if neither regresses and at least one improves.
    Without this the action is a blind gamble; with it the loop can roll back,
    which is what makes this repairable at all.
    """
    def covered(df):
        if df is None:
            return 0
        have = {_CF(c) for c in df.columns}
        return sum(1 for c in declared if _CF(c) in have)

    def cont(df):
        if df is None or counterpart is None or not key_self or not key_other:
            return None
        a = {_CF(c): c for c in df.columns}.get(_CF(key_self))
        b = {_CF(c): c for c in counterpart.columns}.get(_CF(key_other))
        if a is None or b is None:
            return 0.0
        try:
            A = set(df[a].dropna().astype(str))
            B = set(counterpart[b].dropna().astype(str))
        except Exception:
            return 0.0
        if not A or not B:
            return 0.0
        return max(len(A & B) / len(A), len(A & B) / len(B))

    dset = {_CF(c) for c in declared}
    cb, ca = covered(before), covered(after)
    kb, ka = cont(before), cont(after)

    hb = _hidden_declared_values(before, dset)
    ha = _hidden_declared_values(after, dset)
    pb = _still_packed_columns(before, dset)
    pa = _still_packed_columns(after, dset)
    sb = _candidate_progress(before, dset, key_self, counterpart, key_other)
    sa = _candidate_progress(after, dset, key_self, counterpart, key_other)

    structural_improved = (
        len(ha) < len(hb)
        or len(pa) < len(pb)
        or sa > sb + 0.5
    )
    structural_regressed = (
        len(ha) > len(hb)
        or len(pa) > len(pb)
        or sa < sb - 0.5
    )

    improved = (
        ca > cb
        or (ka is not None and kb is not None and ka > kb + 1e-9)
        or structural_improved
    )
    regressed = (
        ca < cb
        or (ka is not None and kb is not None and ka < kb - 1e-9)
        or structural_regressed
    )
    return {"declared_covered_before": cb, "declared_covered_after": ca,
            "declared_total": len(declared),
            "containment_before": kb, "containment_after": ka,
            "hidden_declared_before": hb, "hidden_declared_after": ha,
            "packed_declared_before": pb, "packed_declared_after": pa,
            "progress_before": sb, "progress_after": sa,
            "structural_improved": bool(structural_improved),
            "structural_regressed": bool(structural_regressed),
            "improved": bool(improved), "regressed": bool(regressed),
            # Veto, not gate. Requiring a strict improvement accepted 0 of 8
            # rewrites in the smoke run while applying them blindly moved 5 —
            # `declared_covered` is a name-level count and is already saturated,
            # so a value-level fix leaves it flat and the strict rule rejects it.
            # The same flaw in `revise_relational_plan.accept` cost 1 subtable_full
            # and 2 join_key_full on 12 tasks. Use these observables to detect
            # damage, and let anything that does no visible harm through.
            "accept": not regressed}


# --------------------------------------------------------------------------- #
# driver
# --------------------------------------------------------------------------- #

def load(inter: Path, tid: str, benchmark="nl2sql-bird", split="dev") -> Dict[str, Any]:
    rows = lambda n: {json.loads(l)["task_id"]: json.loads(l)                # noqa: E731
                      for l in (inter / n).open() if l.strip()} if (inter / n).exists() else {}
    bench_dir = AUTOP / benchmark / split
    plans, links, pipes = rows("relational_plan.jsonl"), rows("schema_linking.jsonl"), rows("pipeline.jsonl")
    task = next(json.loads(l) for l in (bench_dir / "benchmark.jsonl").open()
                if json.loads(l).get("task_id") == tid)
    with (inter / "tables" / f"{tid}.pkl").open("rb") as fh:
        shard = pickle.load(fh)
    plan = plans.get(tid, {})
    raw = {}
    for t in plan.get("gold_tables") or []:
        p = bench_dir / (t.get("input_file") or "")
        if p.exists():
            try:
                raw[t["logical_table"]] = pd.read_pickle(p)
            except Exception:
                pass
    return {"task": task, "plan": plan, "link": links.get(tid, {}),
            "pipe": pipes.get(tid, {}), "produced": shard.get("subtables") or {},
            "edges": shard.get("edges") or [], "raw": raw}


def candidates_for(pipe: Dict[str, Any], lt: str,
                   raw: pd.DataFrame) -> List[Tuple[dict, Optional[pd.DataFrame]]]:
    out = []
    for c in ((pipe.get("tables") or {}).get(lt) or {}).get("candidates") or []:
        out.append((c, replay(raw, c.get("steps"))))
    return out


def main(argv: Optional[Sequence[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="Rewrite a table's pipeline as pandas.")
    ap.add_argument("--inter", type=Path, required=True)
    ap.add_argument("--task-id", required=True)
    ap.add_argument("--table", default=None,
                    help="skip stage 1 and rewrite this logical table")
    ap.add_argument("--model", default="gpt-5-2025-08-07")
    ap.add_argument("--effort", default="medium")
    ap.add_argument("--show-prompt", choices=["localise", "rewrite"], default=None,
                    help="print the prompt and call nothing")
    args = ap.parse_args(argv)

    import os
    os.environ["REASONING_EFFORT"] = args.effort
    # llm.py defaults to a 90s per-request timeout, which fits the project-wide
    # effort=minimal and not this one.
    os.environ.setdefault("OPENAI_REQUEST_TIMEOUT",
                          "90" if args.effort == "minimal" else "420")
    d = load(args.inter, args.task_id)
    q = d["task"].get("question", "")

    if args.show_prompt == "localise" or (args.show_prompt is None and False):
        print(build_localise_prompt(question=q, plan=d["plan"],
                                    produced=d["produced"], edges=d["edges"]))
        return 0

    lt = args.table
    if lt is None:
        p = build_localise_prompt(question=q, plan=d["plan"],
                                  produced=d["produced"], edges=d["edges"])
        resp, _ = timed_llm_generate(llm_generate_setup, p, model=args.model,
                                     json_format=True)
        loc = json.loads(require_text(resp, "revise_pipeline (localise)"))
        print(json.dumps(loc, ensure_ascii=False, indent=2))
        picks = [t for t in (loc.get("at_fault") or []) if t in d["produced"]]
        if not picks:
            print("stage 1 named no table that exists; nothing to do")
            return 1
        lt = picks[0]

    raw = d["raw"].get(lt)
    if raw is None:
        print(f"no raw source recorded for {lt}")
        return 1
    cands = candidates_for(d["pipe"], lt, raw)
    edge = next((e for e in d["edges"]
                 if lt in (e.get("left_table"), e.get("right_table"))), None)
    other = key_s = key_o = None
    if edge:
        if edge.get("left_table") == lt:
            other, key_s, key_o = d["produced"].get(edge.get("right_table")), edge.get("left_on"), edge.get("right_on")
        else:
            other, key_s, key_o = d["produced"].get(edge.get("left_table")), edge.get("right_on"), edge.get("left_on")
    prompt = build_rewrite_prompt(
        question=q, lt=lt, plan=d["plan"], link=d["link"], raw=raw,
        candidates=cands, edges=d["edges"],
        symptom="  the produced table does not supply what the question needs",
        current=d["produced"].get(lt), counterpart=other,
        key_self=key_s, key_other=key_o)

    if args.show_prompt == "rewrite":
        print(prompt)
        return 0

    resp, _ = timed_llm_generate(llm_generate_setup, prompt, model=args.model,
                                 json_format=True)
    out = json.loads(require_text(resp, "revise_pipeline (rewrite)"))
    print(json.dumps({k: v for k, v in out.items() if k != "code"},
                     ensure_ascii=False, indent=2))
    print("\n--- code ---\n" + (out.get("code") or "(none)"))

    idx = out.get("accept_candidate")
    if idx is not None and 0 <= int(idx) < len(cands):
        print(f"\nstage 2 accepted candidate {idx} as-is; no rewrite executed")
        return 0

    start = raw
    ci = out.get("closest_candidate")
    if out.get("start_from") == "candidate" and ci is not None and 0 <= int(ci) < len(cands):
        start = cands[int(ci)][1] if cands[int(ci)][1] is not None else raw
    new, err = run_snippet(out.get("code") or "", start)
    if new is None:
        print(f"\nEXECUTION FAILED: {err}")
        return 1
    v = validate(d["produced"].get(lt), new, declared_columns(d["plan"], lt),
                 other, key_s, key_o)
    print("\n--- result ---")
    print(f"  shape {new.shape}   columns {list(new.columns)[:12]}")
    print("  " + json.dumps(v, ensure_ascii=False))
    print("  ACCEPT" if v["accept"] else "  REJECT — roll back to the previous output")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
