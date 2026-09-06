"""Where the self-correction module finds its models and inputs."""

from __future__ import annotations

import os
from pathlib import Path

MODULE_DIR = Path(__file__).resolve().parent
REPO_ROOT = MODULE_DIR.parents[1]
MODELS_DIR = Path(os.environ.get("PREPWEAVER_MODELS", REPO_ROOT / "models"))

# ---------------------------------------------------------------------------
# The localizer.
#
# The mainline localizer is the STAGED model: a frozen answerdotai/ModernBERT-base
# encoder (149M parameters) with LoRA adapters and task heads on top.
#
# The checkpoint stores ONLY the trainable tensors — LoRA weights, the heads, and
# the embeddings of the added marker tokens. The frozen encoder is reconstructed
# from its HuggingFace name, which is why the checkpoint is a few hundred KB
# rather than the ~600 MB a full state dict would be. So it belongs in the
# repository, and no external hosting is needed; `transformers` downloads and
# caches the base encoder on first use.
#
# Two files are required and must come from the SAME training run:
#   <name>.pt          trainable tensors + config + evidence spec
#   <name>.meta.json   special_tokens — the tokenizer must match exactly, or the
#                      marker tokens map to different ids and the heads read noise
# ---------------------------------------------------------------------------
LOCALIZER_CHECKPOINT = Path(
    os.environ.get("PREPWEAVER_LOCALIZER")
    or MODELS_DIR / "localizer_staged.pt"
)

LOCALIZER_META = Path(
    os.environ.get("PREPWEAVER_LOCALIZER_META")
    or str(LOCALIZER_CHECKPOINT).replace(".pt", ".meta.json")
)


def localizer_available() -> bool:
    """Whether the LOCAL staged model can be loaded. The remote arm needs only
    a reachable endpoint, and checks that itself."""
    return LOCALIZER_CHECKPOINT.exists() and LOCALIZER_META.exists()


def describe() -> str:
    ok = localizer_available()
    lines = [f"[self-correction] localizer   : {LOCALIZER_CHECKPOINT} "
             f"({'found' if LOCALIZER_CHECKPOINT.exists() else 'MISSING'})",
             f"[self-correction] localizer meta: {LOCALIZER_META} "
             f"({'found' if LOCALIZER_META.exists() else 'MISSING'})"]
    if not ok:
        lines.append(
            f"[self-correction] no localizer checkpoint at {MODELS_DIR}. It ships "
            "with the repository; if it is missing, re-clone or point "
            "PREPWEAVER_LOCALIZER at it.")
    return "\n".join(lines)
