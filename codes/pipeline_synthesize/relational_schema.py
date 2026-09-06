"""Stage 1 of pipeline synthesis: question + selected tables -> RELATIONAL SCHEMA.

Input  : results/table_discovery/selection/<Dataset>/table_selection.jsonl
         datasets/<Dataset>/input_tables/*.pkl
Output : results/pipeline_synthesize/schema/<Dataset>/relational_schema.jsonl
         one record per task:
           {task_id, question, input_tables,
            tables:     [{logical_table, input_file, db_table, create_table_sql}],
            join_edges: [{left_table, left_on, right_table, right_on}]}

The relational schema declares, for each selected table, the CREATE TABLE it
should have AFTER preparation, plus the join keys connecting those tables. It
does not contain an answer SQL: this module describes the shape of the prepared
data, and answering the question is a separate concern downstream.

THE IDEA
--------
A prepared table's schema is DERIVED, not recalled. Retrieved few-shot examples
mostly teach output format; the actual knowledge comes from two places:
    the question              -> WHICH information is needed
    the raw table's content   -> WHERE that information lives and what it is called
So instead of "retrieve K similar tasks and imitate", we compute DETERMINISTIC
layout evidence from the real data and let the model read the target schema off
it.

WHY THESE FOUR DETECTORS AND NOT ONE PER OPERATION
--------------------------------------------------
The schema declares column NAMES, so the only question worth detecting is:

        *where does the target column's name live in the raw data right now?*

The four detectors below enumerate the possible answers, and the operation is
simply the inverse map that moves the name back onto the header row:

        name already on the header row       ->  no operation
        name in the first column's VALUES    ->  Transpose
        name in an attribute column's VALUES ->  Pivot
        name split across `stub_suffix` heads->  WideToLong / Stack
        name does not exist; values share one cell -> SplitColumn (name invented)

That framing also explains what is NOT detected, measured over the 155 gold
operations of the 43-task eval set:
    covered   58.1%   Transpose 19.4 | Pivot 17.4 | SplitColumn 12.9
                      | Stack 6.5 | WideToLong 1.9
    uncovered 41.9%   Rename 23.9 | Concatenate 5.8 | StandardizeString 5.2
                      | CastType 4.5 | Explode 1.9 | StandardizeDatetime 0.6
The uncovered set splits in two, for different reasons:
  (a) CastType / StandardizeString / StandardizeDatetime change values or types
      but not the attribute set, so a schema-declaring stage is indifferent to
      them. Explode is in this group too (it changes ROW granularity, not
      columns) but is a blind spot: a join key can be name-correct and still be
      a comma-joined list, which no name-based signal can see.
  (b) Rename (the single most frequent operation) and Concatenate DO change
      attributes, but the target name exists nowhere in the data — only the
      question implies it. No detector can recover these, and they are the
      method's inherent ceiling.

Run:
    python -m pipeline_synthesize.relational_schema --dataset Synth-Bird
"""
from __future__ import annotations

import argparse
import json
import os
import re
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

import pandas as pd
from tqdm import tqdm

from common import dataset as DS
from common import paths as P
from common.io_utils import append_jsonl, load_jsonl, load_jsonl_by_key

PREVIEW_ROWS = 4
MAX_CELL_CHARS = 160


# ============================================================================================
# 1. EVIDENCE SPECIFICATIONS — the single source of truth
#
# Each entry ties together: how the evidence is detected, which operation it implies, where the
# target column names come from, and the instruction the model is given. `grounding_evidence()`
# and the prompt's RULES section are both generated from this list, so the two can never drift.
# ============================================================================================
@dataclass(frozen=True)
class EvidenceSpec:
    key: str                       # field name in the evidence dict
    implied_op: str                # the operation this evidence calls for
    name_source: str               # where the target column names come from
    instruction: str               # what the model must do when this evidence fires
    detect: Callable[[pd.DataFrame], object]   # returns a JSON-able payload, or None


def _short(value, limit: int = MAX_CELL_CHARS) -> str:
    try:
        missing = pd.isna(value)
        if not isinstance(missing, bool):
            missing = False
    except Exception:
        missing = False
    text = "" if missing else str(value)
    return text if len(text) <= limit else f"{text[:limit]}...<+{len(text) - limit} chars>"


def _col(df: pd.DataFrame, c):
    """A column as a Series even when duplicate headers make df[c] a DataFrame."""
    s = df[c]
    return s.iloc[:, 0] if isinstance(s, pd.DataFrame) else s


