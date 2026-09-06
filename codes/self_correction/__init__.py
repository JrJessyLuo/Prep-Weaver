"""Self-correction: diagnose a synthesized pipeline, revise it, keep what helps.

    revise_table            re-select the input tables, fed the diagnosis
    revise_relational_plan  revise the declared schema and join edges
    revise_pipeline_code    rewrite one table's pipeline as pandas

`tree.py` drives them: every node is one round's state, and the search expands
in depth (revise the best state again) and in breadth (try other actions from
the same state).

WHY THE INTERNALS ARE FLAT
--------------------------
`internal/` holds the diagnostic, evidence, scoring and localizer code lifted
from the research tree. Those modules import each other by bare name, so this
package puts `internal/` on `sys.path` rather than rewriting ~6,000 lines of
measured code into relative imports. Three of the modules there are shims that
map the old `schema_linking` / `relational_plan` / `pipeline_synthesize` names
onto Prep-Weaver's `table_discovery` and `pipeline_synthesize`, so the action
code connects to the new stages unchanged.
"""

from __future__ import annotations

import sys
from pathlib import Path

# The engine first: this module replays operator chains and re-runs synthesis,
# so it needs `test_param_synthesis`, `table_executor` and the rest on the path.
# Importing it also pins the policy models and the usage examples.
from pipeline_synthesize import engine  # noqa: F401

# Only `internal/` goes on the flat path. Adding this package's own directory
# too would expose `paths.py`, `tree.py`, `actions.py` under bare names where
# they can shadow an engine module of the same name.
_HERE = Path(__file__).resolve().parent
_INTERNAL = _HERE / "internal"
if str(_INTERNAL) not in sys.path:
    sys.path.insert(0, str(_INTERNAL))

from . import paths  # noqa: E402

__all__ = ["paths"]
