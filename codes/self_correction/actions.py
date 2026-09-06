"""The three revise actions, and the State they operate on.

Each action takes a State and returns a NEW State or None ("no change
proposed"). `tree.py` decides which action to run and whether to keep the
result; this module only knows how to perform one.

    revise_table            evidence-fed re-selection of the input tables, then
                            a fresh relational schema and full re-synthesis.
                            6/32 -> 16/32 against a retry-only control,
                            McNemar p = 0.0063.
    revise_relational_plan  conservative schema revision: abstention
                            short-circuits, only ADDITIVE column changes, tables
                            matched by `input_file`, and a regression veto.
                            3/12 -> 5/12 subtable_full, 6/12 -> 9/12 join_key_full.
    revise_pipeline         rewrite one table's pipeline as pandas, applied
                            BLIND. That is deliberate: the validator's "improved
                            and not regressed" rule accepted 0 of 8 rewrites
                            while applying them blind moved 5, because the
                            observables it reads are name-level and already
                            saturated. The tree's own delta gate is the rollback
                            mechanism, so a second, stricter gate inside the
                            action only suppresses candidates before delta ever
                            sees them.

Everything DOWNSTREAM of an action re-runs:

    revise_table            -> relational schema -> pipeline synthesis
    revise_relational_plan  ->                      pipeline synthesis
    revise_pipeline         ->  (its output IS the tables; nothing follows)
"""

from __future__ import annotations

import json
import pickle
import threading
import traceback
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

from . import paths as _scp  # noqa: F401  (puts internal/ on sys.path)

# token accounting
# --------------------------------------------------------------------------- #
# The loop spent real money for weeks without recording a single token. Worse,
# the cost column of the eval table was filled from the BASELINE run's
# _metrics.csv, so the repaired method appeared to cost what the unrepaired one
# did — the repair calls were invisible rather than merely unmeasured.
#
# Prices duplicated from example_run/initital_run/run.py, which stays the source
# of truth; a mismatch shows up as a disagreement between the two cost tables
# rather than silently.
PRICES = {
    "gpt-4o-2024-08-06": {"input": 2.50, "cached": 1.25, "output": 10.0},
    "gpt-5-2025-08-07":  {"input": 1.25, "cached": 0.125, "output": 10.0},
}
_FALLBACK_PRICE = PRICES["gpt-4o-2024-08-06"]
_LOCAL = threading.local()


def meter_reset() -> None:
    _LOCAL.usage = {}
    _LOCAL.bkt = {}


def meter_add(meta: Optional[Dict[str, Any]], model: str = "",
              bucket: str = "revise") -> None:
    """Accumulate one call into the CURRENT TASK's totals.

    Thread-local rather than a cfg field: `cfg` is shared by every worker, so a
    counter on it would sum all tasks together and make per-task cost — the
    thing eval_all_oom's cost table needs — unrecoverable.
    """
    u = getattr(_LOCAL, "usage", None)
    if u is None or not meta:
        return
    m = str(meta.get("model") or model or "")
    d = u.setdefault(m, {"calls": 0, "input": 0, "output": 0, "cached": 0,
                         "elapsed_seconds": 0.0})
    d["calls"] += int(meta.get("calls") or 1)
    # TWO SPELLINGS REACH HERE, AND ONLY ONE WAS READ.
    # `pipeline_synthesize` returns `input`/`output`; `timed_llm_generate` returns
    # `input_tokens`/`output_tokens` via `extract_token_usage`. This function read
    # the first spelling only, so every direct LLM call in the revise actions was
    # counted as one call with zero tokens — a smoke run over 5 tasks reported
    # `calls 5  in 0  out 0  $0.00` after 98 seconds of gpt-5 traffic. The cost
    # column was not merely low; it was structurally blind to the calls this file
    # exists to make.
    for k in ("input", "output"):
        d[k] += int(meta.get(k) or meta.get(f"{k}_tokens") or 0)
    raw = meta.get("raw_usage") or {}
    cached = (meta.get("cached")
              or (raw.get("prompt_tokens_details") or {}).get("cached_tokens")
              or (raw.get("input_tokens_details") or {}).get("cached_tokens") or 0)
    d["cached"] += int(cached or 0)
    d["elapsed_seconds"] += float(meta.get("elapsed_seconds") or 0.0)
    # SAME NUMBERS, SPLIT BY WHO SPENT THEM. An LLM localizer and the revise
    # models bill to one ledger, and the arm comparison needs them apart: the
    # localizer cost is what a trained model replaces, the revise cost is what
    # both arms pay regardless. Subtracting per-round totals from the task total
    # only bounds it, because a candidate's re-diagnosis happens INSIDE a round.
    b = getattr(_LOCAL, "bkt", None)
    if b is None:
        b = _LOCAL.bkt = {}
    e = b.setdefault(f"{bucket}|{m}", {"calls": 0, "input": 0, "output": 0,
                                       "cached": 0})
    e["calls"] += int(meta.get("calls") or 1)
    for k in ("input", "output"):
        e[k] += int(meta.get(k) or meta.get(f"{k}_tokens") or 0)
    e["cached"] += int(cached or 0)