# ---- (a) attribute-like column -> Pivot ----------------------------------------------------
# EXAMPLE  bird_87a95c8b::table_2   raw headers [GasStationID, StationID, Value]
#   GasStationID holds {"ChainID", "Country", "Segment"} — those ARE the target columns.
# MOTIVATION  A melted table stores the schema as data. Its attribute column's distinct values
#   are exactly the header row of the prepared table, so Pivot spreads them back.
def _detect_attribute_like(df: pd.DataFrame):
    out = []
    for c in list(df.columns)[:200]:
        s = _col(df, c).dropna().astype(str)
        if len(s) == 0:
            continue
        # identifier-ish, low cardinality: looks like a set of field names, not free text
        if 1 < s.nunique() <= 30 and s.str.len().max() <= 40 and \
           s.str.fullmatch(r"[A-Za-z][A-Za-z0-9_ .-]*").mean() > 0.8:
            out.append({"column": str(c),
                        "distinct_values": [_short(v, 80) for v in sorted(s.unique())[:20]]})
    if not out:
        return None
    # a column literally named "attribute"/"field"/... is the most likely one; show it first
    out.sort(key=lambda a: (0 if str(a["column"]).lower() in
                            {"attribute", "field", "property", "key", "name"} else 1,
                            len(a["distinct_values"])))
    return out[:8]


# ---- (b) packed cells -> SplitColumn --------------------------------------------------------
# EXAMPLE  bird_058b8e3b::table_2   set_info = "ALA|<non-latin name>"  ->  setCode + translation
#   Neither target name exists anywhere in the data; only the values do.
# MOTIVATION  This is the one detector whose output names must be INVENTED — the evidence can
#   only say "there are N fields in here".
# KNOWN FAILURE  The `n.nunique() <= 2` guard is meant to require a stable field count, but a
#   uuid ("95b622b4-8e91-59de-99b2-503c52b4d4ed") splits into a constant 5 parts on "-" and is
#   flagged. Over-splitting uuid/time columns was the largest single source of lost tasks in our
#   error analysis, so the excluded-pattern list below matters more than it looks.
_DATETIME = re.compile(r"^\s*\d{1,4}[-/.]\d{1,2}([-/.]\d{1,4})?([ T]\d{1,2}:\d{2}(:\d{2})?(\.\d+)?)?\s*$")
_URLISH = re.compile(r"https?://|www\.|/\S+/", re.I)


def _detect_packed(df: pd.DataFrame):
    out = []
    for c in list(df.columns)[:200]:
        s = _col(df, c).dropna().astype(str).head(60)
        if len(s) == 0:
            continue
        # a single semantic value that merely CONTAINS a delimiter is not a packed record
        if s.str.match(_DATETIME).mean() > 0.6 or s.str.contains(_URLISH).mean() > 0.5:
            continue
        for d in ("|", ",", "/", ":", "_", "-"):
            n = s.str.split(re.escape(d)).str.len()
            if (n > 1).mean() > 0.8 and n.nunique() <= 2:
                out.append({"column": str(c), "delimiter": d, "parts": int(n.mode().iloc[0]),
                            "sample": _short(s.iloc[0], 240)})
                break
    return out or None


# ---- (c) wide column group -> WideToLong / Stack --------------------------------------------
# EXAMPLE  bird_232def1d::table_2   headers [id, sts_brawl, sts_commander, ..., uid_brawl, ...]
#   The stubs `sts` and `uid` survive folding; brawl/commander/... are one variable's values.
# MOTIVATION  A wide table stores a variable's values in the header row. Folding restores the
#   stub as a column plus one column holding the variable.
def _detect_wide_groups(df: pd.DataFrame):
    groups: dict[str, list[str]] = {}
    for c in list(df.columns)[:200]:
        m = re.match(r"^(.*?)[_\- ]?(\d{2,4}|[A-Za-z]+)$", str(c))
        if m and len(m.group(1)) >= 3:
            groups.setdefault(m.group(1), []).append(str(c))
    wide = {k: v for k, v in groups.items() if len(v) >= 3}
    return wide or None


# ---- (d) header-is-data -> Transpose ---------------------------------------------------------
# EXAMPLE  bird_24e90167::table_1   shape (2, 5001), headers [ID, 2110, 2110.1, 12052, ...]
#   The headers are patient ids; the real field names sit in column 0's values.
# MOTIVATION  A transposed table has the header row and the first column swapped.
def _detect_header_is_data(df: pd.DataFrame):
    cols = list(df.columns)[:200]
    numeric = sum(str(c).strip().replace(".", "", 1).isdigit() for c in cols) / max(len(cols), 1)
    return True if numeric > 0.5 else None


# ---- (e) fragmented column -> Concatenate ---------------------------------------------------
# EXAMPLE  spider_74ea5da7::table_1   headers [..., Fname_part1, Fname_part2]  ->  Fname
#   The benchmark's corruption SPLIT one field across several columns, and the prepared table is
#   expected to hold it whole again.
# WHY THIS DETECTOR EXISTS  Every other detector here points the same way — Pivot, SplitColumn,
#   WideToLong and Transpose all UNPACK something. Nothing pointed at putting a field back
#   together, and the prompt says in so many words that when no evidence fires "the raw headers
#   are already the right schema". So on these tasks the planner was told to keep the fragments,
#   and it complied — then did the concatenation in the SQL instead
#   (`SELECT T1.Fname_part1 || T1.Fname_part2 AS FirstName`). That is a defensible place to put
#   it for answering the question and the wrong place for the metric, which scores the PREPARED
#   subtables. Measured on spider: `Concatenate` is the third most common gold operation
#   (51 of 120 tasks) and those tasks score .471 against .580 for the rest.
# WHAT IT KEYS ON  Names, not values. The fragments are usually short strings with no separator,
#   which is exactly what an ordinary short text column looks like; the reliable signal is the
#   shared stem plus an ordinal or positional suffix, which is how the corruption names them.
# A part word must be a WORD, not a suffix of one. Without the separator requirement below,
# `detail` parses as `de` + `tail` and the whole group is discarded — which is exactly what
# happened to spider_1841afd2's `detail_part1`/`detail_part2` in the first version of this.
_PART_WORDS = ("prefix", "suffix", "first", "second", "third", "last", "num",
               "tens", "units", "hundreds", "left", "right", "head", "tail")
