#!/usr/bin/env python3
"""
evidence_text.py
================
One grammar for every table-like object in an execution state, so a SHARED
encoder sees one dialect instead of three.

    from evidence_text import build_evidence, joinkey_features, SPECIAL_TOKENS

WHY A SINGLE GRAMMAR
--------------------
The first serialisation rendered raw and produced tables as a column profile and
the relational plan as CREATE TABLE DDL. One encoder, run three times with shared
weights, then had to digest two unrelated dialects for the same underlying
object. Everything is emitted here in the same shape, with `role` as the only
distinguishing mark, so what the encoder learns about "a column and its value
domain" transfers between the three passes:

    [TABLE] name=... role=selected|rejected|declared|produced rows=... cols=...
    [COL] name=... type=... distinct=... unique=... nonnull=... values= v1 ; v2
    [JOIN] left=t1.c1 right=t2.c2

A declared table has no materialised values, so its statistic slots read `na`.
That is a real difference between a declaration and a result, and it is the one
difference the grammar keeps.

WHY QUESTION AND EVIDENCE ARE RETURNED SEPARATELY
-------------------------------------------------
`build_evidence` returns the question and each evidence block as separate
strings. Sentence-pair classification — `[CLS] question [SEP] evidence [SEP]` —
is the format these encoders are pretrained and fine-tuned in, and the collator
needs the two halves apart to build it. Concatenating them here would also repeat
the earlier mistake in a new place: with a FROZEN embedding model, putting the
question in the same string as the tables dropped `revise_table` detection from
0.927 to 0.590, because a single pooled vector dilutes rather than aligns. A
cross-encoder with a task head is the architecture that can use the pairing; a
bi-encoder cannot, and this file has to serve both.

WHY COLUMN-MAJOR
----------------
`score_task` matches produced columns to gold columns by VALUE DOMAIN, one to
one, and is invariant to row order. A row-major sample shows the first few rows
of every column; what decides the metric is each column's domain. So one line per
column, with distinct values sampled from that column.

TRUNCATION IS BY ROLE, NOT BY TAIL
----------------------------------
Rejected tables are the strongest single evidence there is — embedded alone they
reach 0.945 on `revise_table` — and they are emitted last. Cutting the string at
a character cap therefore removed exactly the signal the bundle exists to carry;
46% of dev states were truncated that way. Budget is allocated per role, then
round-robin across the tables of a role, then across the columns of a table.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

SPECIAL_TOKENS = ["[TABLE]", "[COL]", "[JOIN]", "[Q]"]
ROLES = ("selected", "rejected", "declared", "produced")
_CF = lambda c: re.sub(r"[^a-z0-9]", "", str(c).strip().lower())      # noqa: E731

# Characters, not tokens: the caller cannot tokenise here without pinning a
# tokenizer, and table text runs ~3.5 chars/token in practice. Measured on
# nl2sql-bird dev, these give median 1686 / 222 / 770 tokens per bundle.
DEFAULT_BUDGET = {"ev_selected_rejected": 12000, "ev_declared": 3000,
                  "ev_produced": 8000}


# --------------------------------------------------------------------------- #
def _col_line(col, name: str, n_vals: int, width: int) -> str:
    """One column: profile then sampled distinct values.

    `distinct` and `nonnull` are DESCRIPTION, of the kind any data dictionary
    carries for any table, not diagnosis. They are here because a handful of
    sampled values cannot reveal that a column holds 551 distinct values or 40%
    nulls, and those are the properties a wrong pipeline shows up in.
    """
    n = len(col)
    try:
        nd = int(col.nunique(dropna=True))
    except TypeError:                       # a cell holding a list is unhashable
        nd = int(col.dropna().astype(str).nunique())
    nn = float(col.notna().mean()) if n else 0.0
    vals, seen = [], set()
    for v in col.dropna().astype(str).head(300).tolist():
        s = re.sub(r"\s+", " ", v).strip()[:40]
        if s and s not in seen:
            seen.add(s)
            vals.append(s)
        if len(vals) >= n_vals:
            break
    line = (f"[COL] name={name} type={col.dtype} distinct={nd} "
            f"unique={nd / max(n, 1):.2f} nonnull={nn:.2f} values= "
            + " ; ".join(vals))
    return line[:width]


def render_table(df, name: str, role: str, budget: int,
                 max_cols: int = 40, n_vals: int = 6) -> str:
    """A materialised table under the shared grammar, inside `budget` chars.

    Columns are emitted round-robin under the budget rather than in order, so a
    wide table does not spend everything on its first few columns.
    """
    head = (f"[TABLE] name={name} role={role} "
            f"rows={df.shape[0]} cols={df.shape[1]}")
    cols = list(df.columns)[:max_cols]
    if not cols:
        return head
    per = max((budget - len(head)) // max(len(cols), 1), 60)
    out = [head]
    used = len(head)
    for c in cols:
        s = df[c]
        if hasattr(s, "columns"):
            s = s.iloc[:, 0]
        line = _col_line(s, str(c), n_vals, per)
        if used + len(line) + 1 > budget:
            break
        out.append(line)
        used += len(line) + 1
    return "\n".join(out)


def render_declared(spec: Dict[str, Any], budget: int) -> str:
    """A plan's declared table, in the same grammar with `na` statistics."""
    lt = spec.get("logical_table")
    sql = spec.get("create_table_sql") or ""
    ct = spec.get("column_types")
    if isinstance(ct, dict) and ct:
        cols = [(c, str(t)) for c, t in ct.items()]
    else:
        cols = [(c, "") for c in re.findall(r"`([^`]+)`", sql)]
        types = re.findall(r"`[^`]+`\s+([A-Za-z]+(?:\([^)]*\))?)", sql)
        cols = [(c, types[i] if i < len(types) else "") for i, (c, _) in enumerate(cols)]
    pk = re.search(r"PRIMARY\s+KEY\s*\(([^)]*)\)", sql, re.I)
    pkset = {_CF(x) for x in re.findall(r"`?([^`,\s]+)`?", pk.group(1))} if pk else set()
    out = [f"[TABLE] name={lt} role=declared source={spec.get('input_file')} "
           f"rows=na cols={len(cols)}"]
    used = len(out[0])
    for c, t in cols:
        line = (f"[COL] name={c} type={t or 'na'} distinct=na unique=na "
                f"nonnull=na key={'yes' if _CF(c) in pkset else 'no'} values= na")
        if used + len(line) + 1 > budget:
            break
        out.append(line)
        used += len(line) + 1
    return "\n".join(out)


