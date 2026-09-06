"""Export the synthesized pipelines and score them.

    export.py   pipeline.jsonl + relational_schema.jsonl -> one .py per task
    score.py    run those scripts under the external scorer and report

The scorer never reads a materialised DataFrame — it RE-EXECUTES the exported
source under a lineage tracer. So a run that was not exported cannot be scored
at all, and a script that does not reproduce the frame that was scored is worse
than no script.
"""

from __future__ import annotations

import sys
from pathlib import Path

# The exporter lives with the repair module and imports its neighbours by bare
# name; importing that package puts them on the path.
from self_correction import paths as _scp  # noqa: F401

__all__: list[str] = []