_PARTW = "|".join(_PART_WORDS)
# stem THEN part, separated:  Fname_part1, ID_Tens, IdOrder_suffix, detail_part1
_PART_TAIL = re.compile(rf"^(?P<stem>.+?)[_\-. ](?P<part>part\s*\d+|p\d+|\d+|{_PARTW})$", re.I)
# part THEN stem, separated:  First_Name, Last_Name
_PART_HEAD = re.compile(rf"^(?P<part>{_PARTW})[_\-. ](?P<stem>.+)$", re.I)
# the part word standing alone as a whole column name:  prefix, suffix
_PART_BARE = re.compile(rf"^(?P<part>{_PARTW})$", re.I)


def _split_stem(col: str):
    """(stem, part) for a fragment column, or None.

    Three shapes, in order of how unambiguous they are. `_PART_BARE` gets a synthetic stem so
    that two bare fragments in one table group together — `prefix` and `suffix` name no field
    between them, and the planner has to read the values to name the merged column.
    """
    c = str(col).strip()
    m = _PART_TAIL.match(c)
    if m:
        stem = m.group("stem").strip("_-. ")
        return (stem, m.group("part")) if len(stem) >= 2 else None
    m = _PART_HEAD.match(c)
    if m:
        stem = m.group("stem").strip("_-. ")
        return (stem, m.group("part")) if len(stem) >= 2 else None
    if _PART_BARE.match(c):
        return ("\u0000bare", c)
    return None


def _detect_split_parts(df: pd.DataFrame):
    groups: dict[str, list[str]] = {}
    for c in list(df.columns)[:200]:
        got = _split_stem(c)
        if got:
            groups.setdefault(got[0].lower(), []).append(str(c))

    out = []
    for stem, cols in groups.items():
        if len(cols) < 2:
            continue
        # A wide group is a DIFFERENT shape — one variable spread across headers, folded by
        # WideToLong — and `_detect_wide_groups` already claims 3 or more. Fragments of one
        # field come in small fixed counts, so the two are separated by arity rather than by
        # having both fire and hoping the model picks.
        if len(cols) > 4:
            continue
        samples = []
        for c in cols[:4]:
            v = _col(df, c).dropna().astype(str).head(3).tolist()
            samples.append({"column": c, "sample": [_short(x, 40) for x in v]})
        out.append({"stem": ("(unnamed)" if stem == "\u0000bare" else stem),
                    "parts": cols, "samples": samples})
    return out or None


EVIDENCE_SPECS: list[EvidenceSpec] = [
    EvidenceSpec(
        key="attribute_like_columns",
        implied_op="Pivot",
        name_source="the attribute column's VALUES",
        instruction=("the table is LONG/melted: emit the attribute column's VALUES as the target "
                     "columns, and DROP the attribute column and its paired value column."),
        detect=_detect_attribute_like,
    ),
    EvidenceSpec(
        key="packed_columns",
        implied_op="SplitColumn",
        name_source="invented — only the values exist",
        instruction=("the flagged column packs several fields into one cell: emit the SPLIT parts "
                     "as separate columns and DROP the packed column. A column NOT flagged here "
                     "is a single value — keep it whole; never split a date or a URL."),
        detect=_detect_packed,
    ),
    EvidenceSpec(
        key="wide_column_groups",
        implied_op="WideToLong / Stack",
        name_source="the shared stub",
        instruction=("a variable's values were spread across headers: emit the stub plus one "
                     "column for the variable, not the many wide columns."),
        detect=_detect_wide_groups,
    ),
    EvidenceSpec(
        key="header_is_data",
        implied_op="Transpose",
        name_source="the first column's VALUES",
        instruction=("the table is TRANSPOSED: the target columns are the VALUES of the first "
                     "column, not the numeric headers. Keep the first column's HEADER too — it "
                     "names the entity key whose values became the numeric headers."),
        detect=_detect_header_is_data,
    ),
]


