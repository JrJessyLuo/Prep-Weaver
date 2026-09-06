"""Compatibility shim: the old `pipeline_synthesize` API over the new one.

NAMED `synthesis_shim`, NOT `pipeline_synthesize`. `codes/` sits ahead of
`internal/` on sys.path, so a shim called `pipeline_synthesize` is shadowed by
the real package of that name and `import pipeline_synthesize as PS` silently
binds the wrong module — which then has no `synthesize_pipeline` at top level.

The repair loop re-runs synthesis after `revise_table` or
`revise_relational_plan` changes the schema. It calls

    synthesize_pipeline(plan, task=..., raw_tables=..., bench_dir=...)

whereas the Prep-Weaver entry point takes `(schema, tables_dir, question=...,
db_id=...)`. This adapts one to the other so the loop's action code is unchanged.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Optional

from pipeline_synthesize import synthesize as PS

FIXED = PS.FIXED


def synthesize_pipeline(plan: Dict[str, Any],
                        *,
                        task: Optional[Dict[str, Any]] = None,
                        raw_tables: Optional[Dict[str, Any]] = None,
                        bench_dir: Optional[Path] = None,
                        tables_dir: Optional[Path] = None,
                        **kw) -> Dict[str, Any]:
    task = task or {}
    schema = dict(plan)
    # The loop's plans carry `gold_tables`; the new stage reads `tables`.
    if "tables" not in schema and schema.get("gold_tables"):
        schema["tables"] = schema["gold_tables"]
    return PS.synthesize_pipeline(
        schema,
        tables_dir or bench_dir,
        question=task.get("question", ""),
        db_id=task.get("db_id", ""),
        raw_tables=raw_tables,
        **{k: v for k, v in kw.items()
           if k in {"model", "workers", "repair_hints", "repair_joins_after",
                    "select_method"}},
    )
