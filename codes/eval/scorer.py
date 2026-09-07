"""Value-domain scoring of a Prep-Weaver run. No external evaluator needed.

Scores only THIS system's own output, read from `results/`. Baseline comparison
is deliberately out of scope: the reference evaluator dispatches over half a
dozen methods, and reproducing that dispatch is what made it un-runnable outside
its own checkout.

THE METRIC
----------
Names are ignored throughout; only VALUES are compared. A prepared table is
correct when the values of every gold column reappear somewhere in what the
system produced, and the relationships are correct when the same holds for the
value domains on both sides of every gold join edge.

    normalise      strip; drop empty / nan / none / <NA>; render a numeric as
                   an int when it is integral, else repr(float), so 1, 1.0 and
                   " 1 " are one value

    vmatch(M, G)   a predicted domain M covers a gold domain G when
                       |M ∩ G| >= min(2, |G|)      and
                       |M ∩ G| / |M| >= 0.8
                   The first term rejects a one-value coincidence. The second is
                   what stops an "EAV grab-bag" — a column holding every value
                   in the database would otherwise cover every gold column.

    matching       ONE-TO-ONE (maximum bipartite matching), not per-column
                   lookup. Without it a single predicted domain — typically a
                   shared join key — would cover several gold columns from
                   different tables at once and inflate the score.

    table correctness       matched gold columns / all gold columns == 1.0
    relationship correctness matched gold key domains / all of them == 1.0

Gold columns come from `tables_rels/outputs/<task>.json`: for every
(table, column) in `table_columns`, the DISTINCT values of that column in the
task's sqlite database. Gold key domains are both sides of every `join_keys` and
`set_relations` entry, de-duplicated by value set.

WHAT COUNTS AS THE PREDICTION
-----------------------------
Every column of every subtable the system produced, plus, for each join edge the
relational schema declared, the values of the two key columns. The subtables are
re-materialised by replaying each recorded operator chain on its raw input, so
what is scored is what the pipeline actually produces.

ALIGNMENT
---------
The reference evaluator reaches the same numbers by re-executing an exported
script under a lineage tracer, which additionally captures intermediate columns.
Extra predicted domains can only ever help a one-to-one matching, so this
implementation is a lower bound on that one. `verify_scorer_alignment.py`
measures the difference per task rather than assuming it is zero.

Run:
    python -m eval.scorer --dataset Synth-Bird
    python -m eval.scorer --dataset Synth-Bird --source selection
"""

from __future__ import annotations

import json
import os
import sqlite3
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Set, Tuple

import pandas as pd

MAX_COL_VALUES = 20000          # cap per column, so a huge table cannot exhaust memory


# --------------------------------------------------------------------------- #
# value normalisation
# --------------------------------------------------------------------------- #

def normalise(values: Iterable) -> Set[str]:
    """A comparable value set: 1, 1.0 and " 1 " all become "1"."""
    out: Set[str] = set()
    for v in values:
        if v is None:
            continue
        s = str(v).strip()
        if not s or s.lower() in ("nan", "none", "<na>"):
            continue
        try:
            f = float(s)
            s = str(int(f)) if f == int(f) else repr(f)
        except Exception:
            pass
        out.add(s)
    return out


def norm_series(s, max_values: int = MAX_COL_VALUES) -> Set[str]:
    """Normalise a column without materialising unbounded values."""
    try:
        if isinstance(s, pd.DataFrame):
            s = s.iloc[:, 0]
        s = pd.Series(s).dropna()
        if max_values and len(s) > max_values:
            s = s.sample(max_values, random_state=0)
        return normalise(s.astype(str).drop_duplicates().tolist())
    except BaseException:
        return set()


# --------------------------------------------------------------------------- #
# matching
# --------------------------------------------------------------------------- #

def vmatch(pred: Set[str], gold: Set[str]) -> bool:
    """Whether a predicted value domain covers a gold one."""
    if not pred or not gold:
        return False
    inter = len(pred & gold)
    if inter < min(2, len(gold)):
        return False
    return inter / len(pred) >= 0.8


def _dedup(domains: Sequence[Set[str]]) -> List[Set[str]]:
    seen, out = set(), []
    for d in domains:
        if not d:
            continue
        k = frozenset(d)
        if k in seen:
            continue
        seen.add(k)
        out.append(d)
    return out