# Opt-in, per benchmark. `Concatenate` was missing from the evidence set from the start, so
# EVERY number reported so far was produced without it; switching it on globally would silently
# invalidate them. It is enabled by `--concat-evidence` (or CONCAT_EVIDENCE=1) so a benchmark can
# be re-run under the new mechanism while the settled ones stay reproducible under the old.
OPTIONAL_EVIDENCE_SPECS: list[EvidenceSpec] = [
    EvidenceSpec(
        key="split_part_columns",
        implied_op="Concatenate",
        name_source="the shared stem of the fragment columns",
        instruction=("these columns are FRAGMENTS of one field, split by the benchmark's own "
                     "corruption: emit ONE column named after the shared stem, holding the parts "
                     "joined in order, and DROP the fragments. Do NOT leave the fragments in the "
                     "schema and concatenate them in the SQL — the PREPARED table is what is "
                     "compared against gold, so a concatenation deferred to the query never "
                     "appears in it."),
        detect=_detect_split_parts,
    ),
]


def active_evidence_specs() -> list[EvidenceSpec]:
    """The detectors in force for this run.

    Read at CALL time, not at import: `run.py` sets the flag after importing this module.
    """
    if os.environ.get("CONCAT_EVIDENCE") == "1":
        return EVIDENCE_SPECS + OPTIONAL_EVIDENCE_SPECS
    return EVIDENCE_SPECS


def grounding_evidence(df: pd.DataFrame) -> dict:
    """Run every detector; return only the ones that fired."""
    ev = {}
    for spec in active_evidence_specs():
        try:
            payload = spec.detect(df)
        except Exception:
            payload = None
        if payload is not None:
            ev[spec.key] = payload
    return ev


# ============================================================================================
# 2. PROMPT — generated from EVIDENCE_SPECS so the rules can never contradict the detectors
# ============================================================================================

# ============================================================================================
# 2. PROMPT
# ============================================================================================
FORMAT_EXAMPLE = """\
### Output format example
Question: Which country's gas station had the first paid customer on 2012/8/25?
table_1 columns: [TransactionID, Date, Time, CustomerID, CardID, GasStationID, ProductID, je, dj]
table_2 columns: [Attribute, StationID, Value]
  GROUNDING EVIDENCE: attribute_like_columns: Attribute -> ["ChainID","Country","Segment"]
{"tables": [
  {"logical_table": "table_1", "db_table": "transactions_1k", "create_table_sql":
   "CREATE TABLE transactions_1k (`TransactionID` INT, `Date` DATE, `Time` VARCHAR(16), `CustomerID` INT, `CardID` INT, `GasStationID` INT, `ProductID` INT, `Amount` INT, `Price` FLOAT, PRIMARY KEY (`TransactionID`));"},
  {"logical_table": "table_2", "db_table": "gasstations", "create_table_sql":
   "CREATE TABLE gasstations (`GasStationID` INT, `ChainID` INT, `Country` VARCHAR(8), `Segment` VARCHAR(32), PRIMARY KEY (`GasStationID`));"}],
 "join_edges": [{"left_table": "table_1", "left_on": "GasStationID",
                 "right_table": "table_2", "right_on": "GasStationID"}]}
Note both schemas are FULL — every column of the prepared table, not only the ones the question
mentions."""

def _evidence_rules() -> str:
    lines = [f"  - {s.key} -> {s.implied_op}: {s.instruction}" for s in active_evidence_specs()]
    return "\n".join(lines)


# The FULL-schema requirement is not stylistic: the downstream operation predictor is featurized
# on complete table schemas, so a partial schema shifts its input distribution. Kept out of the
# prompt text itself — the model only needs the instruction, not the rationale.
# What the ABSENCE of evidence is allowed to mean.
#
# The original sentence — "When no evidence fired, the raw headers are already the
# right schema" — turns a detector MISS into a positive instruction. That is only
# sound while the detectors are near-perfect, and `_detect_split_parts` is not:
# measured on the tables whose gold sequence contains Concatenate, its recall is
# 0.50, and extending its name patterns (CamelCase `FirstName`, separator-less
# `Contents1`, arbitrary suffixes over a shared stem) lifted it only to 0.53.
# Half of the cases carry NO name signal at all — `age, pilot, plane` gives no clue
# which columns merge — so the ceiling is a property of name-based detection, not
# of the patterns.
#
# The cost of that sentence is measurable end to end. Of the 59 spider tables whose
# gold sequence needs Concatenate, 15 came out of stage 3 with an EMPTY chain: the
# plan had declared the fragment columns verbatim, so the target schema equalled the
# raw headers, the completion gate reported the table already finished, and no
# operator was ever tried. Installing the gold plan drops those 15 to 1.
#
# So the fix belongs here rather than in the detector: stop asserting that silence
# means correctness, and ask the model — which sees the preview's values, and is not
# restricted to what a regex can name — to check for fragments itself.
def _no_evidence_rule() -> str:
    """REFUTED, and left here as the record of it.

    The replacement text below asked the model to look for fragment columns itself
    whenever no detector fired, on the grounds that `_detect_split_parts` recognises
    fragments by COLUMN NAME and its measured recall is 0.50. The reasoning was
    sound and the effect was not: replaying one spider forward run's chains, the
    plan produced under the new wording scored subtable .517 against .583 for the
    same configuration under the sentence it replaced — eight tasks worse, before
    any conformance pass. Inviting the model to hunt for fragments makes it merge
    columns that were already correct, and the resulting wider plans also blew up
    stage 3's search (two tasks took 40 minutes each).

    Detector silence being read as "the headers are right" is still wrong in
    principle. It is just less wrong than telling a model to go looking.
    """
    return "When no evidence fired, the raw headers are already the right schema."