def meter_total() -> Dict[str, Any]:
    u = getattr(_LOCAL, "usage", None) or {}
    out = {"calls": 0, "input": 0, "output": 0, "cached": 0,
           "elapsed_seconds": 0.0, "cost_usd": 0.0, "by_model": u}
    for m, d in u.items():
        pr = PRICES.get(m, _FALLBACK_PRICE)
        fresh = max(d["input"] - d["cached"], 0)
        out["cost_usd"] += (fresh * pr["input"] + d["cached"] * pr["cached"]
                            + d["output"] * pr["output"]) / 1e6
        for k in ("calls", "input", "output", "cached"):
            out[k] += d[k]
        out["elapsed_seconds"] += d["elapsed_seconds"]
    out["cost_usd"] = round(out["cost_usd"], 6)
    by = {}
    for key, d in (getattr(_LOCAL, "bkt", None) or {}).items():
        bucket, _, m = key.partition("|")
        pr = PRICES.get(m, _FALLBACK_PRICE)
        fresh = max(d["input"] - d["cached"], 0)
        t = by.setdefault(bucket, {"calls": 0, "input": 0, "output": 0,
                                   "cached": 0, "cost_usd": 0.0})
        for k in ("calls", "input", "output", "cached"):
            t[k] += d[k]
        t["cost_usd"] += (fresh * pr["input"] + d["cached"] * pr["cached"]
                          + d["output"] * pr["output"]) / 1e6
    for t in by.values():
        t["cost_usd"] = round(t["cost_usd"], 6)
    out["by_bucket"] = by
    return out



# state
# --------------------------------------------------------------------------- #

class State:
    """One task's mutable artefacts. A round replaces some and re-derives the rest."""

    def __init__(self, task, link, plan, produced, edges, raw, bench_dir,
                 steps=None, rewrite=None):
        self.task, self.link, self.plan = task, link, plan
        self.produced, self.edges, self.raw = produced, edges, raw
        self.bench_dir = bench_dir
        # PROVENANCE, not decoration. eval_all_oom never reads a materialised
        # frame — it re-executes source under a traced pandas — so a state that
        # carries only `produced` cannot be scored at all.
        #
        # Two shapes, because the two producers do not share semantics.
        # `steps[lt]` is a synthesis chain, replayed the way `run_table` does it
        # (sanitize AND auto-rename around every step). `rewrite[lt]` is what
        # `revise_pipeline` did, and it OVERRIDES steps for that table:
        #   base "raw"     the snippet ran on the untouched pickle — no
        #                  sanitize, no auto-rename
        #   base "replay"  `revise_pipeline_code.replay` semantics — sanitize
        #                  only, never auto-rename — then the snippet if any
        # Collapsing these into one path silently exports a script that does not
        # reproduce the frame that was scored.
        self.steps = steps or {}
        self.rewrite = rewrite or {}

    def copy(self) -> "State":
        return State(self.task, dict(self.link), json.loads(json.dumps(self.plan)),
                     dict(self.produced), list(self.edges), dict(self.raw),
                     self.bench_dir,
                     {k: list(v) for k, v in self.steps.items()},
                     {k: dict(v) for k, v in self.rewrite.items()})