def max_matching(pred_domains: Sequence[Set[str]],
                 gold_domains: Sequence[Set[str]]) -> Tuple[int, int]:
    """Maximum bipartite matching from predicted domains to gold domains.

    One-to-one: a predicted domain can satisfy at most one gold domain, so a
    shared join key cannot cover several gold columns at once.
    """
    pred = _dedup(pred_domains)
    gold = _dedup(gold_domains)
    match_to_pred: Dict[int, int] = {}

    def dfs(pi: int, seen: Set[int]) -> bool:
        for gi, g in enumerate(gold):
            if gi in seen or not vmatch(pred[pi], g):
                continue
            seen.add(gi)
            if gi not in match_to_pred or dfs(match_to_pred[gi], seen):
                match_to_pred[gi] = pi
                return True
        return False

    matched = sum(1 for pi in range(len(pred)) if dfs(pi, set()))
    return matched, len(gold)


# --------------------------------------------------------------------------- #
# gold
# --------------------------------------------------------------------------- #

def gold_domains(outputs_json: Path) -> Optional[dict]:
    """{cols, edges, col_labels, edge_labels} for one task, or None.

    Column values come from the task's sqlite database, so the gold is the
    database's own content rather than anything the system produced.
    """
    outputs_json = Path(outputs_json)
    if not outputs_json.exists():
        return None
    d = json.loads(outputs_json.read_text())

    edges, edge_labels = [], []
    for e in (d.get("join_keys") or []) + (d.get("set_relations") or []):
        lv, rv = normalise(e.get("left_values") or []), normalise(e.get("right_values") or [])
        if lv or rv:
            edges.append({"left": lv, "right": rv})
            edge_labels.append(f"{e.get('left_table')}.{e.get('left_column')}"
                               f" <-> {e.get('right_table')}.{e.get('right_column')}")

    cols, col_labels = [], []
    db_path = d.get("db_path") or ""
    if db_path:
        # Stored relative to the outputs directory.
        p = Path(db_path)
        if not p.is_absolute():
            p = (outputs_json.parent / p).resolve()
        if p.exists():
            try:
                con = sqlite3.connect(str(p))
                for tbl, tcols in (d.get("table_columns") or {}).items():
                    for c in tcols:
                        try:
                            rows = con.execute(f'SELECT DISTINCT "{c}" FROM "{tbl}"').fetchall()
                            v = normalise(r[0] for r in rows)
                            if v:
                                cols.append(v)
                                col_labels.append(f"{tbl}.{c}")
                        except Exception:
                            pass
                con.close()
            except Exception:
                pass
    return {"cols": cols, "edges": edges,
            "col_labels": col_labels, "edge_labels": edge_labels}


def gold_domains_exists(ds, task_id: str) -> bool:
    return (ds.outputs_dir / f"{task_id}.json").exists()


def gold_key_domains(edges: Sequence[dict]) -> List[Set[str]]:
    out = []
    for e in edges:
        if e.get("left"):
            out.append(e["left"])
        if e.get("right"):
            out.append(e["right"])
    return _dedup(out)


# --------------------------------------------------------------------------- #
# prediction
# --------------------------------------------------------------------------- #

def predicted_domains(subtables: Dict[str, pd.DataFrame],
                      join_edges: Sequence[dict],
                      intermediates: Optional[Sequence[pd.DataFrame]] = None) -> dict:
    """{cols, keys} from the produced subtables, their intermediates, and the
    declared join edges."""
    cols, col_labels = [], []
    for lt, df in subtables.items():
        if not isinstance(df, pd.DataFrame):
            continue
        for c in df.columns:
            v = norm_series(df[c])
            if v:
                cols.append(v)
                col_labels.append(f"{lt}.{c}")
    for i, df in enumerate(intermediates or []):
        if not isinstance(df, pd.DataFrame):
            continue
        for c in df.columns:
            v = norm_series(df[c])
            if v:
                cols.append(v)
                col_labels.append(f"intermediate[{i}].{c}")

    def _col(df: pd.DataFrame, name) -> Optional[Set[str]]:
        import re
        key = re.sub(r"[^a-z0-9]", "", str(name).lower())
        for c in df.columns:
            if re.sub(r"[^a-z0-9]", "", str(c).lower()) == key:
                return norm_series(df[c])
        return None

    keys, key_labels = [], []
    for e in join_edges or []:
        for side, tbl, col in (("left", e.get("left_table"), e.get("left_on")),
                               ("right", e.get("right_table"), e.get("right_on"))):
            df = subtables.get(tbl)
            if df is None or col is None:
                continue
            v = _col(df, col)
            if v:
                keys.append(v)
                key_labels.append(f"{tbl}.{col}")
    return {"cols": cols, "keys": keys,
            "col_labels": col_labels, "key_labels": key_labels}