def _rules() -> str:
    # Built per call, not at import: the optional detectors are switched on after this
    # module is imported, and a module-level f-string would have frozen the rule list to
    # whatever was active at import time.
    return f"""\
Rules
-----
One entry per logical table, in the given order. `create_table_sql` is the schema the table
should have AFTER preparation — NOT its current headers.

WHEN GROUNDING EVIDENCE IS PRESENT, the table is mis-shaped and its prepared schema differs from
the raw headers. Emitting the raw headers unchanged is then WRONG:
{_evidence_rules()}
{_no_evidence_rule()}

COLUMN NAMING, in priority order:
  1. The name exists in the data (a header, an attribute value, a transposed first-column value,
     or a stub) -> copy that string VERBATIM; do not re-case or paraphrase it.
  2. The name exists nowhere (e.g. a field split out of a packed cell) -> hypothesize a short
     snake_case identifier from the question's meaning and the column's role.
  3. Join keys: name each side by its OWN table's data. The two sides need NOT match — 42% of
     joins in this benchmark connect differently-named columns (`id` <- `<entity>_id`).

Also:
  - Emit each table's FULL schema, with PRIMARY KEY when identifiable.
  - Only name a column whose values you can point to in the evidence. Do not invent a column
    whose values appear nowhere.
  - join_edges: one entry per edge; both column names must appear in their create_table_sql.

Output ONE JSON object: {{"tables": [...], "join_edges": [...]}}. No prose."""


def _preview(df: pd.DataFrame, rows: int = PREVIEW_ROWS, name_cap: int = 200,
             row_cols: int = 16) -> dict:
    sub = df.iloc[:rows, :row_cols]
    return {
        "columns": [str(c) for c in df.columns][:name_cap],
        "shape": [int(df.shape[0]), int(df.shape[1])],
        "rows": [{str(c): _short(sub.iloc[i, j]) for j, c in enumerate(sub.columns)}
                 for i in range(len(sub))],
    }


# --------------------------------------------------------------------------------------------
# beaver only — offer the offline join-key predictions as candidates for `join_edges`
# --------------------------------------------------------------------------------------------
# Stage 2 invents join_edges from the previews alone, and on beaver that is the weakest link in
# the whole system: join_key_full .109-.126 against subtable_full .210-.218, joinkey coverage
# .378, and the largest single category of unmatched gold value domains is "the join key was
# never produced at all" (31.7%). Meanwhile a 1487-entry predicted key file sits next to it
# unused.
#
# Measured on the V3b selections: of the gold join edges whose two tables are both selected,
# 70% appear verbatim in that file, and restricting it to the selected tables leaves a median
# of 4 candidate pairs per task. So this is a short list that usually contains the answer —
# worth showing, not worth trusting blindly, which is why the wording below says so.
#
# Rendered in LOGICAL table ids (table_1, ...) because that is what join_edges must use;
# handing the model real warehouse names here would make it emit those instead, and
# validate_edges would drop every edge.
_PLAN_JOIN_CAP = 30


def beaver_join_candidates(tables: list[dict],
                           join_keys_path: Path,
                           profile_path: Path) -> str:
    try:
        pairs = json.loads(Path(join_keys_path).read_text())
    except Exception:
        return ""
    try:
        profile = json.loads(Path(profile_path).read_text())
    except Exception:
        profile = {}
    # real table name (no .pkl) -> logical id
    by_name = {}
    for t in tables:
        stem = str(t.get("input_file", ""))
        stem = stem[:-4] if stem.endswith(".pkl") else stem
        by_name[stem.casefold()] = t["logical_table"]
    rows = []
    for pr in pairs:
        if not (isinstance(pr, list) and len(pr) == 2):
            continue
        try:
            (lt, lc), (rt, rc) = (str(x).split(".", 1) for x in pr)
        except ValueError:
            continue
        ll, rl = by_name.get(lt.casefold()), by_name.get(rt.casefold())
        if not ll or not rl or ll == rl:
            continue
        info = profile.get(f"{lt}.{lc}|{rt}.{rc}") or profile.get(f"{rt}.{rc}|{lt}.{lc}") or {}
        rows.append((float(info.get("score") or 0.0), ll, lc, rl, rc))
    if not rows:
        return ""
    rows.sort(key=lambda r: -r[0])
    lines = [f"  - {ll}.{lc} <-> {rl}.{rc}   strength {sc:.2f}"
             for sc, ll, lc, rl, rc in rows[:_PLAN_JOIN_CAP]]
    if len(rows) > _PLAN_JOIN_CAP:
        lines.append(f"  - ...+{len(rows) - _PLAN_JOIN_CAP} weaker candidates omitted")
    return ("\nCANDIDATE JOIN KEYS (offline predictions over these same tables, strongest first).\n"
            "`strength` is computed from the DATA: how unique the parent column's values are times\n"
            "how much of the child column is contained in them. High strength means the join is\n"
            "mechanically sound, NOT that this question needs it — a warehouse shares many valid\n"
            "keys. Roughly 70% of the join edges these questions actually need appear in this list,\n"
            "so prefer a candidate over inventing an edge, but only take the ones the question\n"
            "requires, and drop any whose columns you do not also declare in create_table_sql.\n"
            "Note the column names here are the RAW ones; if you rename a key in create_table_sql,\n"
            "state the edge using your renamed column.\n" + "\n".join(lines))