def load_state(task_id: str, dataset: str, *,
               selection: Optional[Dict[str, Any]] = None,
               schema: Optional[Dict[str, Any]] = None,
               pipeline: Optional[Dict[str, Any]] = None) -> State:
    """Assemble one task's State from the upstream modules' outputs.

    Reads, in order:
        table_discovery/selection/<Dataset>/table_selection.jsonl   the link
        pipeline_synthesize/schema/<Dataset>/relational_schema.jsonl the schema
        pipeline_synthesize/pipeline/<Dataset>/pipeline.jsonl        the pipeline

    The produced subtables are re-materialised by replaying each table's chain
    on its raw frame, because `pipeline.jsonl` records columns and shape but not
    the frames themselves — keeping 6 candidates x N tables of DataFrames on
    disk would dwarf everything else.
    """
    import pandas as pd
    from common import dataset as DS
    from common import paths as P
    from common.io_utils import load_jsonl_by_key

    ds = DS.resolve(dataset)

    def _row(module: str, group: str, name: str, given):
        if given is not None:
            return given
        path = P.resolve(dataset, module=module, group=group).out(name)
        return load_jsonl_by_key(path, "task_id").get(str(task_id), {})

    link = _row("table_discovery", "selection", "table_selection.jsonl", selection)
    plan = _row("pipeline_synthesize", "schema", "relational_schema.jsonl", schema)
    pipe = _row("pipeline_synthesize", "pipeline", "pipeline.jsonl", pipeline)
    if not plan:
        raise KeyError(f"no relational schema for {task_id}; run "
                       f"pipeline_synthesize.relational_schema first")

    task = next((t for t in ds.tasks() if str(t.get("task_id")) == str(task_id)), None)
    if task is None:
        raise KeyError(f"task {task_id!r} is not in {dataset}'s benchmark.jsonl")

    # The old loader read `gold_tables`; the schema now uses `tables`. Present
    # both, as the same list, so neither name can go stale.
    plan = dict(plan)
    plan.setdefault("tables", plan.get("gold_tables") or [])
    plan["gold_tables"] = plan["tables"]
    plan.setdefault("task_id", str(task_id))

    raw = rebuild_raw(plan, ds.input_tables)

    steps = {lt: list(t.get("steps") or [])
             for lt, t in (pipe.get("tables") or {}).items()}
    produced = _materialise(raw, steps)
    edges = list(pipe.get("join_keys") or plan.get("join_edges") or [])

    return State(task, link, plan, produced, edges, raw, ds.input_tables, steps)


def _materialise(raw: Dict[str, Any], steps: Dict[str, list]) -> Dict[str, Any]:
    """Replay each table's recorded chain on its raw frame.

    A table whose chain is empty, or whose replay fails, keeps its raw frame:
    that is what synthesis itself produced in those cases, and dropping the
    table instead would make the diagnosis blame a missing table rather than the
    wrong one.
    """
    import test_param_synthesis as M
    from table_executor import execute_chain

    out = {}
    for lt, df in raw.items():
        chain = steps.get(lt) or []
        frame = M.sanitize(df)
        if chain:
            try:
                res, err = execute_chain(frame, chain)
                if res is not None:
                    frame = M.sanitize(res)
            except Exception:
                pass
        out[lt] = frame
    return out


def rebuild_raw(plan: Dict[str, Any], bench_dir: Path) -> Dict[str, Any]:
    import pandas as pd
    out = {}
    for t in plan.get("gold_tables") or []:
        p = bench_dir / (t.get("input_file") or "")
        if p.exists():
            try:
                out[t["logical_table"]] = pd.read_pickle(p)
            except Exception:
                pass
    return out



# --------------------------------------------------------------------------- #

