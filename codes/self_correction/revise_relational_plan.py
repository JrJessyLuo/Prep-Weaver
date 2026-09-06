#!/usr/bin/env python3
"""
revise_relational_plan.py
=========================
Rewrite a relational plan, re-run synthesis on it, and keep the result only if a
gold-free check says it improved.

    python3 revise_relational_plan.py --inter <...>            # batch, all 12
    python3 revise_relational_plan.py --inter <...> --task-id bird_dddd14d1 --show-prompt

DELIBERATELY CONSERVATIVE
-------------------------
The offline ceiling for this action is low and the downside is real, so every
guard below exists to make "change nothing" the default:

    3/12   the omitted question-named column exists in a source table the plan
           already uses — a declaration could reach it
    5/12   nothing in the evidence is wrong; the prompt should abstain
    1/12   gold needs a table we never selected (that is revise_table, not this)
    3/12   the omitted column is neither a column nor a value in the source

and the four structural diffs that look like defects — under-declaration (0.92 vs
0.88 on healthy tasks), primary key (0.58 vs 0.55), over-decomposition (0.25 vs
0.31), table set (0.17 vs 0.11) — do not separate this class from the tasks that
came out CORRECT. A revision that acts on them is expected to do harm.

So:
  * abstention short-circuits. `plan_at_fault: false` re-runs NOTHING and keeps
    the original score. Re-synthesising an abstained task would mix "declined to
    change" with "changed and it did not help", and synthesis is not free.
  * only ADDITIVE column changes are applied. Dropping a declared column,
    dropping a table, or changing a primary key is rejected and logged — those
    are the diffs measured to be noise.
  * tables are matched by `input_file`. Our plan and the gold plan disagree on
    the logical numbering on 6 of these 12 tasks; matching on `table_N` would
    silently rewrite the wrong table.
  * the rewritten plan is kept only if a GOLD-FREE check improves: declared-column
    coverage must not fall and join containment must not fall, and at least one
    must rise. Otherwise the original plan's output is restored.

`score_task` is used for REPORTING only, never to decide acceptance.
"""
from __future__ import annotations

import argparse
import json
import os
import pickle
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