def build_prompt(question: str, tables: list[dict], subquestions: dict | None = None,
                 join_candidates: str = "") -> str:
    """`tables` items: {logical_table, input_file, preview, evidence}."""
    subquestions = subquestions or {}
    parts = ["You design the TARGET schema each raw table should have after data preparation, "
             "plus the join keys connecting those prepared tables.",
             FORMAT_EXAMPLE, _rules(), "\n### Task", f"Question: {question}", "\nRaw tables:"]
    for t in tables:
        parts.append(f"\n[{t['logical_table']}] file={t['input_file']} shape={t['preview']['shape']}")
        why = subquestions.get(t["input_file"])
        if why:
            parts.append(f"  why selected: {why}")
        parts.append(f"  columns: {t['preview']['columns']}")
        parts.append(f"  sample rows: {json.dumps(t['preview']['rows'], ensure_ascii=False)}")
        if t["evidence"]:
            parts.append(f"  GROUNDING EVIDENCE: {json.dumps(t['evidence'], ensure_ascii=False)}")
    if join_candidates:
        parts.append(join_candidates)
    parts.append("\nOutput the JSON object now.")
    return "\n".join(parts)


# ============================================================================================
# 3. DETERMINISTIC POST-PROCESSING — each of these fixes a measured, systematic model error
# ============================================================================================
def _cf(x) -> str:
    return re.sub(r"[^a-z0-9]", "", str(x).lower())


def _cols_of(create_sql: str) -> list[str]:
    return re.findall(r"`([^`]+)`", create_sql or "")


def clean_table_file(name) -> str:
    """Strip a stray `file_name: ` prefix from a schema-linking entry.

    One row of the schema-linking output serialises its selection as
    "file_name: bird_3f3aba77_input_1.pkl", so the path never resolves and the task is silently
    dropped with no tables.
    """
    s = str(name).strip()
    return s.split(":", 1)[1].strip() if s.lower().startswith("file_name:") else s


def recover_join_keys(tables: list[dict], by_lt: dict) -> list[tuple[str, str]]:
    """Re-add the column-0 header of every TRANSPOSED table that the model dropped.

    In a transposed table the header of column 0 names the entity key and the remaining headers
    are that key's VALUES (`driverId | 1 | 2 | 3 ...`). The model reliably recovers the field
    names out of column 0 and then drops the key itself — that cost 7 of 50 gold join edges a
    side. Measured effect of this repair: +11 true / +2 false columns, and gold edges with both
    keys declared 24/50 -> 29/50.
    """
    added = []
    for t in tables:
        df = t.get("df")
        if df is None or not t["evidence"].get("header_is_data") or df.shape[1] == 0:
            continue
        key = str(df.columns[0]).strip()
        if not key or key.replace(".", "", 1).isdigit():
            continue
        declared = {_cf(c) for c in _cols_of((by_lt.get(t["logical_table"]) or {})
                                             .get("create_table_sql", ""))}
        if _cf(key) and _cf(key) not in declared:
            added.append((t["logical_table"], key))
    return added


def inject_columns(create_sql: str, names: list[str]) -> str:
    """Append columns just before PRIMARY KEY / the closing paren."""
    if not names or not create_sql:
        return create_sql
    add = ", ".join(f"`{n}` VARCHAR(255)" for n in names)
    m = re.search(r",?\s*PRIMARY\s+KEY\s*\(", create_sql, re.I)
    if m:
        return create_sql[:m.start()] + ", " + add + create_sql[m.start():]
    i = create_sql.rfind(")")
    return create_sql[:i] + ", " + add + create_sql[i:] if i > 0 else create_sql


def ensure_primary_key(create_sql: str) -> str:
    """Add `PRIMARY KEY (<first column>)` only when the model declared none at all.

    Not a correction of the model's choice: measured over 73 tables, the model's own PK and the
    first-declared-column rule both match gold 74.0% of the time, so overriding is a wash. This
    fills the handful of tables (2 of 91) that declare no key, since downstream join anchoring
    reads the PK out of this clause.
    """
    if not create_sql or re.search(r"PRIMARY\s+KEY", create_sql, re.I):
        return create_sql
    cols = _cols_of(create_sql)
    if not cols:
        return create_sql
    i = create_sql.rfind(")")
    return create_sql[:i] + f", PRIMARY KEY (`{cols[0]}`)" + create_sql[i:] if i > 0 else create_sql