def _synthesize(plan, st: State, model_syn: Optional[str],
                workers: Optional[int] = None) -> Tuple[Dict, List]:
    """Re-run synthesis.

    `workers` caps the threads INSIDE one task. `pipeline_synthesize.FIXED`
    defaults to 8, and the loop then runs `--workers` tasks on top of that, so
    `--workers 2` means 16 concurrent table synthesises each holding DataFrames.
    On an 8 GB machine that is what got the full 141-task run killed by the OOM
    reaper at task 85.
    """
    from synthesis_shim import synthesize_pipeline as _synth
    kw = {"model": model_syn} if model_syn else {}
    if workers:
        kw["workers"] = workers
    res = _synth(plan, task=st.task, raw_tables=st.raw,
                 bench_dir=st.bench_dir, **kw)
    # revise_table and revise_relational_plan both re-run the whole synthesis,
    # which is where most of a repair's tokens actually go — far more than the
    # one gpt-5 call that decided to do it.
    meter_add(res.get("usage"), model_syn or "gpt-4o-2024-08-06")
    subs = {lt: t.df for lt, t in (res.get("tables") or {}).items()
            if getattr(t, "df", None) is not None}
    steps = {lt: list(getattr(t, "steps", None) or [])
             for lt, t in (res.get("tables") or {}).items()}
    return subs, list(res.get("join_keys") or []), steps


def act_revise_table(st: State, diag, chains, cfg) -> Optional[State]:
    from . import revise_table as RT
    from relational_plan import synthesize_plan
    res = RT.revise_table(st.task, diag=diag, plan=st.plan, link=st.link,
                          chains=chains, produced=st.produced,
                          raw_tables=st.raw, bench_dir=st.bench_dir,
                          benchmark=cfg["benchmark"], split=cfg["split"],
                          model=cfg["model"])
    sel = res.get("selected_tables") or []
    if not sel or sorted(sel) == sorted(st.link.get("selected_tables") or []):
        return None
    plan = synthesize_plan(st.task.get("question", ""), sel,
                           subquestions=res.get("subquestions") or {},
                           bench_dir=st.bench_dir)
    plan["task_id"] = st.task.get("task_id")
    new = st.copy()
    new.link, new.plan = res, plan
    new.raw = rebuild_raw(plan, st.bench_dir)
    new.produced, new.edges, new.steps = _synthesize(plan, new, cfg.get("model_syn"),
                                                     cfg.get("syn_workers"))
    new.rewrite = {}               # re-synthesis discards any earlier rewrite
    return new


def act_revise_relational_plan(st: State, diag, chains, cfg) -> Optional[State]:
    from repair_context import build_context
    from prep_utils import llm_generate_setup, require_text, timed_llm_generate
    from . import revise_relational_plan as RP
    ctx = build_context("revise_relational_plan", diag=diag, plan=st.plan,
                        link=st.link, chains=chains,
                        task_id=st.task.get("task_id"),
                        question=st.task.get("question", ""), raw_tables=st.raw,
                        bench_dir=st.bench_dir, produced=st.produced, tried=[])
    resp, _m = timed_llm_generate(llm_generate_setup, ctx, model=cfg["model"],
                                  json_format=True)
    meter_add(_m, cfg["model"])
    out = json.loads(require_text(resp, "repair_loop revise"))
    if not out.get("plan_at_fault"):
        return None                       # abstention: change nothing, spend nothing
    rev = RP.apply_revision(st.plan, out)
    if rev["plan"] is None:
        return None
    new = st.copy()
    new.plan = rev["plan"]
    new.produced, new.edges, new.steps = _synthesize(rev["plan"], new,
                                                     cfg.get("model_syn"),
                                                     cfg.get("syn_workers"))
    new.rewrite = {}
    # The regression veto stays: this action can silently break a working join.
    gate = RP.accept(RP.plan_health(st.plan, st.produced),
                     RP.plan_health(rev["plan"], new.produced))
    return None if not gate["accept"] else new


def _as_text(v, default: str = "") -> str:
    """A model-supplied field, as a string, whatever the model actually sent.

    `what_is_missing` is documented in the prompt as a sentence and is usually
    one, but gpt-5 sometimes answers with an object — a per-table breakdown, or
    {"column": ..., "reason": ...}. Concatenating that raised

        TypeError: can only concatenate str (not "dict") to str

    which killed the round, and the loop recorded it as `no change proposed`:
    indistinguishable from the model having nothing to propose. It cost 2 of 148
    rounds on bird, and the rate is a property of the model, not of the
    benchmark, so it would have recurred on every new dataset.

    Structured content is kept rather than discarded — it is still the symptom,
    just not in the shape the prompt asked for.
    """
    if isinstance(v, str):
        return v.strip() or default
    if v in (None, [], {}):
        return default
    return json.dumps(v, ensure_ascii=False)[:1000]


