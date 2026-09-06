"""Where the engine finds its own files.

The engine was extracted from a research tree in which every module resolved
its resources through NOVELPREP_ROOT / AUTOPREP_ROOT. Inside Prep-Weaver those
roots do not exist, so this module is the single place that says where things
are now. Each constant still honours its original environment variable, so a
checkout of the original tree keeps working.
"""

from __future__ import annotations

import os
from pathlib import Path

# <repo>/codes/pipeline_synthesize/engine/paths.py -> <repo>
ENGINE_DIR = Path(__file__).resolve().parent
REPO_ROOT = ENGINE_DIR.parents[2]

# Trained operator-selection classifier (~12 MB, versioned with the repo).
POLICY_MODEL = Path(
    os.environ.get("PREPWEAVER_POLICY_MODEL")
    or os.environ.get("MULTISTEP_MODEL_PATH")
    or REPO_ROOT / "models" / "model_multistep_m4_prefix_history.joblib"
)

# Single-operation classifier, used by SingleOpInfer (~3 MB). A SECOND model:
# the multistep policy above predicts the next op given the chain prefix, this
# one scores a single operation in isolation, and six engine modules import it.
SINGLE_OP_MODEL = Path(
    os.environ.get("PREPWEAVER_SINGLE_OP_MODEL")
    or os.environ.get("SINGLE_OP_MODEL_PATH")
    or REPO_ROOT / "models" / "model.joblib"
)

# Per-task operation details, indexed by task_id and read by SingleOpInfer at
# construction time (~850 KB).
OPERATION_DETAILS = Path(
    os.environ.get("PREPWEAVER_OPERATION_DETAILS")
    or ENGINE_DIR / "resources" / "operation_details.jsonl"
)

# Per-operation usage examples shown to the parameter-synthesis LLM.
USAGE_EXAMPLES_DIR = Path(
    os.environ.get("PREPWEAVER_USAGE_EXAMPLES")
    or ENGINE_DIR / "resources" / "operation_usage_examples"
)

# Raw table collections. Left as an override only: the Prep-Weaver entry points
# pass an explicit tables directory, and nothing on the synthesis path should
# reach into a benchmark tree on its own.
AUTOPREP_ROOT = Path(os.environ.get("AUTOPREP_ROOT", REPO_ROOT / "datasets"))

# Ground-truth schema files, used only by the schema-alignment path. Alignment
# is hard-disabled during synthesis (it rewrites a predicted schema into the
# database's real one, which a deploy-time action must not do), so these are
# unset unless someone opts in explicitly.
SPIDER_TABLES = os.environ.get("SPIDER_TABLES_JSON", "")
SPIDER_TEST_TABLES = os.environ.get("SPIDER_TEST_TABLES_JSON", "")
BIRD_DEV_TABLES = os.environ.get("BIRD_DEV_TABLES_JSON", "")


def describe() -> str:
    return (f"[engine] policy model : {POLICY_MODEL} "
            f"({'found' if POLICY_MODEL.exists() else 'MISSING'})\n"
            f"[engine] single-op model: {SINGLE_OP_MODEL} "
            f"({'found' if SINGLE_OP_MODEL.exists() else 'MISSING'})\n"
            f"[engine] operation details: {OPERATION_DETAILS} "
            f"({'found' if OPERATION_DETAILS.exists() else 'MISSING'})\n"
            f"[engine] usage examples: {USAGE_EXAMPLES_DIR} "
            f"({len(list(USAGE_EXAMPLES_DIR.glob('*.md'))) if USAGE_EXAMPLES_DIR.exists() else 0} files)")