def validate_edges(edges, by_lt: dict) -> tuple[list, list]:
    """Drop edges naming a column the spec does not declare; returns (kept, rejected).

    Such an edge cannot be materialized downstream AND displaces a real one, so dropping it
    silently is better than passing it on.
    """
    declared = {lt: {_cf(c) for c in _cols_of((g or {}).get("create_table_sql", ""))}
                for lt, g in by_lt.items()}
    kept, bad, seen = [], [], set()
    for e in edges or []:
        if not isinstance(e, dict):
            continue
        lt, rt = str(e.get("left_table") or ""), str(e.get("right_table") or "")
        lc, rc = str(e.get("left_on") or ""), str(e.get("right_on") or "")
        if not all((lt, rt, lc, rc)) or lt == rt:
            bad.append(e)
        elif _cf(lc) not in declared.get(lt, set()) or _cf(rc) not in declared.get(rt, set()):
            bad.append(e)
        else:
            key = tuple(sorted([(lt, _cf(lc)), (rt, _cf(rc))]))
            if key not in seen:
                seen.add(key)
                kept.append({"left_table": lt, "left_on": lc,
                             "right_table": rt, "right_on": rc})
    return kept, bad


# ============================================================================================
# 4. LLM CALL
# ============================================================================================
def _complete(prompt: str, model: str, temperature: float = 0.0) -> tuple[str, dict]:
    """Returns (text, usage). Usage is per call so an orchestrator can attribute
    cost to THIS stage rather than to a process-wide meter."""
    from openai import OpenAI

    kw = {} if re.match(r"^(gpt-5|o\d)", model) else {"temperature": temperature}
    t0 = time.perf_counter()
    # Timeout and retries, explicitly. OpenAI() with no arguments takes the SDK
    # defaults of timeout 600s and max_retries 2, i.e. up to 1800 seconds on one
    # call; a single hung read there once stalled a repair loop for 33 minutes.
    _to = float(os.getenv("OPENAI_REQUEST_TIMEOUT", "90"))
    r = OpenAI(timeout=_to, max_retries=2).chat.completions.create(
        model=model, messages=[{"role": "user", "content": prompt}],
        max_completion_tokens=2800, **kw)
    u = getattr(r, "usage", None)
    det = getattr(u, "prompt_tokens_details", None) if u else None
    return (r.choices[0].message.content or ""), {
        "calls": 1,
        "input": int(getattr(u, "prompt_tokens", 0) or 0),
        "output": int(getattr(u, "completion_tokens", 0) or 0),
        "cached": int(getattr(det, "cached_tokens", 0) or 0) if det else 0,
        "elapsed_seconds": time.perf_counter() - t0,
        "model": model,
    }


def _parse_json(text: str) -> dict:
    m = re.search(r"\{.*\}", text or "", re.S)
    if not m:
        return {}
    try:
        return json.loads(m.group(0))
    except Exception:
        return {}


# ============================================================================================
# 5. PUBLIC API
# ============================================================================================
def load_tables(table_files: Iterable, tables_dir: Path) -> list[dict]:
    """Read the raw tables and attach their preview + grounding evidence."""
    tables = []
    for i, f in enumerate(table_files):
        f = clean_table_file(f)
        p = Path(f) if Path(f).is_absolute() else Path(tables_dir) / f
        if not p.exists():
            continue
        df = pd.read_pickle(p)
        tables.append({"logical_table": f"table_{i + 1}", "input_file": str(f), "df": df,
                       "preview": _preview(df), "evidence": grounding_evidence(df)})
    return tables


def synthesize_schema(question: str,
                      table_files: Iterable,
                      tables_dir: Path,
                      *,
                      subquestions: dict | None = None,
                      model: str = "gpt-4o-2024-08-06",
                      temperature: float = 0.0,
                      key_recovery: bool = True,
                      is_warehouse: bool = False,
                      join_keys_path: Path | None = None,
                      join_profile_path: Path | None = None,
                      return_prompt: bool = False) -> dict:
    """Question + selected tables -> relational schema.

        schema["tables"]      [{logical_table, input_file, db_table, create_table_sql}, ...]
        schema["join_edges"]  [{left_table, left_on, right_table, right_on}, ...]

    `table_files` may be collection-relative names or absolute paths.
    """
    tables = load_tables(table_files, tables_dir)
    if not tables:
        return {"tables": [], "join_edges": [], "error": "no readable input tables"}

    # Warehouse collections get the offline join-key predictions as candidates:
    # inventing edges from previews alone is the weakest link there.
    jc = ""
    if is_warehouse and join_keys_path:
        jc = beaver_join_candidates(tables, join_keys_path,
                                    join_profile_path or Path("/nonexistent"))

    prompt = build_prompt(question, tables, subquestions, join_candidates=jc)
    usage = {"calls": 0, "input": 0, "output": 0, "cached": 0,
             "elapsed_seconds": 0.0, "model": model}
    try:
        text, usage = _complete(prompt, model, temperature)
        data = _parse_json(text)
    except Exception as exc:  # noqa: BLE001
        data = {"error": f"{type(exc).__name__}: {exc}"}

    # "tables" is this module's key; accept the old "gold_tables" too, so a
    # model that echoes the older format is not silently dropped.
    declared = data.get("tables") or data.get("gold_tables") or []
    by_lt = {str(g.get("logical_table")): g for g in declared}

    recovered = recover_join_keys(tables, by_lt) if key_recovery else []
    for lt, name in recovered:
        g = by_lt.setdefault(lt, {})
        g["create_table_sql"] = inject_columns(g.get("create_table_sql", ""), [name])
    for g in by_lt.values():
        if isinstance(g, dict) and g.get("create_table_sql"):
            g["create_table_sql"] = ensure_primary_key(g["create_table_sql"])
    edges, rejected = validate_edges(data.get("join_edges"), by_lt)

    schema = {
        "question": question,
        "input_tables": [t["input_file"] for t in tables],
        "join_edges": edges,
        "tables": [{
            "logical_table": t["logical_table"],
            "input_file": t["input_file"],
            "db_table": (by_lt.get(t["logical_table"], {}).get("db_table") or t["logical_table"]),
            "create_table_sql": by_lt.get(t["logical_table"], {}).get("create_table_sql", ""),
        } for t in tables],
        "_recovered_columns": [f"{lt}.{n}" for lt, n in recovered],
        "_rejected_edges": rejected,
        "usage": usage,
    }
    if "error" in data:
        schema["error"] = data["error"]
    if return_prompt:
        schema["_prompt"] = prompt
    return schema