def act_revise_pipeline(st: State, diag, chains, cfg) -> Optional[State]:
    """Localize a table, then rewrite its pipeline as pandas. Applied BLIND.

    `--accept blind` is deliberate. The validator's `improved and not regressed`
    rule accepted 0 of 8 rewrites while applying them blind moved 5, because the
    observables it reads are name-level and already saturated. The loop's own
    delta gate is the rollback mechanism, so a second, stricter gate inside the
    action only suppresses candidates before delta ever sees them.
    """
    from . import revise_pipeline_code as RC
    from prep_utils import llm_generate_setup, require_text, timed_llm_generate
    p = RC.build_localise_prompt(question=st.task.get("question", ""),
                                 plan=st.plan, produced=st.produced, edges=st.edges)
    resp, _m = timed_llm_generate(llm_generate_setup, p, model=cfg["model"],
                                  json_format=True)
    meter_add(_m, cfg["model"])
    loc = json.loads(require_text(resp, "repair_loop localise"))
    # Same defect class as `what_is_missing`, but silent: the prompt asks for a
    # list and a model that answers with the bare string "table_1" would be
    # iterated CHARACTER BY CHARACTER, none of which is a table, leaving `picks`
    # empty and the round recorded as `no change proposed`. No exception, no
    # trace, one lost repair.
    _at = loc.get("at_fault")
    if isinstance(_at, str):
        _at = [_at]
    elif not isinstance(_at, (list, tuple)):
        _at = []
    picks = [t for t in _at if t in st.produced]
    if not picks:
        return None
    lt = picks[0]
    raw = st.raw.get(lt)
    if raw is None:
        return None
    cands = RC.candidates_for(cfg["pipe"].get(st.task["task_id"], {}), lt, raw)
    p2 = RC.build_rewrite_prompt(
        question=st.task.get("question", ""), lt=lt, plan=st.plan, link=st.link,
        raw=raw, candidates=cands, edges=st.edges,
        symptom="  " + _as_text(loc.get("what_is_missing"),
                                "the produced table does not answer the question"))
    resp2, _m = timed_llm_generate(llm_generate_setup, p2, model=cfg["model"],
                                   json_format=True)
    meter_add(_m, cfg["model"])
    out = json.loads(require_text(resp2, "repair_loop rewrite"))
    # Both branches record how the frame was reached. A candidate IS replayable —
    # `candidates_for` builds it by replaying `c["steps"]` on the raw frame — so
    # the accepted candidate exports as an ordinary operator chain, and only the
    # free-pandas branch needs a snippet. Without this the produced frame has no
    # source and eval_all_oom, which re-executes rather than reads frames, cannot
    # score the task at all.
    ai = out.get("accept_candidate")
    if ai is not None and 0 <= int(ai) < len(cands) and cands[int(ai)][1] is not None:
        new_df = cands[int(ai)][1]
        prov = {"base": "replay", "steps": list((cands[int(ai)][0] or {}).get("steps") or []),
                "code": ""}
    else:
        start, prov = raw, {"base": "raw", "steps": [], "code": ""}
        ci = out.get("closest_candidate")
        if out.get("start_from") == "candidate" and ci is not None and 0 <= int(ci) < len(cands):
            if cands[int(ci)][1] is not None:
                start = cands[int(ci)][1]
                prov = {"base": "replay",
                        "steps": list((cands[int(ci)][0] or {}).get("steps") or []),
                        "code": ""}
        prov["code"] = out.get("code") or ""
        new_df, err = RC.run_snippet(prov["code"], start)
        if new_df is None:
            return None
    new = st.copy()
    new.produced = {**st.produced, lt: new_df}
    new.rewrite[lt] = prov
    return new


ACTIONS = {"revise_table": act_revise_table,
           "revise_relational_plan": act_revise_relational_plan,
           "revise_pipeline": act_revise_pipeline}