# --------------------------------------------------------------------------- #
# score one task
# --------------------------------------------------------------------------- #

def score_task(pred: dict, gold: dict) -> dict:
    """Coverage fractions for one task. None when there is no gold to score."""
    sub = jk = None
    if gold["cols"]:
        m, t = max_matching(pred["cols"], gold["cols"])
        sub = m / t if t else None
    if gold["edges"]:
        m, t = max_matching(pred["keys"], gold_key_domains(gold["edges"]))
        jk = m / t if t else None
    return {"subtable_cov": sub, "join_key": jk,
            "n_pred_cols": len(pred["cols"]), "n_pred_keys": len(pred["keys"]),
            "n_gold_cols": len(gold["cols"]),
            "n_gold_keys": len(gold_key_domains(gold["edges"]))}


# --------------------------------------------------------------------------- #
# reading a run out of results/
# --------------------------------------------------------------------------- #

def materialise(raw: Dict[str, pd.DataFrame], steps: Dict[str, list],
                specs: Optional[Dict[str, dict]] = None,
                on_error: Optional[List[str]] = None
                ) -> Tuple[Dict[str, pd.DataFrame], List[pd.DataFrame]]:
    """Replay each table's chain, returning (final frames, intermediate frames).

    `pipeline.jsonl` stores columns and shape, not frames — keeping several
    candidate frames per table on disk would dwarf everything else — so they are
    rebuilt through the same executor the pipeline ran.

    The intermediates matter for scoring. The reference evaluator traces the
    executed code and therefore sees every frame the pipeline passed through,
    not only the last one; a gold column materialised at step 2 and consumed at
    step 3 counts there. Collecting them here closed most of that difference:
    exact per-task agreement on bird went 79.4% -> 83.0%, and table correctness
    0.5390 -> 0.5674 against the reference's 0.5957.

    `steps` is not the whole chain. Between operators the pipeline applies a
    deterministic rename -- a transposed index column `row_id` to the key column
    the schema asks for, and casing-only differences -- which is not an operator
    and so is not recorded. Replaying the operators alone therefore diverges at
    the first step that refers to a renamed column: `Transpose` emits `row_id`,
    the recorded `Pivot(index="Id")` then raises KeyError, and the table is left
    unreshaped. That needs `specs`, the relational schema per logical table.

    A chain that fails to replay is reported through `on_error`, never silently
    swallowed. Falling back to the raw frame keeps a plausible-looking score:
    the table is still there, its values still cover some gold columns, but the
    declared join key is not a column of an unreshaped table, so the key is
    dropped and relationship correctness reads as a modelling failure when it is
    a replay failure. That mistake cost 15 of 141 bird tasks.
    """
    import test_param_synthesis as M
    try:
        from coverage_policy import plan_next, apply_auto_rename
    except Exception:                       # engine not importable: no renames
        plan_next = apply_auto_rename = None
    try:
        from table_specs import normalize_spec
        from schema_conform import conform_to_schema
    except Exception:
        normalize_spec = conform_to_schema = None

    def finish(df, spec):
        """Schema conformance, which the pipeline applies AFTER the operator loop.

        Not an operator, so not in `steps`. Skipping it leaves the literal
        quoting the raw data carries: `bird_1ab2aac9` produced account ids as
        '"2444"' where the gold domain holds 2444, so the two sets intersected
        in ZERO values and the join key scored as wrong while being right.
        """
        if conform_to_schema is None or not spec:
            return df
        try:
            types = (normalize_spec(spec) or {}).get("column_types") or {}
            return conform_to_schema(df, types) if types else df
        except Exception:
            return df

    def conform(df, spec):
        """The pipeline's deterministic between-step repair."""
        if plan_next is None or not spec:
            return df
        try:
            return apply_auto_rename(df, plan_next(df, spec)["auto_rename"])
        except Exception:
            return df

    final, mids = {}, []
    for lt, df in raw.items():
        spec = (specs or {}).get(lt)
        frame = conform(M.sanitize(df), spec)
        chain = steps.get(lt) or []
        ok = True
        for i, step in enumerate(chain, 1):
            # `robust_execute`, not `execute_chain`. The exported script -- the
            # thing the reference evaluator actually runs -- uses this one, and
            # the two disagree: on bird_08611c0f `execute_chain` leaves the
            # transposed index as `row_id`, the deterministic rename then claims
            # it for the primary key rather than the column `Pivot` was given,
            # and the step raises KeyError. `robust_execute` reproduces the
            # recorded (10698, 21) exactly.
            try:
                res, err = M.robust_execute(frame, step), None
            except Exception as exc:
                res, err = None, f"{type(exc).__name__}: {exc}"
            if res is None:
                ok = False
                if on_error is not None:
                    on_error.append(f"{lt} step {i}/{len(chain)} "
                                    f"{step.get('op')}: {err}")
                break
            frame = conform(M.sanitize(res), spec)
            if i < len(chain):
                mids.append(frame)
        final[lt] = finish(frame, spec)
    return final, mids