# ============================================================================================
# 6. CLI — batch over a dataset's table-selection output
# ============================================================================================
def default_selection_path(dataset: str) -> Path:
    return P.resolve(dataset, module="table_discovery",
                     group="selection").out("table_selection.jsonl")


def default_schema_path(dataset: str) -> Path:
    return P.resolve(dataset, module="pipeline_synthesize",
                     group="schema").out("relational_schema.jsonl")


def run_dataset(dataset: str, out_path: Path, selection_path: Path | None = None,
                model: str = "gpt-4o-2024-08-06", limit: int = 0,
                task_ids: list[str] | None = None, overwrite: bool = False) -> Path:
    """Synthesize a relational schema for every task selection, one record each.

    The output file is the cache: a task already present is skipped, so an
    interrupted run resumes without paying twice.
    """
    ds = DS.resolve(dataset)
    selection_path = Path(selection_path or default_selection_path(dataset))
    selections = load_jsonl(selection_path)
    if not selections:
        raise FileNotFoundError(
            f"no table selections at {selection_path}. Run "
            f"table_discovery.table_selection --dataset {dataset} first.")

    if task_ids:
        wanted = set(task_ids)
        selections = [s for s in selections if str(s.get("task_id")) in wanted]

    is_warehouse = DS.SOURCE_NAME.get(dataset, dataset) == "beaver"
    join_keys_path = (P.resolve(dataset, module="table_discovery",
                                group="offline_online").out_dir
                      / "dw_join_keys_g_domain.json") if is_warehouse else None

    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    if overwrite and out_path.exists():
        out_path.unlink()

    done = load_jsonl_by_key(out_path, "task_id")
    pending = [s for s in selections if str(s.get("task_id")) not in done]
    if limit and limit > 0:
        pending = pending[:limit]

    print(f"[schema] dataset={dataset} warehouse={is_warehouse}")
    print(f"[schema] selections: {selection_path} ({len(selections)})")
    print(f"[schema] cached={len(done)} to_process={len(pending)}")
    print(f"[schema] output:     {out_path}")

    written = 0
    for sel in tqdm(pending, desc="Relational schema"):
        selected = list(sel.get("selected_tables") or [])
        if not selected:
            print(f"[schema] task {sel.get('task_id')}: no selected tables, skipped")
            continue
        rec = synthesize_schema(
            question=sel.get("question", ""),
            table_files=selected,
            tables_dir=ds.input_tables,
            subquestions=sel.get("subquestions") or {},
            model=model,
            is_warehouse=is_warehouse,
            join_keys_path=join_keys_path,
        )
        rec["task_id"] = str(sel.get("task_id"))
        append_jsonl(out_path, rec)
        written += 1

    print(f"[schema] wrote {written} records")
    return out_path


def parse_args():
    ap = argparse.ArgumentParser(
        description="Stage 1: synthesize the relational schema for each task.")
    ap.add_argument("--dataset", type=str, default="Synth-Bird")
    ap.add_argument("--selection", type=Path, default=None,
                    help="Override the table_selection.jsonl input.")
    ap.add_argument("--out", type=Path, default=None,
                    help="Override the output JSONL.")
    ap.add_argument("--model", type=str, default="gpt-4o-2024-08-06")
    ap.add_argument("--limit", type=int, default=0,
                    help="Process at most N not-yet-done tasks (0 = all).")
    ap.add_argument("--task-ids", type=str, nargs="+", default=None)
    ap.add_argument("--overwrite", action="store_true")
    return ap.parse_args()


if __name__ == "__main__":
    a = parse_args()
    run_dataset(a.dataset, a.out or default_schema_path(a.dataset),
                selection_path=a.selection, model=a.model, limit=a.limit,
                task_ids=a.task_ids, overwrite=a.overwrite)
