#!/usr/bin/env python3
"""
model.py
========
Shared encoder over three evidence pairs, fused with the join-key numbers, into
two heads.

    ev_1 ─┐
    ev_2 ─┼─ SHARED encoder ─ mean-pool ─ SHARED proj 768->d ─┐
    ev_3 ─┘                                                   ├─ concat(3d + 9)
                                        jk[9] ────────────────┘
                                                     │
                                                  MLP trunk
                                                     ├── head_trigger  (1 logit)
                                                     └── head_router   (2 logits)

WHY ONE ENCODER AND ONE PROJECTION
----------------------------------
Three independent encoders is three times the parameters for a training set of
300 real states, and three independent projections is 147k parameters against
24.5k for a shared one. The grammar in `evidence_text.py` was made uniform for
exactly this reason: a column of a rejected table and a column of a produced
table are described identically, so what the encoder learns about columns
transfers between the passes rather than being learned three times.

WHY TWO HEADS AND NOT ONE THREE-WAY SOFTMAX
-------------------------------------------
The two decisions are calibrated against different things. The trigger's
operating point has to be set on the real, imbalanced distribution — 47.5% of
nl2sql-bird dev needs no revision — while any synthetic data is class-balanced
by construction. A single softmax couples them: the trigger threshold cannot
move without moving the routing. Measured on the earlier hand-feature setup, one
multiclass model reached 0.583 trigger AUC against 0.711 for two heads.

The router's loss is defined only on broken states, so it is masked and
normalised by the number of broken states in the batch. Dividing by batch size
instead lets a batch that happens to be mostly healthy silently shrink the
routing gradient.

WHY CHANNEL SELECTION IS A PENALTY AND NOT A GATE
-------------------------------------------------
The two channels carry different decisions. Measured with 20-seed random-readout
ensembles on dev: the text channel alone gives revise_table 19/32 — identical to
text+jk — and collapses to 16/42 on pipeline; the join keys alone give pipeline
25/42 and collapse to 12/32 on table. Each head should therefore weight the
channels differently.

The obvious construction is a learned sigmoid gate, `f' = sigmoid(a) * f`. It
does nothing here. The gate feeds a Linear, and `W (g * f) = (W diag(g)) f`, so
every gated model is a plain Linear with a different weight matrix — the trunk
could already zero the 96 text columns and does not. The shortfall is not
capacity, it is that 110 routing rows let text weights memorise instead of
vanishing, so the correction has to come from the OBJECTIVE.

Hence `group_lasso` (sum of per-block weight norms, which zeroes whole blocks
where per-element weight decay only shrinks) and `channel_dropout`. An
input-DEPENDENT gate `sigmoid(W_g f)` would be genuinely more expressive, since a
Linear cannot absorb a multiplicative interaction, but it costs ~11k parameters
against 110 rows and is not worth attempting at this scale.

MEAN-POOLING, NOT [CLS]
-----------------------
[CLS] is only meaningful once it has been fine-tuned into a sentence
representation. With the encoder frozen — the default here, because 300 states
cannot fine-tune 149M parameters — mean-pooling over the attention mask is the
better readout, and it stays reasonable when the encoder is later unfrozen.
"""
from __future__ import annotations

import contextlib
from dataclasses import dataclass
from typing import Any, Dict, Optional

import torch
import torch.nn as nn

BUNDLES = ("ev_1", "ev_2", "ev_3")


def masked_mean(h: torch.Tensor, mask: torch.Tensor) -> torch.Tensor:
    m = mask.unsqueeze(-1).to(h.dtype)
    return (h * m).sum(1) / m.sum(1).clamp(min=1e-6)


@dataclass
class Config:
    model_name: str = "answerdotai/ModernBERT-base"
    proj_dim: int = 32
    trunk_dim: int = 32
    jk_dim: int = 9
    dropout: float = 0.3
    freeze_encoder: bool = True
    jk_mean: tuple = ()        # per-feature train statistics, not per-sample
    jk_std: tuple = ()
    use_jk: bool = True
    use_bundles: tuple = BUNDLES
    hand_dim: int = 0          # >0 concatenates the incumbent 86 features
    channel_dropout: float = 0.0   # drop a whole channel, not single features
    split_router: bool = False     # ORACLE arm: router reads the join keys only


