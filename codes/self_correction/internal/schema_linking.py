"""Compatibility shim: the old `schema_linking` API over `table_discovery`.

`revise_table` re-runs table selection with extra evidence appended to the
prompt. It calls `link_schema_for_task(task, ..., prompt_suffix=...)`, which is
the interface the research tree had. Prep-Weaver's selector is
`table_discovery.table_selection`, whose signature differs (it takes a metadata
dict rather than reaching into a benchmark tree), so this module adapts one to
the other instead of editing `revise_table`.

The `prompt_suffix` hook is the whole point of the action: a repair must differ
from the first pass by the diagnostic EVIDENCE and nothing else, or an A/B
measures the prompt rewrite rather than the evidence.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Optional, Sequence

from common import dataset as DS
from table_discovery import table_selection as TS
from table_discovery.meta_inferrence import default_metadata_path, load_table_metadata

DEFAULT_MODEL = TS.DEFAULT_MODEL

_META_CACHE: Dict[str, Dict[str, dict]] = {}


def _metadata(dataset: str) -> Dict[str, dict]:
    """Offline table metadata for one dataset, read once per process."""
    if dataset not in _META_CACHE:
        _META_CACHE[dataset] = load_table_metadata(default_metadata_path(dataset))
    return _META_CACHE[dataset]


def link_schema(question: str,
                table_files: Sequence[str],
                *,
                dataset: str = "Synth-Bird",
                model: str = DEFAULT_MODEL,
                on_missing: str = "original",
                prompt_suffix: str = "",
                metadata: Optional[Dict[str, dict]] = None,
                join_keys_path: Optional[Path] = None,
                **_ignored) -> Dict[str, Any]:
    """Select tables for one question, with `prompt_suffix` appended verbatim.

    `on_missing` defaults to "original" here, not "error": a repair round must
    not abort because one candidate lacks metadata — it should fall back and say
    so, which `fell_back_to_original` records.
    """
    return TS.select_tables(
        question=question,
        table_files=table_files,
        metadata=metadata if metadata is not None else _metadata(dataset),
        dataset=dataset,
        model=model,
        on_missing=on_missing,
        join_keys_path=join_keys_path,
        prompt_suffix=prompt_suffix,
    )


def link_schema_for_task(task: Dict[str, Any],
                         *,
                         dataset: str = "Synth-Bird",
                         benchmark: str = "",
                         split: str = "dev",
                         candidate_tables: Optional[Sequence[str]] = None,
                         **kw) -> Dict[str, Any]:
    """`link_schema` for a benchmark task record.

    `benchmark` is accepted for call-site compatibility and mapped to a
    Prep-Weaver dataset name when one is not given directly.
    """
    if benchmark and dataset == "Synth-Bird":
        dataset = _dataset_for(benchmark) or dataset
    pool = list(candidate_tables or task.get("retrieved_table")
                or task.get("input_table") or [])
    res = link_schema(task.get("question", ""), pool, dataset=dataset, **kw)
    res["task_id"] = task.get("task_id")
    return res


def _dataset_for(benchmark: str) -> Optional[str]:
    """Old benchmark name -> Prep-Weaver dataset name."""
    for name, source in DS.SOURCE_NAME.items():
        if source == benchmark or name == benchmark:
            return name
    return None