def render_joins(edges: Sequence[dict]) -> str:
    return "\n".join(
        f"[JOIN] left={e.get('left_table')}.{e.get('left_on')} "
        f"right={e.get('right_table')}.{e.get('right_on')}"
        for e in (edges or []))


def _blocks(items, budget: int, fn) -> str:
    """Split a budget evenly across items, then let each render inside its share."""
    if not items:
        return "(none)"
    per = max(budget // len(items), 200)
    return "\n".join(fn(x, per) for x in items)


def build_evidence(task, link, plan, shard, bench_dir: Path,
                   budget: Optional[Dict[str, int]] = None,
                   max_cols: int = 40, n_vals: int = 6) -> Dict[str, Any]:
    """The question and three evidence blocks, plus what was truncated.

    Returns question / ev_1 / ev_2 / ev_3 separately; the collator pairs them.
    `trunc_*` is reported so a weak result can be checked against how much of the
    evidence actually reached the encoder, rather than guessed at.
    """
    import pandas as pd
    B = {**DEFAULT_BUDGET, **(budget or {})}

    def load(f):
        p = bench_dir / f
        try:
            return pd.read_pickle(p) if p.exists() else None
        except Exception:
            return None

    # The candidate POOL, not input_table. `selected_tables` is chosen from
    # whatever prep_utils.schema.selected_tables_for_task offers, which is
    # `retrieved_table` when the benchmark ships one. Deriving the rejected set
    # from input_table therefore showed the model a set that is not what the
    # linker rejected: on beaver the two overlap by a median 0.60, and in 57 of
    # 119 tasks a gold table lives only in retrieved_table — so the single
    # strongest piece of evidence for `revise_table` could not appear in ev_1 at
    # all. The remote localizer predicted revise_table for 1 of 119 beaver tasks
    # against 93 true, and for 0 of the 49 where a better table was available.
    # bird/spider carry no retrieved_table, so this is identical there.
    files = list(task.get("retrieved_table") or task.get("input_table") or [])
    sel = [f for f in (link.get("selected_tables") or [])]
    unsel = [f for f in files if f not in set(sel)]

    # Half the budget to each role. Rejected tables carry the strongest single
    # signal for `revise_table`, so they get an equal share by construction
    # rather than whatever is left over.
    half = B["ev_selected_rejected"] // 2
    sel_df = [(f, load(f)) for f in sel]
    uns_df = [(f, load(f)) for f in unsel]
    sel_df = [(f, d) for f, d in sel_df if d is not None]
    uns_df = [(f, d) for f, d in uns_df if d is not None]
    ev1 = (_blocks(sel_df, half, lambda x, p: render_table(x[1], x[0], "selected", p, max_cols, n_vals))
           + "\n" +
           _blocks(uns_df, half, lambda x, p: render_table(x[1], x[0], "rejected", p, max_cols, n_vals)))

    specs = list(plan.get("gold_tables") or plan.get("tables") or [])
    ev2 = _blocks(specs, B["ev_declared"], lambda s, p: render_declared(s, p))
    j = render_joins(plan.get("join_edges"))
    if j:
        ev2 += "\n" + j

    subs = list((shard or {}).get("subtables", {}).items())
    ev3 = _blocks(subs, B["ev_produced"],
                  lambda x, p: render_table(x[1], x[0], "produced", p, max_cols, n_vals))
    j3 = render_joins((shard or {}).get("edges"))
    if j3:
        ev3 += "\n" + j3

    # The ORDER tables are emitted in, so a per-table head can align its
    # segments with per-table labels. `[TABLE]` is an added token, so the
    # segment boundaries are findable in input_ids directly; what cannot be
    # recovered from the text alone is which file each block came from, and
    # therefore whether it was one of the gold tables.
    #
    # `_blocks` truncates to a character budget, so the list is filtered to the
    # blocks that actually survived into ev1. A silent mismatch here would pair
    # table k's representation with table k+1's label.
    tables_1 = ([{"name": f, "role": "selected"} for f, _ in sel_df
                 if f"name={f}" in ev1]
                + [{"name": f, "role": "rejected"} for f, _ in uns_df
                   if f"name={f}" in ev1])
    return {"question": task.get("question", ""),
            "ev_1": ev1, "ev_2": ev2, "ev_3": ev3, "tables_1": tables_1,
            "n_selected": len(sel), "n_rejected": len(unsel),
            "trunc_1": int(len(ev1) >= B["ev_selected_rejected"] * 0.98),
            "trunc_2": int(len(ev2) >= B["ev_declared"] * 0.98),
            "trunc_3": int(len(ev3) >= B["ev_produced"] * 0.98)}


# --------------------------------------------------------------------------- #
# numeric channel
# --------------------------------------------------------------------------- #
JK_NAMES = ("jk_containment", "jk_jaccard", "jk_yield", "jk_fanout",
            "jk_left_unique", "jk_right_unique", "jk_left_nonnull",
            "jk_right_nonnull", "jk_present")


def _key_series(df, on):
    m = {_CF(c): c for c in df.columns}
    real = m.get(_CF(on))
    if real is None:
        return None
    s = df[real]
    return s.iloc[:, 0] if hasattr(s, "columns") else s


def _canon_keys(ls, rs):
    """Both key columns in ONE comparable form before the set arithmetic.

    `astype(str)` on its own is wrong whenever the two sides carry the same
    surrogate key at different dtypes: a float64 column renders 13.0 and an int64
    column renders 13, the string sets never intersect, and every ratio reports
    0 for a join that is in fact perfect. On nl2sql-bird dev this hit 11 of the
    133 tasks that declare an edge, and it was visible from the outside — an LLM
    reading these same numbers wrote "join keys mismatch types (int vs float)"
    for four of them and routed them to `revise_pipeline`.

    Numeric coercion is applied only when BOTH sides are almost entirely
    coercible AND coercion preserves the number of distinct values on both
    sides. That guard matters: zero-padded identifiers ("007") and codes that
    happen to look numeric would otherwise be silently collapsed, turning a
    formatting fix into a data corruption.
    """
    import pandas as pd
    a, b = ls.dropna(), rs.dropna()
    na, nb = pd.to_numeric(a, errors="coerce"), pd.to_numeric(b, errors="coerce")
    if (len(a) and len(b)
            and na.notna().mean() >= 0.9 and nb.notna().mean() >= 0.9
            and na.dropna().nunique() == a.astype(str).nunique()
            and nb.dropna().nunique() == b.astype(str).nunique()):
        return na.dropna(), nb.dropna()
    return a.astype(str).str.strip(), b.astype(str).str.strip()


def joinkey_features(shard) -> Dict[str, float]:
    """Nine set statistics of the declared join edges, aggregated by MIN.

    Numbers rather than text because join keys are frequently integer
    surrogates: `12345 | 67890` carries no semantics for a text encoder, and the
    text-only arm scores 0.542 on `revise_pipeline` — chance — where these reach
    0.682. Ratios only: splitting the 86 hand features into scale-dependent
    counts and scale-free ratios gave train-vs-dev domain AUC 0.948 for the
    counts against 0.849 for the ratios, with the counts contributing nothing to
    the decision.

    MIN and not mean: the two agree on 84-100% of tasks because most declare a
    single edge, and carrying both measured WORSE than min alone (0.666 vs 0.682
    on `revise_pipeline`) for twice the width. The weakest edge is what breaks a
    join, so min is also the right summary on its own terms.
    """
    subs = (shard or {}).get("subtables") or {}
    per: List[Dict[str, float]] = []
    for e in (shard or {}).get("edges") or []:
        L, R = subs.get(e.get("left_table")), subs.get(e.get("right_table"))
        if L is None or R is None:
            continue
        ls, rs = _key_series(L, e.get("left_on")), _key_series(R, e.get("right_on"))
        if ls is None or rs is None:
            per.append({n: 0.0 for n in JK_NAMES})
            continue
        lv, rv = _canon_keys(ls, rs)
        ln, rn = set(lv), set(rv)
        inter, union = len(ln & rn), len(ln | rn) or 1
        rc = rv.value_counts()
        fan = float(rc.reindex(list(ln & rn)).mean()) if inter else 0.0
        per.append({
            "jk_containment": inter / max(min(len(ln), len(rn)), 1),
            "jk_jaccard": inter / union,
            "jk_yield": float(lv.isin(rn).mean()) if len(lv) else 0.0,
            "jk_fanout": fan / max(len(rv), 1) * max(len(rn), 1),
            "jk_left_unique": len(ln) / max(len(lv), 1),
            "jk_right_unique": len(rn) / max(len(rv), 1),
            "jk_left_nonnull": float(ls.notna().mean()) if len(ls) else 0.0,
            "jk_right_nonnull": float(rs.notna().mean()) if len(rs) else 0.0,
            "jk_present": 1.0,
        })
    # A task with no edges is a real state, not missing data: single-table tasks
    # exist and `join_key_full` is correctly None for them. Zeros say "no join
    # evidence", which is what the numeric channel should report.
    return {n: (float(min(p[n] for p in per)) if per else 0.0) for n in JK_NAMES}