OURS = {"no_self_correction", "self_correction"}
_ALIASES = {"selection": "no_self_correction", "repair": "self_correction",
            "ours": "no_self_correction", "ours_repair": "self_correction",
            # The LLM baseline is named for the model it runs; `gpt5` was the
            # internal shorthand and still resolves.
            "gpt5": "gpt-5.5"}


def baseline_dir(method: str, dataset: str) -> Path:
    """Where a baseline's generated code for one dataset lives."""
    from common import paths as P
    return (P.REPO_ROOT / "baselines" / "baseline_results" / method / dataset)


def available_baselines() -> List[str]:
    from common import paths as P
    root = P.REPO_ROOT / "baselines" / "baseline_results"
    return sorted(d.name for d in root.iterdir() if d.is_dir()) if root.exists() else []


def load_baseline(dataset: str, method: str, timeout: int = 120,
                  mem_gb: float = 8.0,
                  task_ids: Optional[Sequence[str]] = None,
                  skip: Optional[Sequence[str]] = None) -> Dict[str, dict]:
    """Run a baseline's code per task and collect what it produced.

    A baseline emits arbitrary pandas rather than a recorded operator chain, so
    there is nothing to replay: the code is executed and watched. Join keys come
    from the merges and `isin` filters it actually performed, because after a
    merge the two key columns are usually collapsed into one and a semi-join key
    never becomes a column at all.
    """
    from common import dataset as DS
    from .tracer import run_code

    ds = DS.resolve(dataset)
    d = baseline_dir(method, dataset)
    if not d.exists():
        raise FileNotFoundError(
            f"no results for baseline {method!r} at {d}. "
            f"Available: {', '.join(available_baselines()) or 'none'}")

    from tqdm import tqdm

    out: Dict[str, dict] = {}
    # Only run what is actually going to be scored. Executing a baseline is the
    # expensive part, so a --task-ids run must not pay for the other 130 tasks,
    # and a cached task must not be run again.
    want = set(task_ids) if task_ids else None
    done = set(skip or ())
    tasks = [t for t in ds.tasks()
             if (want is None or str(t.get("task_id")) in want)
             and str(t.get("task_id")) not in done
             and any((d / f"{t.get('task_id')}{e}").exists() for e in (".py", ".json"))]
    for task in tqdm(tasks, desc=f"running {method}", unit="task"):
        tid = str(task.get("task_id"))
        src = next((d / f"{tid}{ext}" for ext in (".py", ".json")
                    if (d / f"{tid}{ext}").exists()), None)
        if src is None:
            continue
        tables = {}
        for i, f in enumerate(task.get("input_table") or [], 1):
            p = ds.input_tables / f
            if p.exists():
                try:
                    tables[f"table_{i}"] = pd.read_pickle(p)
                except Exception:
                    pass

        if src.suffix == ".json":
            # A SQL-emitting baseline. Its work never passes through pandas, so
            # the pandas tracer would see an empty run and score it as all-zeros
            # — which reads as "it got everything wrong" rather than "we did not
            # measure it". Run the statements in duckdb instead.
            from .sql_tracer import run_sql, clean_columns
            art = json.loads(src.read_text(errors="replace"))
            # The SQL was generated against column names the producing driver had
            # already cleaned (lower-cased, non-word runs collapsed to "_"), and it
            # refers to them by those names. Registering the raw frames instead makes
            # every statement fail on an unknown column, which scores as "wrong"
            # rather than "not measured" — the exact failure this branch exists to
            # avoid. The driver shipped the cleaned frames alongside each artifact;
            # they are 5.4 GB for one benchmark, so they are reconstructed here.
            r = run_sql(art.get("statements") or art.get("S") or "",
                        {k: clean_columns(v) for k, v in tables.items()},
                        timeout=timeout)
        else:
            r = run_code(src.read_text(errors="replace"), tables,
                         timeout=timeout, mem_gb=mem_gb)
        out[tid] = {
            "subtables": {f"frame_{i}": f for i, f in enumerate(r["frames"])},
            "intermediates": [],
            "join_edges": [],
            "traced_keys": r["joins"],
            "selected_tables": [],
            "error": r["error"],
        }
    return out


