"""Run a baseline's generated code and capture what it produced.

Our own runs are scored from their recorded artefacts — the operator chain is
stored, so the frames can be replayed. A baseline hands us arbitrary pandas
instead, so the only way to see what it produced is to RUN it and watch.

Two things have to be observed, and they need different mechanisms:

    tables   every DataFrame the code ends up holding. Collected from the
             module namespace after execution, plus anything it assigned to
             `result` or `tables`.

    joins    the key columns of every join it performed. These cannot be read
             off the final frames: after a merge the two key columns have
             usually been collapsed into one, and a key that was filtered
             through `isin` never appears as a column at all. So `pd.merge`,
             `DataFrame.merge`, `DataFrame.join` and `Series.isin` are wrapped
             for the duration of the call and record their operands' values.

The patching is process-global while the code runs, and undone in a `finally`.
Baselines are executed one at a time for that reason.

SAFETY
------
This executes third-party generated code. It runs with a wall-clock alarm and
an address-space cap, and a task that exceeds either is recorded as a failure
rather than being allowed to take the run down. It is NOT a sandbox: only run
code you are willing to execute.
"""

from __future__ import annotations

import contextlib
import io
import os
import resource
import signal
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

import pandas as pd


class _Timeout(Exception):
    pass


def _install_optional_stubs() -> None:
    """Stand-ins for plotting / analysis packages a generated script may import.

    Some baseline code imports a library only to draw a figure it never returns.
    A missing import would abort the whole script and score the task as a total
    failure, when the data preparation it performed may have been fine. The
    stubs accept any call and return something inert, so the import succeeds and
    the preparation still runs.
    """
    import sys
    import types

    if "PyComplexHeatmap" not in sys.modules:
        m = types.ModuleType("PyComplexHeatmap")

        class _Dummy:
            def __init__(self, *a, **k):
                pass

            def __repr__(self):
                return "<stub>"

        m.oncoPrintPlotter = lambda *a, **k: _Dummy()
        sys.modules["PyComplexHeatmap"] = m

    if "lifelines" not in sys.modules:
        m = types.ModuleType("lifelines")

        class KaplanMeierFitter:
            def __init__(self, *a, **k):
                pass

            def fit(self, *a, **k):
                return self

            def plot_survival_function(self, *a, **k):
                return None

        m.KaplanMeierFitter = KaplanMeierFitter
        sys.modules["lifelines"] = m


@contextlib.contextmanager
def _limits(seconds: int, mem_gb: float):
    def _alarm(_sig, _frm):
        raise _Timeout(f"exceeded {seconds}s")

    old = signal.signal(signal.SIGALRM, _alarm)
    signal.alarm(seconds)
    soft = hard = None
    if mem_gb:
        try:
            soft, hard = resource.getrlimit(resource.RLIMIT_AS)
            resource.setrlimit(resource.RLIMIT_AS, (int(mem_gb * 2**30), hard))
        except (ValueError, OSError):
            soft = None
    try:
        yield
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, old)
        if soft is not None:
            with contextlib.suppress(Exception):
                resource.setrlimit(resource.RLIMIT_AS, (soft, hard))


def _vals(obj) -> List[str]:
    try:
        if isinstance(obj, pd.DataFrame):
            obj = obj.iloc[:, 0]
        s = pd.Series(obj).dropna()
        if len(s) > 20000:
            s = s.sample(20000, random_state=0)
        return s.astype(str).drop_duplicates().tolist()
    except BaseException:
        return []


@contextlib.contextmanager
def _watch_joins(sink: List[dict]):
    """Record the operands of every merge / join / isin performed inside."""
    orig_merge_fn = pd.merge
    orig_merge_m = pd.DataFrame.merge
    orig_join_m = pd.DataFrame.join
    orig_isin = pd.Series.isin

    def _keys(left, right, on, left_on, right_on):
        lk = left_on or on
        rk = right_on or on
        lk = [lk] if isinstance(lk, str) else list(lk or [])
        rk = [rk] if isinstance(rk, str) else list(rk or [])
        for a, b in zip(lk, rk or lk):
            try:
                sink.append({"left": _vals(left[a]), "right": _vals(right[b])})
            except Exception:
                pass

    def merge_fn(left, right, *a, **kw):
        with contextlib.suppress(Exception):
            _keys(left, right, kw.get("on"), kw.get("left_on"), kw.get("right_on"))
        return orig_merge_fn(left, right, *a, **kw)

    def merge_m(self, right, *a, **kw):
        with contextlib.suppress(Exception):
            _keys(self, right, kw.get("on"), kw.get("left_on"), kw.get("right_on"))
        return orig_merge_m(self, right, *a, **kw)

    def join_m(self, other, *a, **kw):
        with contextlib.suppress(Exception):
            on = kw.get("on")
            if on is not None:
                _keys(self, other, on, None, None)
        return orig_join_m(self, other, *a, **kw)

    def isin_m(self, values):
        # A semi-join: the key never survives as a column, but both sides of the
        # comparison are exactly the join-key value domains.
        with contextlib.suppress(Exception):
            if not isinstance(values, dict):
                sink.append({"left": _vals(self), "right": _vals(list(values))})
        return orig_isin(self, values)

    pd.merge = merge_fn
    pd.DataFrame.merge = merge_m
    pd.DataFrame.join = join_m
    pd.Series.isin = isin_m
    try:
        yield
    finally:
        pd.merge = orig_merge_fn
        pd.DataFrame.merge = orig_merge_m
        pd.DataFrame.join = orig_join_m
        pd.Series.isin = orig_isin


def run_code(code: str, tables: Dict[str, pd.DataFrame],
             timeout: int = 120, mem_gb: float = 8.0) -> dict:
    """Execute one baseline's code. Returns {frames, joins, result, error}."""
    _install_optional_stubs()
    joins: List[dict] = []
    ns: Dict[str, Any] = {"tables": tables, "__name__": "__baseline__"}
    err = None
    try:
        with _limits(timeout, mem_gb), _watch_joins(joins), \
                contextlib.redirect_stdout(io.StringIO()), \
                contextlib.redirect_stderr(io.StringIO()):
            exec(compile(code, "<baseline>", "exec"), ns)
    except BaseException as exc:            # noqa: BLE001 - incl. timeout, MemoryError
        err = f"{type(exc).__name__}: {exc}"

    frames: List[pd.DataFrame] = []
    seen = set()

    def _add(obj):
        if isinstance(obj, pd.DataFrame) and id(obj) not in seen:
            seen.add(id(obj))
            frames.append(obj)

    res = ns.get("result")
    if isinstance(res, dict):
        for v in res.values():
            _add(v)
    else:
        _add(res)
    for k, v in ns.items():
        if k in ("tables", "__builtins__"):
            continue
        _add(v)
        if isinstance(v, dict):
            for x in v.values():
                _add(x)
        elif isinstance(v, (list, tuple)):
            for x in v:
                _add(x)
    return {"frames": frames, "joins": joins, "result": res, "error": err}