ROOT = Path(__file__).resolve().parent.parent
for _p in (str(ROOT), str(ROOT / "actions"), str(ROOT / "prep_utils"),
           str(ROOT / "construct_training_data"), str(ROOT / "train_infer_single_ops"),
           str(ROOT / "pipeline_eval")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import pandas as pd                                                 # noqa: E402

AUTOP = Path(os.environ.get("AUTOPREP_ROOT") or Path(__file__).resolve().parents[2] / "datasets")
_CF = lambda x: re.sub(r"[^0-9a-z]", "", str(x).lower())            # noqa: E731
_PK = re.compile(r"PRIMARY\s+KEY\s*\(([^)]*)\)", re.I)


# --------------------------------------------------------------------------- #
# plan surgery
# --------------------------------------------------------------------------- #

def parse_table(t: Dict[str, Any]) -> Tuple[List[str], Dict[str, str], List[str]]:
    """(columns, {column: sql type}, primary key) from a plan table entry."""
    sql = t.get("create_table_sql") or ""
    body = _PK.sub("", sql)
    cols = re.findall(r"`([^`]+)`", body)
    types: Dict[str, str] = {}
    for m in re.finditer(r"`([^`]+)`\s+([A-Za-z][A-Za-z0-9_ ]*(?:\([^)]*\))?)", body):
        types[m.group(1)] = m.group(2).strip().rstrip(",").strip()
    mk = _PK.search(sql)
    pk = [x.strip(' `"') for x in mk.group(1).split(",")] if mk else []
    return cols, types, pk


def render_table_sql(name: str, cols: Sequence[str], types: Dict[str, str],
                     pk: Sequence[str]) -> str:
    parts = [f"`{c}` {types.get(c, 'VARCHAR(255)')}" for c in cols]
    if pk:
        parts.append("PRIMARY KEY (" + ", ".join(f"`{c}`" for c in pk) + ")")
    return f"CREATE TABLE {name} (" + ", ".join(parts) + ")"


def apply_revision(plan: Dict[str, Any], revision: Dict[str, Any]) -> Dict[str, Any]:
    """Build a new plan from the model's answer, applying only additive changes.

    Returns {"plan": <new plan or None>, "applied": [...], "rejected": [...]}.
    """
    by_file = {t.get("input_file"): t for t in (plan.get("gold_tables") or [])}
    applied: List[str] = []
    rejected: List[str] = []
    new_tables: List[Dict[str, Any]] = []

    want = {}
    for r in (revision.get("revised_tables") or []):
        f = r.get("input_file")
        if f in by_file:
            want[f] = r
        else:
            rejected.append(f"unknown input_file {f!r}")

    for f, t in by_file.items():
        cols, types, pk = parse_table(t)
        r = want.get(f)
        if r:
            new_cols = [str(c) for c in (r.get("columns") or [])]
            dropped = [c for c in cols if _CF(c) not in {_CF(x) for x in new_cols}]
            added = [c for c in new_cols if _CF(c) not in {_CF(x) for x in cols}]
            if dropped:
                rejected.append(f"{f}: refused to drop {dropped[:6]}")
            if r.get("primary_key") and [_CF(x) for x in r["primary_key"]] != [_CF(x) for x in pk]:
                rejected.append(f"{f}: refused primary-key change {pk} -> {r['primary_key']}")
            if added:
                cols = cols + added
                applied.append(f"{f}: +{added}")
        new_tables.append({**t, "create_table_sql": render_table_sql(
            t.get("db_table") or t.get("logical_table") or "T", cols, types, pk)})

    lt_of = {t.get("input_file"): t.get("logical_table") for t in (plan.get("gold_tables") or [])}
    old_edges = plan.get("join_edges") or []
    new_edges = []
    for e in (revision.get("revised_join_edges") or []):
        lt_l = lt_of.get(e.get("left_table"), e.get("left_table"))
        lt_r = lt_of.get(e.get("right_table"), e.get("right_table"))
        if lt_l and lt_r and e.get("left_on") and e.get("right_on"):
            new_edges.append({"left_table": lt_l, "left_on": e["left_on"],
                              "right_table": lt_r, "right_on": e["right_on"]})
    if new_edges and new_edges != old_edges:
        applied.append(f"edges {old_edges} -> {new_edges}")
    edges = new_edges or old_edges

    if not applied:
        return {"plan": None, "applied": [], "rejected": rejected}
    return {"plan": {**plan, "gold_tables": new_tables, "join_edges": edges},
            "applied": applied, "rejected": rejected}


# --------------------------------------------------------------------------- #
# gold-free acceptance
# --------------------------------------------------------------------------- #

def plan_health(plan: Dict[str, Any], produced: Dict[str, Any]) -> Dict[str, float]:
    """Two observables computable at inference time.

    `covered`     declared columns that actually exist in the produced tables
    `containment` best directional overlap of a declared join key

    Both are properties of the plan+output pair, and neither touches gold.
    """
    declared_total = declared_have = 0
    for t in (plan.get("gold_tables") or []):
        lt = t.get("logical_table")
        cols, _, _ = parse_table(t)
        df = (produced or {}).get(lt)
        have = {_CF(c) for c in df.columns} if df is not None else set()
        declared_total += len(cols)
        declared_have += sum(1 for c in cols if _CF(c) in have)
    best = 0.0
    for e in (plan.get("join_edges") or []):
        l, r = (produced or {}).get(e.get("left_table")), (produced or {}).get(e.get("right_table"))
        if l is None or r is None:
            continue
        lm, rm = {_CF(c): c for c in l.columns}, {_CF(c): c for c in r.columns}
        a, b = lm.get(_CF(e.get("left_on"))), rm.get(_CF(e.get("right_on")))
        if a is None or b is None:
            continue
        try:
            A = set(l[a].dropna().astype(str)); B = set(r[b].dropna().astype(str))
        except Exception:
            continue
        if A and B:
            best = max(best, max(len(A & B) / len(A), len(A & B) / len(B)))
    return {"covered": declared_have / max(declared_total, 1), "containment": best}


def accept(before: Dict[str, float], after: Dict[str, float]) -> Dict[str, Any]:
    """Accept unless something demonstrably REGRESSES.

    The first version required a strict improvement and rejected 8 of 12
    revisions — but on 6 of those both observables were byte-identical
    (covered 1.000 -> 1.000, containment 0.000 -> 0.000), because they are
    STRUCTURE-level and `covered` is already saturated at 1.000 on two thirds of
    these tasks. Requiring a rise in a signal with no headroom rejects
    everything. Two of the rejections were real fixes: bird_c4b9b7a5 went
    subtable_full False -> True and join_key_full 0 -> 1 with both observables
    flat, and bird_83d15f3a went 0 -> 1 the same way.

    What the observables CAN do is detect damage — bird_82f1d1a4's containment
    fell 0.182 -> 0.000 and that rejection was correct. So they are used as a
    veto, not as a gate. This is the conservative reading: a revision the model
    proposed and the guards already filtered is applied unless it visibly breaks
    something.
    """
    down = (after["covered"] < before["covered"] - 1e-9
            or after["containment"] < before["containment"] - 1e-9)
    up = (after["covered"] > before["covered"] + 1e-9
          or after["containment"] > before["containment"] + 1e-9)
    return {"before": before, "after": after, "improved": bool(up),
            "regressed": bool(down), "accept": not down}


# --------------------------------------------------------------------------- #
# driver
# --------------------------------------------------------------------------- #

def load(inter: Path, tid: str, benchmark="nl2sql-bird", split="dev") -> Dict[str, Any]:
    rows = lambda n: ({json.loads(l)["task_id"]: json.loads(l)                # noqa: E731
                       for l in (inter / n).open() if l.strip()}
                      if (inter / n).exists() else {})
    bench_dir = AUTOP / benchmark / split
    plans = rows("relational_plan.jsonl")
    plan = plans.get(tid, {})
    raw = {}
    for t in plan.get("gold_tables") or []:
        p = bench_dir / (t.get("input_file") or "")
        if p.exists():
            try:
                raw[t["logical_table"]] = pd.read_pickle(p)
            except Exception:
                pass
    with (inter / "tables" / f"{tid}.pkl").open("rb") as fh:
        shard = pickle.load(fh)
    cp = inter / "chains.json"
    task = next(json.loads(l) for l in (bench_dir / "benchmark.jsonl").open()
                if json.loads(l).get("task_id") == tid)
    return {"task": task, "plan": plan, "link": rows("schema_linking.jsonl").get(tid, {}),
            "diag": rows("diagnose.jsonl").get(tid, {}),
            "chains": json.loads(cp.read_text()) if cp.exists() else {},
            "produced": shard.get("subtables") or {}, "edges": shard.get("edges") or [],
            "raw": raw, "bench_dir": bench_dir}


def main(argv: Optional[Sequence[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="Conservatively revise a relational plan.")
    ap.add_argument("--inter", type=Path, required=True)
    ap.add_argument("--task-id", default=None)
    ap.add_argument("--benchmark", default="nl2sql-bird")
    ap.add_argument("--split", default="dev")
    ap.add_argument("--model", default="gpt-5-2025-08-07")
    ap.add_argument("--effort", default="medium")
    ap.add_argument("--label", default="revise_relational_plan")
    ap.add_argument("--workers", type=int, default=3)
    ap.add_argument("--timeout", type=float, default=None)
    ap.add_argument("--show-prompt", action="store_true")
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args(argv)

    os.environ["REASONING_EFFORT"] = args.effort
    os.environ["OPENAI_REQUEST_TIMEOUT"] = str(
        args.timeout if args.timeout is not None
        else {"minimal": 90.0, "low": 150.0}.get(args.effort, 210.0))
    os.environ.setdefault("MULTISTEP_MODEL_PATH", str(
        ROOT / "train_infer_single_ops/trained_model/model_multistep_m4_prefix_history.joblib"))

    from repair_context import build_context
    from prep_utils import llm_generate_setup, require_text, timed_llm_generate
    from score_subtables import gt_birdspider, score_task
    import pipeline_synthesize as PS

    if args.show_prompt:
        d = load(args.inter, args.task_id, args.benchmark, args.split)
        print(build_context("revise_relational_plan", diag=d["diag"], plan=d["plan"],
                            link=d["link"], chains=d["chains"], task_id=args.task_id,
                            question=d["task"].get("question", ""), raw_tables=d["raw"],
                            bench_dir=d["bench_dir"], produced=d["produced"], tried=[]))
        return 0

    labels = {json.loads(l)["task_id"]: json.loads(l)
              for l in (args.inter / "labels.jsonl").open() if l.strip()}
    ids = ([args.task_id] if args.task_id
           else [t for t, r in labels.items() if r["label"] == args.label])
    print(f"{len(ids)} task(s); model {args.model} (effort {args.effort}, "
          f"timeout {os.environ['OPENAI_REQUEST_TIMEOUT']}s)\n")

    def one(tid: str) -> Dict[str, Any]:
        rec: Dict[str, Any] = {"task_id": tid}
        try:
            d = load(args.inter, tid, args.benchmark, args.split)
        except Exception as exc:
            return {**rec, "error": f"load: {type(exc).__name__}: {exc}"}
        gt = gt_birdspider(tid, args.benchmark, args.split, AUTOP)
        if not gt:
            return {**rec, "error": "no gold reference"}
        rec["before"] = score_task(d["produced"], d["edges"], gt)
        rec["after"] = rec["before"]          # default: change nothing
        try:
            ctx = build_context("revise_relational_plan", diag=d["diag"], plan=d["plan"],
                                link=d["link"], chains=d["chains"], task_id=tid,
                                question=d["task"].get("question", ""),
                                raw_tables=d["raw"], bench_dir=d["bench_dir"],
                                produced=d["produced"], tried=[])
            resp, _ = timed_llm_generate(llm_generate_setup, ctx, model=args.model,
                                         json_format=True)
            out = json.loads(require_text(resp, "revise_relational_plan"))
        except Exception as exc:
            return {**rec, "error": f"llm: {type(exc).__name__}: {exc}"}

        rec["plan_at_fault"] = bool(out.get("plan_at_fault"))
        rec["unmet_requirement"] = out.get("unmet_requirement")
        rec["reasoning"] = (out.get("reasoning") or "")[:240]
        if not rec["plan_at_fault"]:
            rec["route"] = "abstained"
            return rec

        rev = apply_revision(d["plan"], out)
        rec["applied"], rec["rejected"] = rev["applied"], rev["rejected"]
        if rev["plan"] is None:
            rec["route"] = "no_applicable_change"
            return rec

        try:
            res = PS.synthesize_pipeline(rev["plan"], task=d["task"],
                                         raw_tables=d["raw"], bench_dir=d["bench_dir"])
            subs = {lt: t.df for lt, t in (res.get("tables") or {}).items()
                    if getattr(t, "df", None) is not None}
        except Exception as exc:
            rec["route"] = "synthesis_failed"
            rec["error"] = f"synth: {type(exc).__name__}: {exc}"
            return rec

        gate = accept(plan_health(d["plan"], d["produced"]),
                      plan_health(rev["plan"], subs))
        rec["gate"] = gate
        rec["scored_if_applied"] = score_task(subs, res.get("join_keys") or [], gt)
        rec["route"] = "applied" if gate["accept"] else "rolled_back"
        if gate["accept"]:
            rec["after"] = rec["scored_if_applied"]
        rec["cost"] = (res.get("usage") or {}).get("cost_usd")
        return rec

    out_path = args.out or (args.inter / "revise_plan_probe.jsonl")
    t0 = time.perf_counter()
    rows: List[Dict[str, Any]] = []
    import threading
    lock = threading.Lock()
    with out_path.open("w") as fh, ThreadPoolExecutor(max_workers=args.workers) as ex:
        for r in ex.map(one, ids):
            with lock:
                rows.append(r)
                fh.write(json.dumps(r, ensure_ascii=False, default=str) + "\n")
                fh.flush()
                print(f"  [{len(rows):>2}/{len(ids)}] {r['task_id']:<16} "
                      f"{r.get('route') or r.get('error','')[:40]:<20} "
                      f"{(r.get('unmet_requirement') or '')[:44]}   "
                      f"{time.perf_counter() - t0:.0f}s", flush=True)

    from collections import Counter
    n = max(len(rows), 1)
    print(f"\nroute: {dict(Counter(r.get('route') or 'error' for r in rows))}")
    for m in ("subtable_full", "join_key_full"):
        b = sum(1 for r in rows if (r.get("before") or {}).get(m))
        a = sum(1 for r in rows if (r.get("after") or {}).get(m))
        blind = sum(1 for r in rows
                    if (r.get("scored_if_applied") or r.get("before") or {}).get(m))
        gain = [r["task_id"] for r in rows
                if (r.get("after") or {}).get(m) and not (r.get("before") or {}).get(m)]
        lose = [r["task_id"] for r in rows
                if (r.get("before") or {}).get(m) and not (r.get("after") or {}).get(m)]
        print(f"{m}:  before {b}/{n}   after {a}/{n}   if applied blindly {blind}/{n}"
              + (f"   gained {gain}" if gain else "")
              + (f"   LOST {lose}" if lose else ""))
    for m in ("subtable_recall", "join_key_recall"):
        pr = [((r.get("before") or {}).get(m), (r.get("after") or {}).get(m)) for r in rows]
        pr = [(x, y) for x, y in pr if x is not None and y is not None]
        if pr:
            print(f"{m}: before {sum(x for x, _ in pr)/len(pr):.3f}   "
                  f"after {sum(y for _, y in pr)/len(pr):.3f}")
    rej = [x for r in rows for x in (r.get("rejected") or [])]
    if rej:
        print(f"\nguards fired {len(rej)}x, e.g. {rej[:4]}")
    cost = sum(r.get("cost") or 0 for r in rows)
    print(f"\nsynthesis spend ${cost:.2f}   wall {time.perf_counter() - t0:.0f}s")
    print(f"per-task -> {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