def load_run(dataset: str, source: str = "self_correction") -> Dict[str, dict]:
    """{task_id: {subtables, join_edges, selected_tables}} for a whole dataset.

    source="no_self_correction"  the pipeline as synthesized
    source="self_correction"     the state the repair tree chose
    source="auto"                the repaired one where it exists
    """
    source = _ALIASES.get(source, source)
    replay_errors: Dict[str, List[str]] = {}
    from common import dataset as DS
    from common import paths as P
    from common.io_utils import load_jsonl_by_key
    import self_correction  # noqa: F401  (importing it puts the engine executor on the path)

    ds = DS.resolve(dataset)
    schema = load_jsonl_by_key(P.resolve(dataset, module="pipeline_synthesize",
                                         group="schema").out("relational_schema.jsonl"), "task_id")
    pipe = load_jsonl_by_key(P.resolve(dataset, module="pipeline_synthesize",
                                       group="pipeline").out("pipeline.jsonl"), "task_id")
    repair = {}
    if source in ("auto", "self_correction"):
        repair = load_jsonl_by_key(P.resolve(dataset, module="self_correction",
                                             group="").out("repair.jsonl"), "task_id")
        if source == "self_correction" and not repair:
            raise FileNotFoundError("--source repair asked for, but repair.jsonl is empty")

    sel = load_jsonl_by_key(P.resolve(dataset, module="table_discovery",
                                      group="selection").out("table_selection.jsonl"), "task_id")

    out = {}
    for tid, prec in pipe.items():
        srec = schema.get(tid) or {}
        tables = srec.get("tables") or srec.get("gold_tables") or []
        raw = {}
        if tables:
            for t in tables:
                p = ds.input_tables / (t.get("input_file") or "")
                if p.exists():
                    try:
                        raw[t["logical_table"]] = pd.read_pickle(p)
                    except Exception:
                        pass
        else:
            # No relational schema for this task: fall back to the selection, in
            # order. `load_tables` numbers the logical tables that way, so the
            # binding is the same one synthesis used.
            for i, f in enumerate((sel.get(tid) or {}).get("selected_tables") or [], 1):
                p = ds.input_tables / f
                if p.exists():
                    try:
                        raw[f"table_{i}"] = pd.read_pickle(p)
                    except Exception:
                        pass

        rrec = repair.get(tid) if source != "no_self_correction" else None
        steps = {lt: list(t.get("steps") or [])
                 for lt, t in (prec.get("tables") or {}).items()}
        selected = list((sel.get(tid) or {}).get("selected_tables") or [])
        if rrec:
            # The repair tree records each node's columns, not its frames, so the
            # chosen state is rebuilt from the steps of the node that was picked.
            best = next((n for n in rrec.get("nodes") or []
                         if n.get("id") == rrec.get("best")), None)
            if best is None or "steps_by_table" not in best:
                # A record written before per-node provenance existed. Silently
                # falling back to the unrepaired pipeline would report the
                # ablation as "self-correction changes nothing", so refuse.
                raise KeyError(
                    f"{tid}: this repair.jsonl predates per-node provenance "
                    f"(no steps_by_table), so the repaired state cannot be "
                    f"rebuilt. Re-run self_correction.loop, or score with "
                    f"--source no_self_correction.")
            steps = best["steps_by_table"]
            selected = list(rrec.get("selected_tables") or selected)

        specs = {t.get("logical_table"): t
                 for t in ((srec.get("tables") or []) if srec else [])
                 if t.get("logical_table")}
        errs: List[str] = []
        subs, mids = materialise(raw, steps, specs, errs)
        if errs:
            replay_errors[tid] = errs
        out[tid] = {
            "subtables": subs,
            "intermediates": mids,
            "join_edges": list(prec.get("join_keys") or srec.get("join_edges") or []),
            "selected_tables": selected,
        }
    if replay_errors:
        # Loud on purpose. A chain that does not replay is scored as if the
        # method produced an unreshaped table, which reads as a modelling
        # failure rather than an evaluation one.
        print(f"[scorer] WARNING: {len(replay_errors)} task(s) whose recorded "
              f"operator chain failed to replay; their scores are not "
              f"meaningful. First few:")
        for tid, msgs in list(replay_errors.items())[:5]:
            print(f"    {tid}: {msgs[0]}")
    return out


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #

