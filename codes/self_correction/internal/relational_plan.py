"""Compatibility shim: the old `relational_plan` API over `relational_schema`.

`revise_table` produces a new table selection, and the repair loop must then
re-derive the relational schema from it. The research tree called
`synthesize_plan(question, tables, subquestions=..., bench_dir=...)`; the
Prep-Weaver equivalent is `pipeline_synthesize.relational_schema
.synthesize_schema(question, tables, tables_dir, ...)`.

The returned dict carries the schema under BOTH `tables` (the current key) and
`gold_tables` (the old one), because the engine's `map_task_from_spec` and parts
of the repair code still read the old name. It is the same list object, so they
cannot drift.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Iterable, Optional

from pipeline_synthesize import relational_schema as RS


def synthesize_plan(question: str,
                    table_files: Iterable,
                    *,
                    subquestions: Optional[dict] = None,
                    bench_dir: Optional[Path] = None,
                    tables_dir: Optional[Path] = None,
                    model: str = "gpt-4o-2024-08-06",
                    **kw) -> Dict[str, Any]:
    """Question + selected tables -> relational schema, in the old shape."""
    out = RS.synthesize_schema(
        question=question,
        table_files=table_files,
        tables_dir=tables_dir or bench_dir,
        subquestions=subquestions,
        model=model,
        **{k: v for k, v in kw.items()
           if k in {"temperature", "key_recovery", "is_warehouse",
                    "join_keys_path", "join_profile_path", "return_prompt"}},
    )
    out["gold_tables"] = out["tables"]      # same object, cannot drift
    out.setdefault("sql", "")               # this stage no longer produces one
    return out
