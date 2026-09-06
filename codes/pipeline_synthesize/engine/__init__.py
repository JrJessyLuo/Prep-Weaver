"""The pipeline-synthesis search engine, extracted from the research tree.

This package holds the machinery stage 2 runs on: the bounded beam search over
operator chains, the operator library and executor, the LLM parameter
synthesizer, the feature extractor and trained policy, the join-key repair, and
the schema conformance pass.

WHY THE MODULES ARE FLAT
------------------------
The twenty modules here import each other by bare name (`import full_pipeline`,
`from phase2_joinkey import repair_joins`), as they did in the tree they came
from. Rewriting ~7,000 lines of working, measured code into relative imports
would be a large edit whose only benefit is style, and every such edit is a
chance to break something that currently works. So the layout is preserved and
this file puts the package directory on `sys.path`, which makes both forms
resolve:

    from pipeline_synthesize.engine import bounded_explore_loop   # packaged
    import bounded_explore_loop                                   # internal

Importing this package therefore has the side effect of extending `sys.path`.
That is deliberate and is the price of not rewriting the engine.

CONFIGURATION
-------------
`engine_paths.py` is the single place that resolves the engine's own files (the
two trained classifiers, the operation details, the operator usage examples).
The original NOVELPREP_ROOT / AUTOPREP_ROOT environment variables still work as
overrides. The name is deliberately not `paths`: this directory goes on
`sys.path`, so a bare `paths` would collide with any other module of that name
that another package puts there — which it did, silently, with
`self_correction/paths.py`.

The environment switches below were passed on every recorded run, so they are
defaults here rather than flags:

    CHAIN_CAPTURE_PREVIEW  keep a small table preview per chain step
    SYNTH_CACHE            memoise parameter synthesis on (op, columns, frame hash)
    WIDEN_JOINKEY_CANDS    keep top-5 candidates while a declared join key is
                           still MISSING from the frame, instead of collapsing to
                           top-1 when the classifier is confident
    MULTISTEP_MODEL_PATH   must be set BEFORE multistep_loop is imported: that
                           module reads it into a module-level constant at import
                           time, so setting it afterwards has no effect
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

from . import engine_paths  # noqa: E402

os.environ.setdefault("CHAIN_CAPTURE_PREVIEW", "1")
os.environ.setdefault("SYNTH_CACHE", "1")
os.environ.setdefault("WIDEN_JOINKEY_CANDS", "1")
os.environ.setdefault("MULTISTEP_MODEL_PATH", str(engine_paths.POLICY_MODEL))

__all__ = ["engine_paths"]