def evaluate(dataset: str, source: str = "self_correction",
             task_ids: Optional[Sequence[str]] = None,
             timeout: int = 120, mem_gb: float = 8.0,
             only_produced: bool = False) -> dict:
    """Score one method on one dataset: the four metrics plus per-task rows.

    `source` is either one of this system's own states (no_self_correction /
    self_correction), read from the recorded artefacts, or the name of a
    baseline under baselines/baseline_results/, whose generated code is executed.

    THE DENOMINATOR IS THE WHOLE BENCHMARK, not the tasks the method produced
    output for. A method that emits nothing for a task did not solve it, and
    scoring it over only its own successes rewards giving up: on Synth-Bird
    `deepprep_adapted` has output for 100 of 141 tasks and 32 of them are
    correct, which is 0.227 over the benchmark and 0.320 over its own subset —
    a 0.093 difference that comes entirely from the 41 tasks it skipped.

    `only_produced=True` restores the per-subset view. It answers a different
    question ("when it does answer, how good is it?") and must not be compared
    against a method scored the other way.
    """
    from common import dataset as DS

    ds = DS.resolve(dataset)
    gold_sets = {str(t.get("task_id")): {_tnorm(x) for x in ds.gold_tables(t)}
                 for t in ds.tasks()}
    canon = _ALIASES.get(source, source)
    is_ours = canon in OURS or canon == "auto"

    # Executing a baseline takes minutes per task; its per-task SCORE is four
    # numbers. Cache the scores, so re-reading a result, adding a method to a
    # comparison, or changing the table set never re-runs code that already ran.
    cache_path = None
    cached: Dict[str, dict] = {}
    if not is_ours:
        from common import paths as P
        cache_path = (P.resolve(dataset, module="eval", group="").out_dir
                      / "baseline_cache" / f"{canon}.jsonl")
        cached = load_jsonl_by_key(cache_path, "task_id") if cache_path.exists() else {}

    run = (load_run(dataset, canon) if is_ours
           else load_baseline(dataset, canon, timeout=timeout, mem_gb=mem_gb,
                              task_ids=task_ids, skip=list(cached)))
    produced = set(run) | set(cached)
    ids = sorted(produced if only_produced
                 else (t for t in gold_sets if gold_domains_exists(ds, t)))
    if task_ids:
        ids = [t for t in ids if t in set(task_ids)]
    new_scores = []

    rows = []
    n_ident = n_tab = n_rel = n_prep = n_scored = 0
    for tid in ids:
        r = run.get(tid)
        g = gold_domains(ds.outputs_dir / f"{tid}.json")
        if r is None and tid not in cached:
            # The method produced nothing for this task. That is a failure, not
            # an absence: it counts toward the denominator with every metric
            # false, so skipping hard tasks cannot raise a score.
            n_scored += 1
            rows.append({"task_id": tid, "table_identification": False if is_ours else None,
                         "table_correctness": False, "relationship_correctness": False,
                         "preparation_correctness": False,
                         "subtable_cov": None, "join_key": None,
                         "n_gold": len(gold_sets.get(tid, set())), "n_selected": 0,
                         "no_output": True})
            continue
        r = r or {"subtables": {}, "intermediates": [], "join_edges": [],
                  "selected_tables": [], "traced_keys": []}
        gold_tbl = gold_sets.get(tid, set())
        if is_ours:
            picked = {_tnorm(x) for x in r["selected_tables"]}
            ident = bool(gold_tbl) and picked == gold_tbl
            n_ident += int(ident)
        else:
            # A baseline emits code, not a table selection, so there is nothing
            # to compare. Reported as None rather than as a zero, which would
            # read as "it selected the wrong tables".
            picked, ident = set(), None

        tab = rel = prep = None
        s = {}
        hit = cached.get(tid) if not is_ours else None
        if hit is not None and hit.get("subtable_cov") is not None:
            s = {"subtable_cov": hit["subtable_cov"], "join_key": hit["join_key"]}
            n_scored += 1
            tab = s["subtable_cov"] >= 0.999
            rel = s["join_key"] is not None and s["join_key"] >= 0.999
            prep = bool(tab and rel)
            n_tab += int(tab); n_rel += int(rel); n_prep += int(prep)
        elif g and (g["cols"] or g["edges"]) and r.get("traced_keys") is not None or \
             (g and (g["cols"] or g["edges"]) and is_ours):
            pred = predicted_domains(r["subtables"], r["join_edges"],
                                     r.get("intermediates"))
            if r.get("traced_keys"):
                # A baseline declares no join edges; its keys are the operands of
                # the merges and isin filters it actually ran.
                for j in r["traced_keys"]:
                    for side in ("left", "right"):
                        v = normalise(j.get(side) or [])
                        if v:
                            pred["keys"].append(v)
            s = score_task(pred, g)
            n_scored += 1
            tab = (s["subtable_cov"] is not None and s["subtable_cov"] >= 0.999)
            rel = (s["join_key"] is not None and s["join_key"] >= 0.999)
            prep = bool(tab and rel)
            n_tab += int(tab); n_rel += int(rel); n_prep += int(prep)
            if not is_ours:
                new_scores.append({"task_id": tid,
                                   "subtable_cov": s.get("subtable_cov"),
                                   "join_key": s.get("join_key")})

        rows.append({"task_id": tid, "table_identification": ident,
                     "table_correctness": tab, "relationship_correctness": rel,
                     "preparation_correctness": prep,
                     "subtable_cov": s.get("subtable_cov"),
                     "join_key": s.get("join_key"),
                     "n_gold": len(gold_tbl), "n_selected": len(picked),
                     "no_output": False})

    if cache_path is not None and new_scores:
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        with cache_path.open("a", encoding="utf-8") as fh:
            for rec in new_scores:
                fh.write(json.dumps(rec) + "\n")
        print(f"[scorer] cached {len(new_scores)} baseline scores -> {cache_path}")

    n = len(ids)
    n_missing = sum(1 for r in rows if r.get("no_output"))
    return {"dataset": dataset, "source": source, "n_tasks": n, "n_scored": n_scored,
            "n_no_output": n_missing, "only_produced": only_produced,
            "table_identification_accuracy": (n_ident / n if (n and is_ours) else None),
            "table_correctness": n_tab / n_scored if n_scored else 0.0,
            "relationship_correctness": n_rel / n_scored if n_scored else 0.0,
            "preparation_correctness": n_prep / n_scored if n_scored else 0.0,
            "rows": rows}


