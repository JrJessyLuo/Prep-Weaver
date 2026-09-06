"""Shared helpers for every Prep-Weaver module.

    dataset     benchmark.jsonl, input tables, targets, gold relations
    paths       profiling inputs and per-module output directories
    io_utils    JSON / JSONL helpers
    llm_client  OpenAI-compatible chat client

`dataset` resolves a dataset's DATA (tables, answers, relations); `paths`
resolves a dataset's PROFILING inputs and a module's RESULT directory. Both are
addressed by dataset name alone, with every path overridable.
"""

from .dataset import Dataset, add_arguments, from_args, resolve, NAMES, SOURCE_NAME
from . import io_utils, llm_client, paths

__all__ = [
    "Dataset", "add_arguments", "from_args", "resolve", "NAMES", "SOURCE_NAME",
    "io_utils", "llm_client", "paths",
]