class Localizer(nn.Module):
    def __init__(self, cfg: Config, tokenizer_len: Optional[int] = None):
        super().__init__()
        from transformers import AutoModel
        self.cfg = cfg
        self.encoder = AutoModel.from_pretrained(cfg.model_name)
        if tokenizer_len is not None:
            self.encoder.resize_token_embeddings(tokenizer_len)
        hidden = self.encoder.config.hidden_size
        if cfg.freeze_encoder:
            for p in self.encoder.parameters():
                p.requires_grad_(False)
        self.proj = nn.Linear(hidden, cfg.proj_dim)
        fused = cfg.proj_dim * len(cfg.use_bundles) \
            + (cfg.jk_dim if cfg.use_jk else 0) + cfg.hand_dim
        # LayerNorm normalises ACROSS features WITHIN a sample. On learned
        # projections that is standard, but applied to the join-key ratios it
        # destroys them: a state whose jaccard, yield and containment are all low
        # is exactly what "broken" looks like, and per-sample normalisation
        # rescales that back to average. Mixing 9 interpretable ratios into the
        # same normalisation as 96 projection dimensions makes it worse. The
        # measured cost was 0.580 against 0.678 for logistic regression on the
        # identical nine numbers.
        #
        # So the text side keeps LayerNorm and the numeric side gets PER-FEATURE
        # standardisation from fixed training statistics, which is what the
        # sklearn baseline does.
        self.norm = nn.LayerNorm(cfg.proj_dim * len(cfg.use_bundles)) \
            if cfg.use_bundles else nn.Identity()
        jkm = torch.tensor(cfg.jk_mean or [0.0] * cfg.jk_dim, dtype=torch.float)
        jks = torch.tensor(cfg.jk_std or [1.0] * cfg.jk_dim, dtype=torch.float)
        self.register_buffer("jk_mean", jkm)
        self.register_buffer("jk_std", jks.clamp(min=1e-6))
        # A trunk PER HEAD, not one shared between them. Sharing was measured to
        # fail: the trigger loss sees all 198 rows and the router only the ~110
        # broken ones, so the trigger dominates the gradient and shapes the trunk
        # into a single "how broken" axis. The router then reads that axis
        # instead of a stage axis — on dev its p(revise_table) rose monotonically
        # with severity (0.195 healthy, 0.291 table, 0.346 pipeline) and
        # table-vs-pipeline AUC fell to 0.420, below chance and below always
        # answering "pipeline".
        #
        # The shared part is the ENCODER and the PROJECTION, which are feature
        # extraction. A trunk is already task-specific, and two tasks that
        # disagree about what to keep should not be forced through one.
        # Where each channel sits inside the fused vector, so a penalty or a mask
        # can address a whole channel rather than individual features.
        n_text = cfg.proj_dim * len(cfg.use_bundles)
        self.blocks: Dict[str, slice] = {}
        o = 0
        if n_text:
            self.blocks["text"] = slice(o, o + n_text); o += n_text
        if cfg.use_jk:
            self.blocks["jk"] = slice(o, o + cfg.jk_dim); o += cfg.jk_dim
        if cfg.hand_dim:
            self.blocks["hand"] = slice(o, o + cfg.hand_dim); o += cfg.hand_dim

        mk_trunk = lambda d: nn.Sequential(                            # noqa: E731
            nn.Linear(d, cfg.trunk_dim), nn.GELU(), nn.Dropout(cfg.dropout))
        self.trunk_trigger = mk_trunk(fused)
        # `router <- join keys only`. This began as a dev observation, so it was
        # first kept as an oracle ceiling, but it is now supported WITHOUT dev:
        # 5x5-fold cross-validation on the 166 broken TRAINING states routes at
        # .659 +- .007 from the nine ratios alone, against a .608 training
        # majority. Dev then reproduces the margin out of sample — .662 against a
        # .568 majority — so the dev number is a held-out result rather than the
        # thing that chose the design.
        #
        # Letting the model discover the split instead was tried and FAILED.
        # `group_lasso` with the sqrt-width weighting shrinks both blocks at an
        # identical per-column rate (ratio 1.00-1.04 at lam .01 and .03) because
        # the routing loss barely moves over 110 rows — the penalty becomes the
        # only force acting on the trunk, and a uniform force cannot select. The
        # split therefore has to be stated in the architecture.
        self.trunk_router = mk_trunk(cfg.jk_dim if cfg.split_router else fused)
        self.head_trigger = nn.Linear(cfg.trunk_dim, 1)
        self.head_router = nn.Linear(cfg.trunk_dim, 2)
        self.fused_dim = fused

    def _channel_dropout(self, f: torch.Tensor) -> torch.Tensor:
        """Zero an entire channel for a sample, never all of them at once.

        Ordinary dropout removes single features, which the remaining features in
        the same channel replace; it therefore cannot teach a head to work
        WITHOUT a channel. Only dropping the channel as a unit does that, and
        that is the pressure the router needs: on dev the text block is not just
        useless to it but harmful — a text-only random ensemble routes at .432,
        which is the degenerate "always answer revise_table".

        Inverted scaling keeps the expected activation constant. Refusing the
        all-dropped case makes the realised rate slightly below `p`, which errs
        towards less regularisation rather than more.
        """
        p = self.cfg.channel_dropout
        if not self.training or p <= 0 or len(self.blocks) < 2:
            return f
        keep = torch.rand(f.shape[0], len(self.blocks), device=f.device) >= p
        dead = ~keep.any(dim=1)
        if dead.any():                       # revive one channel at random
            j = torch.randint(0, len(self.blocks), (int(dead.sum()),), device=f.device)
            keep[dead, j] = True
        m = torch.ones_like(f)
        for i, sl in enumerate(self.blocks.values()):
            m[:, sl] = keep[:, i : i + 1].to(f.dtype)
        return f * m / (1.0 - p)

    def block_norms(self) -> Dict[str, torch.Tensor]:
        """L2 norm of each trunk's weight block, keyed `<head>.<channel>`.

        Summing these is the group lasso; reading them is the diagnostic. A
        per-element L2 (weight decay) shrinks everything a little and zeroes
        nothing, so it cannot express "this channel is not used". A sum of block
        NORMS is non-differentiable at zero for the block as a whole, which is
        exactly what drives a whole block out.
        """
        out = {}
        for h, trunk in (("trigger", self.trunk_trigger), ("router", self.trunk_router)):
            W = trunk[0].weight
            if h == "router" and self.cfg.split_router:
                out["router.jk"] = W.norm()
                continue
            for name, sl in self.blocks.items():
                out[f"{h}.{name}"] = W[:, sl].norm()
        return out

    def group_lasso(self) -> torch.Tensor:
        """Sum of block norms, each weighted by the square root of its width.

        The weight is not cosmetic. The subgradient of a block norm is
        `W_g / ||W_g||`, whose magnitude is 1 regardless of the block, so an
        unweighted sum shrinks every block at the same ABSOLUTE rate — which is a
        faster RELATIVE rate for whichever block is smaller. Measured without the
        weight at lam=0.1 over six epochs: the 96-wide text block fell 24% and
        the 9-wide join-key block fell 30%, i.e. the penalty preferentially
        removed the channel it was introduced to protect, and the per-column
        ratio ended at 0.91x when the hypothesis predicts it well above 1.

        `sqrt(|g|)` is the standard correction and makes the penalty comparable
        per column: the 96-wide block is charged 9.8x its norm against 3x for the
        9-wide one, so a text block that is merely as useful PER COLUMN as the
        join keys is the one that goes.
        """
        n = self.block_norms()
        w = {"text": self.cfg.proj_dim * len(self.cfg.use_bundles),
             "jk": self.cfg.jk_dim, "hand": self.cfg.hand_dim}
        return torch.stack([v * (w.get(k.split(".")[-1], 1) ** 0.5)
                            for k, v in n.items()]).sum()

    def encode(self, batch: Dict[str, Any]) -> torch.Tensor:
        text = []
        for b in self.cfg.use_bundles:
            ids, mask = batch[f"{b}_input_ids"], batch[f"{b}_attention_mask"]
            # `torch.enable_grad()` would OVERRIDE an ambient `no_grad()`, so an
            # unfrozen encoder built a graph and stored activations during
            # EVALUATION as well — 16 GB was exhausted in the epoch-0 eval, before
            # a single training step. `nullcontext` inherits the caller's mode,
            # which is what "train with grad, evaluate without" requires.
            ctx = (torch.no_grad() if self.cfg.freeze_encoder
                   else contextlib.nullcontext())
            with ctx:
                h = self.encoder(input_ids=ids, attention_mask=mask).last_hidden_state
            text.append(self.proj(masked_mean(h, mask)))
        parts = [self.norm(torch.cat(text, dim=-1))] if text else []
        if self.cfg.use_jk:
            parts.append((batch["jk"] - self.jk_mean) / self.jk_std)
        if self.cfg.hand_dim:
            parts.append(batch["hand"])
        return torch.cat(parts, dim=-1)

    def forward(self, batch: Dict[str, Any]) -> Dict[str, torch.Tensor]:
        f = self._channel_dropout(self.encode(batch))
        fr = f[:, self.blocks["jk"]] if self.cfg.split_router else f
        return {"trigger": self.head_trigger(self.trunk_trigger(f)).squeeze(-1),
                "router": self.head_router(self.trunk_router(fr))}

    def trainable_parameters(self):
        return [p for p in self.parameters() if p.requires_grad]


def losses(out: Dict[str, torch.Tensor], batch: Dict[str, Any],
           pos_weight: Optional[torch.Tensor] = None,
           lam: float = 1.0) -> Dict[str, torch.Tensor]:
    """Trigger BCE over the batch, router CE over the broken states only."""
    bce = nn.functional.binary_cross_entropy_with_logits(
        out["trigger"], batch["y_trigger"], pos_weight=pos_weight)
    m = batch["y_router"] >= 0
    if m.any():
        ce = nn.functional.cross_entropy(out["router"][m], batch["y_router"][m])
    else:
        ce = torch.zeros((), device=out["trigger"].device)
    return {"trigger": bce, "router": ce, "total": bce + lam * ce}