def _tnorm(name) -> str:
    s = str(name).strip().split("/")[-1]
    if "#sep#" in s:
        s = s.split("#sep#")[-1]
    if s.lower().endswith(".pkl"):
        s = s[:-4]
    return s.upper()


def main() -> int:
    import argparse, csv
    from common import paths as P

    ap = argparse.ArgumentParser(
        description="Score this system and the baselines. No external evaluator.")
    ap.add_argument("--dataset", default="Synth-Bird")
    ap.add_argument("--source", default="self_correction",
                    help="Comma-separated methods to score and compare. This "
                         "system's own states are `no_self_correction` and "
                         "`self_correction`; any other name is a baseline under "
                         "baselines/baseline_results/ and is scored by EXECUTING "
                         "its generated code. `all` scores everything available.")
    ap.add_argument("--task-ids", nargs="+", default=None)
    ap.add_argument("--out", type=Path, default=None,
                    help="Per-task CSV. With several sources, one file per "
                         "source, suffixed with its name.")
    ap.add_argument("--timeout", type=int, default=120,
                    help="Per-task wall clock when executing a baseline.")
    ap.add_argument("--mem-gb", type=float, default=8.0,
                    help="Per-task address-space cap when executing a baseline.")
    ap.add_argument("--only-produced", action="store_true",
                    help="Score only the tasks the method produced output for, "
                         "instead of the whole benchmark. Answers 'when it does "
                         "answer, how good is it?' — NOT comparable against a "
                         "method scored the default way.")
    ap.add_argument("--list", action="store_true",
                    help="List the scorable methods and exit.")
    a = ap.parse_args()

    if a.list:
        print("this system :", ", ".join(sorted(OURS)))
        print("baselines   :", ", ".join(available_baselines()) or "none")
        return 0

    sources = ([s.strip() for s in a.source.split(",") if s.strip()]
               if a.source != "all"
               else sorted(OURS) + available_baselines())

    labels = [("table_identification_accuracy", "Table identification accuracy"),
              ("table_correctness", "Table correctness"),
              ("relationship_correctness", "Relationship correctness"),
              ("preparation_correctness", "Preparation correctness")]

    results = []
    for src in sources:
        try:
            res = evaluate(a.dataset, src, a.task_ids,
                           timeout=a.timeout, mem_gb=a.mem_gb,
                           only_produced=a.only_produced)
        except Exception as exc:  # noqa: BLE001
            print(f"[scorer] {src}: {type(exc).__name__}: {exc}")
            continue
        results.append(res)

        out = a.out
        if out and len(sources) > 1:
            out = Path(out).with_name(f"{Path(out).stem}_{src}{Path(out).suffix}")
        out = out or P.resolve(a.dataset, module="eval", group="").out(
            f"metrics_{src}.csv")
        Path(out).parent.mkdir(parents=True, exist_ok=True)
        with open(out, "w", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh)
            w.writerow(["metric", "value", "n"])
            for k, lab in labels:
                v = res[k]
                w.writerow([lab, "" if v is None else f"{v:.4f}",
                            res["n_tasks"] if k.startswith("table_ident") else res["n_scored"]])
            w.writerow([])
            w.writerow(["task_id", "table_identification", "table_correctness",
                        "relationship_correctness", "preparation_correctness",
                        "subtable_cov", "join_key", "n_gold", "n_selected"])
            for r in res["rows"]:
                w.writerow([r[k] for k in ("task_id", "table_identification",
                                           "table_correctness", "relationship_correctness",
                                           "preparation_correctness", "subtable_cov",
                                           "join_key", "n_gold", "n_selected")])
        res["_csv"] = str(out)

    if not results:
        return 1

    w = max(len(r["source"]) for r in results) + 2
    print(f"\n===== {a.dataset} =====")
    print(f"{'method':<{w}}{'n':>5}" + "".join(f"{lab.split()[0][:12]:>14}" for _, lab in labels))
    for r in results:
        cells = "".join(("{:>14}".format("-" if r[k] is None else f"{r[k]:.4f}"))
                        for k, _ in labels)
        print(f"{r['source']:<{w}}{r['n_scored']:>5}{cells}")
    miss = [r for r in results if r.get("n_no_output")]
    if miss:
        print("\n  tasks with no output from the method, counted as failures:")
        for r in miss:
            print(f"    {r['source']:<{w}} {r['n_no_output']}/{r['n_tasks']}")
    print("\n  columns: identification / table / relationship / preparation")
    print("  a dash means the method does not report that metric "
          "(baselines emit code, not a table selection)")
    for r in results:
        print(f"  {r['source']:<{w}} -> {r.get('_csv')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
