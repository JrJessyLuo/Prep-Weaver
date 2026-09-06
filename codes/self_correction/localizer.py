"""Loading the localizer that decides WHICH action to take.

The mainline is the STAGED model: a frozen `answerdotai/ModernBERT-base` encoder
with LoRA adapters and task heads. It reads the diagnosed state and returns a
posterior over

    revise_table | revise_relational_plan | revise_pipeline | no_revision_needed

Two numbers come out of it, and they are used for different things:

    rank(...)   orders the actions. Ranking, not classifying: four-class accuracy
                is 0.618 but hit@2 is 0.80 and expected rounds-to-hit is 1.68,
                which is why the tree tries and rolls back rather than trusting
                one label.
    p_ok(...)   P(no_revision_needed) on a state — the only correctness estimate
                available without gold, and the tree's node score.

THE CHECKPOINT
--------------
It stores only the TRAINABLE tensors: LoRA weights, the heads, and the
embeddings of the added marker tokens. The 149M-parameter encoder is rebuilt
from its HuggingFace name, so the file is a few hundred KB rather than ~600 MB.
Two files, from the SAME training run:

    <name>.pt          trainable tensors + config + evidence spec
    <name>.meta.json   special_tokens

The tokenizer must match exactly; a mismatched meta maps the marker tokens to
different ids and the heads then read noise rather than failing loudly.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Optional, Sequence, Tuple

from . import paths as SCP

OK = "no_revision_needed"
ACTIONS = ("revise_table", "revise_relational_plan", "revise_pipeline", OK)


def load_localizer(kind: str = "staged",
                   checkpoint: Optional[Path] = None,
                   meta: Optional[Path] = None,
                   *,
                   anonymize: bool = True,
                   device: Optional[str] = None,
                   **kw):
    """Build a localizer.

    kind="staged"  the trained ModernBERT model (the mainline)
    kind="llm"     an LLM asked for the label — the comparison baseline. It emits
                   a LABEL, not a comparable score, so the tree falls back to
                   "first state the localizer calls fixed" for selection.

    The staged model runs locally: the checkpoint is 86 KB and the frozen
    encoder is downloaded and cached by `transformers`, so a forward pass takes
    seconds on CPU, MPS or CUDA. There is no serving step.
    """
    if kind == "staged":
        ck = Path(checkpoint or SCP.LOCALIZER_CHECKPOINT)
        mt = Path(meta or SCP.LOCALIZER_META)
        if not ck.exists() or not mt.exists():
            raise FileNotFoundError(
                f"staged localizer not found.\n{SCP.describe()}")
        from loop_localizer import StagedLoopLocalizer
        return StagedLoopLocalizer(ck, mt, device=device, anonymize=anonymize)

    if kind == "llm":
        from loop_localizer import LLMLoopLocalizer
        return LLMLoopLocalizer(**kw)

    raise ValueError(f"unknown localizer kind {kind!r}")


def rank_fn(loc):
    """(diag, state, exclude) -> [(action, prob), ...], best first."""
    def rank(diag, state, exclude: Sequence[str] = ()):
        link = getattr(state, "link", None)
        try:
            if getattr(loc, "wants_state", False):
                return loc.rank(diag, exclude=tuple(exclude), link=link, state=state)
            return loc.rank(diag, exclude=tuple(exclude), link=link)
        except TypeError:
            return loc.rank(diag, exclude=tuple(exclude))
    return rank


def p_ok_fn(loc):
    """(diag, state) -> P(no_revision_needed).

    A localizer that emits only a label has no comparable scalar; 1.0/0.0 is
    used so the tree can still order states, and `emits_score` tells the caller
    that ordering is a label, not a probability.
    """
    def p_ok(diag, state):
        try:
            if getattr(loc, "wants_state", False):
                return float(loc.p_ok(diag, state=state))
            return float(loc.p_ok(diag))
        except AttributeError:
            r = rank_fn(loc)(diag, state)
            return float(dict(r).get(OK, 0.0))
    return p_ok
