"""Dataset path resolution -- the single entry point shared by all modules.


Resolution order (each path resolves independently, so any one can be overridden):
  1. explicit CLI paths        --input-tables / --answer-dir / ...
  2. CLI data root             --data-root <dir>
  3. environment variable      PREPWEAVER_DATA_ROOT
  4. in-repo datasets/<Name>/  (when that subtree actually exists)
  (no machine-specific fallback: missing data is reported, never guessed)

So `--dataset Synth-Spider` runs on its own; point it elsewhere with
`--data-root` or per-path overrides, without editing code.
"""
from __future__ import annotations

import argparse
import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Iterator

REPO = Path(__file__).resolve().parents[2]
DATASETS = REPO / "datasets"

# Public name -> source benchmark name (older artefacts and the evaluator use the latter).
SOURCE_NAME = {
    "Synth-Bird": "nl2sql-bird",
    "Synth-Spider": "nl2sql-spider",
    "Beaver-Prep": "beaver",
}
NAMES = tuple(SOURCE_NAME)

# Built-in fallback roots, tried in order.
# No machine-specific fallback root. A path that happens to exist on one
# developer's laptop makes the repository "work on my machine" and hides a
# misconfiguration as a wrong-data run. Data is found under datasets/, or the
# user says where it is with PREPWEAVER_DATA_ROOT / --data-root.
_FALLBACK_ROOTS: tuple[Path, ...] = ()


@dataclass(frozen=True)
class Dataset:
    """Resolved paths and task list for one dataset."""

    name: str
    benchmark: Path
    input_tables: Path
    answer_dir: Path
    outputs_dir: Path
    db_dir: Path

    # ---- tasks ---------------------------------------------------------
    def tasks(self) -> list[dict]:
        return [json.loads(l) for l in self.benchmark.open() if l.strip()]

    def task_ids(self) -> list[str]:
        return [t["task_id"] for t in self.tasks()]

    def select(self, task_ids: Iterable[str] | None = None,
               limit: int = 0) -> list[dict]:
        """Subset by id or count. Order follows benchmark.jsonl, not the argument."""
        rows = self.tasks()
        if task_ids:
            want = set(task_ids)
            missing = want - {r["task_id"] for r in rows}
            if missing:
                raise KeyError(f"{self.name} has no such task_id: {sorted(missing)}")
            rows = [r for r in rows if r["task_id"] in want]
        return rows[:limit] if limit else rows

    # ---- files ---------------------------------------------------------
    def table(self, file_name: str) -> Path:
        return self.input_tables / file_name

    def target(self, task: dict | str) -> list[Path]:
        t = task if isinstance(task, str) else task.get("target_table")
        files = [t] if isinstance(t, str) else list(t or [])
        return [self.answer_dir / f for f in files]

    def gold_relations(self, task_id: str) -> dict | None:
        """`tables_rels/outputs/<task>.json`: gold subtables and join keys."""
        p = self.outputs_dir / f"{task_id}.json"
        return json.loads(p.read_text()) if p.exists() else None

    def gold_tables(self, task: dict) -> list[str]:
        """Gold table file names.

        Beaver stores them in `gold_tables` as `dw#sep#FCLT_ROOMS`; Synth-* use
        the positional convention (first `relevant_table_num` of `input_table`).
        """
        if task.get("gold_tables"):
            out = []
            for g in task["gold_tables"]:
                n = str(g).split("#sep#")[-1]
                out.append(n if n.endswith(".pkl") else n + ".pkl")
            return out
        n = int(task.get("relevant_table_num") or 0)
        return list(task.get("input_table") or [])[:n]

    def candidate_pool(self, task: dict) -> list[str]:
        """The candidate pool the system sees: Beaver `retrieved_table`, Synth-* `input_table`."""
        if task.get("retrieved_table"):
            return list(task["retrieved_table"])
        return list(task.get("input_table") or [])

    def missing(self) -> list[str]:
        """Resolved paths that do not exist, so callers can fail early."""
        return [f"{k}={v}" for k, v in (
            ("benchmark", self.benchmark), ("input_tables", self.input_tables),
            ("answer", self.answer_dir), ("outputs", self.outputs_dir),
            ("databases", self.db_dir)) if not v.exists()]


def _first_existing(cands: Iterator[Path]) -> Path | None:
    for c in cands:
        if c.exists():
            return c
    return None


def resolve(name: str, *, data_root: str | os.PathLike | None = None,
            benchmark: str | os.PathLike | None = None,
            input_tables: str | os.PathLike | None = None,
            answer_dir: str | os.PathLike | None = None,
            outputs_dir: str | os.PathLike | None = None,
            db_dir: str | os.PathLike | None = None) -> Dataset:
    if name not in SOURCE_NAME:
        raise ValueError(f"unknown dataset {name!r}; choose from: {', '.join(NAMES)}")

    roots: list[Path] = []
    if data_root:
        roots.append(Path(data_root).expanduser())
    env = os.environ.get("PREPWEAVER_DATA_ROOT")
    if env:
        roots.append(Path(env).expanduser())
    roots.append(DATASETS)
    roots.extend(_FALLBACK_ROOTS)

    src = SOURCE_NAME[name]

    def pick(sub_new: str, sub_old: str) -> Path:
        """Search each root: this repo's layout first, then the autoprep_publish layout."""
        hit = _first_existing(
            p for r in roots for p in (r / name / sub_new, r / src / "dev" / sub_old))
        # Nothing found: return the first candidate and let missing() report it.
        return hit or roots[0] / name / sub_new

    bench = Path(benchmark).expanduser() if benchmark else _first_existing(
        p for r in roots for p in (r / name / "benchmark.jsonl",
                                   r / src / "dev" / "benchmark.jsonl")
    ) or DATASETS / name / "benchmark.jsonl"

    return Dataset(
        name=name,
        benchmark=bench,
        input_tables=Path(input_tables).expanduser() if input_tables else pick("input_tables", ""),
        answer_dir=Path(answer_dir).expanduser() if answer_dir else pick("answer", ""),
        outputs_dir=Path(outputs_dir).expanduser() if outputs_dir else pick("tables_rels/outputs", "outputs"),
        db_dir=Path(db_dir).expanduser() if db_dir else pick("tables_rels/databases", ""),
    )


def add_arguments(ap: argparse.ArgumentParser) -> argparse.ArgumentParser:
    """Attach the shared dataset arguments to any subcommand."""
    g = ap.add_argument_group("dataset")
    g.add_argument("--dataset", required=True, choices=NAMES)
    g.add_argument("--data-root", default=None,
                   help="data root directory; also settable via PREPWEAVER_DATA_ROOT")
    g.add_argument("--benchmark", default=None, help="override benchmark.jsonl path")
    g.add_argument("--input-tables", default=None, help="override candidate table dir")
    g.add_argument("--answer-dir", default=None, help="override target table dir")
    g.add_argument("--outputs-dir", default=None, help="override gold relations dir")
    g.add_argument("--db-dir", default=None, help="override sqlite dir")
    g.add_argument("--task-ids", nargs="+", default=None, help="run only these tasks")
    g.add_argument("--limit", type=int, default=0, help="run only the first N tasks")
    return ap


def from_args(a: argparse.Namespace) -> Dataset:
    return resolve(a.dataset, data_root=a.data_root, benchmark=a.benchmark,
                   input_tables=a.input_tables, answer_dir=a.answer_dir,
                   outputs_dir=a.outputs_dir, db_dir=a.db_dir)
