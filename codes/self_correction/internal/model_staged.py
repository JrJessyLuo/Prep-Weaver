#!/usr/bin/env python3
"""
model_staged.py
===============
One scorer per class, each reading the evidence that class is about.

    ev_1  selected + rejected raw tables ─ enc ─ proj ─┬─────────────► z_table
    ev_2  declared schema ─────────────── enc ─ proj ─┤
    ev_3  produced tables ─────────────── enc ─ proj ─┼─┬───────────► z_pipeline
    jk[9] join-key ratios ───────────────────────────┴─┴─┬─────────► z_ok
                                                         │
                              softmax(z_ok, z_table, z_pipeline)

    p_trigger = 1 - P(ok)          p_router = softmax(z_table, z_pipeline)

WHY EACH CLASS GETS ITS OWN EVIDENCE
------------------------------------
The channels are not interchangeable, and each carries one class. Measured with
20-seed random-readout ensembles on dev: text alone gives revise_table 19/32,
identical to text+jk, and collapses to 16/42 on pipeline; the join keys alone
give pipeline 25/42 and collapse to 12/32 on table. The join keys are worse than
useless for routing to `revise_table` — their revise_table AUC is .342, i.e.
significantly INVERTED, because a join-key ratio measures whether the join works,
which is a statement about the pipeline.

The fused model concatenated all of it into 105 dimensions and asked one MLP to
learn, from 110 broken rows, that it should read text for one class and join keys
for the other. It did not. Every attempt to make it failed and is recorded:
splitting the trunks fixed an inverted router (.420 -> .635 AUC) without moving a
single recalled task; `group_lasso` with the sqrt-width weighting shrank both
blocks at an identical per-column rate (1.00-1.04) because the routing loss
barely moves over 110 rows; and hard-wiring the router to the join keys alone
raised routing ACCURACY to .662 while dropping correct `revise_table` actions
from 10/32 to 6/32, since the accuracy was bought by answering the majority class.

A channel assignment that is known does not need to be learned from data that
cannot support learning it. It is stated here instead.

WHY ONE THREE-WAY SOFTMAX AND NOT TWO HEADS
-------------------------------------------
This reverses an earlier decision, because the metric that justified it was the
wrong one. Two heads were chosen when the target was RECALL AT BUDGET, where the
trigger's operating point and the routing are genuinely separate concerns. The
deliverable is CORRECT ACTIONS — a task counts only if it is both acted on and
routed to the right stage — and under that metric the two decisions are one
decision, so a single distribution over {ok, table, pipeline} is the honest model.

It is also worth roughly 1.8x the supervision. With two heads the router's loss
is masked to the broken rows, so 111 of 247 training states say nothing at all
about routing. Under a three-way softmax a healthy state pushes z_ok up relative
to BOTH z_table and z_pipeline, which shapes the same boundary the router reads.
With 247 rows, throwing 111 of them away on the harder of the two decisions is
not affordable.

CAPACITY
--------
Small on purpose, and by measurement rather than taste: on identical inputs an
87-parameter logistic regression beat a 1.18M-parameter LoRA model on the class
that matters (revise_table 20/32 against 18/32), while the LoRA model's trigger
training loss fell only from .613 to .553 over 20 epochs — it could not fit the
training set either. The default here is a frozen encoder with proj_dim 16 and
per-class trunks of 16, about 13k trainable parameters. `--lora` is still
available and is a hypothesis to test, not the default.

WHAT COMES NEXT PLUGS IN HERE
-----------------------------
`z_table` is computed from ev_1 alone, so the stage-1 contrastive pairs — 54
same-task states differing only in one swapped table — supervise exactly this
scalar and nothing else. Under the fused model that gradient would have been
diluted across a 105-dimensional vector shared with the pipeline decision.
"""
from __future__ import annotations

import contextlib
from dataclasses import dataclass, field
from typing import Any, Dict, Optional, Sequence

import torch
import torch.nn as nn

BUNDLES = ("ev_1", "ev_2", "ev_3")
CLASSES = ("no_revision_needed", "revise_table", "revise_pipeline")

# Which evidence each class's scorer reads. `z_ok` sees everything because
# "nothing is wrong" is a claim about every stage at once, while each failure
# class is a claim about one place.
# `tk` is the same idea as `jk`, applied to the other class. The nine join-key
# ratios exist because a pooled sentence embedding cannot judge whether a join
# holds — that is arithmetic over columns, not semantics. `revise_table` fails
# for the same reason and one level up: the discriminating quantities are
# aggregates ACROSS columns (min/max/mean of per-column nonnull, unique,
# verbatim fractions), and while every one of those per-column numbers is already
# written into the evidence text, mean-pooling a transformer over a page of
# `nonnull=0.97` tokens does not compute their minimum.
#
# So `tk` is not "we added hand features". It supplies the one class of
# computation the encoder is structurally unable to perform, under the same
# admission rule that made `jk` transferable: a feature enters only if it
# separates the classes AND does NOT separate the training split from dev. That
# screen is not cosmetic — the two strongest raw signals, `A1_declared_columns`
# (.697) and `B_cols__max` (.652), are both COUNTS and both fail it at domain AUC
# .738 and .799. Dropping them costs nothing: the domain-clean pool scores .468
# macro against .473 for all 86, and better on revise_table, .471 against .462.
EVIDENCE = {
    "table":    {"bundles": ("ev_1",),                "jk": False, "tk": True},
    "pipeline": {"bundles": ("ev_3",),                "jk": True,  "tk": False},
    "ok":       {"bundles": ("ev_1", "ev_2", "ev_3"), "jk": True,  "tk": False},
}


def masked_mean(h: torch.Tensor, mask: torch.Tensor) -> torch.Tensor:
    m = mask.unsqueeze(-1).to(h.dtype)
    return (h * m).sum(1) / m.sum(1).clamp(min=1e-6)


def masked_max(h: torch.Tensor, mask: torch.Tensor) -> torch.Tensor:
    return h.masked_fill(~mask.unsqueeze(-1).bool(), float("-inf")).max(1).values


def pool(h: torch.Tensor, mask: torch.Tensor, how: str) -> torch.Tensor:
    """Readout over the token sequence.

    MEAN IS THE SUSPECT, AND THIS SWITCH IS WHY
    -------------------------------------------
    The two classes have different logical forms. `revise_pipeline` is a global
    property — the produced tables are wrong, the join is unhealthy — and an
    average represents that fine. `revise_table` is EXISTENTIAL and about an
    ABSENCE: some table the question needs was not selected. A missing table
    contributes nothing to a sum, so no average over the present tokens can
    reveal it, and one absent table among six is washed out regardless.

    The measured split matches exactly: across three seeds `revise_pipeline` F1
    sits at .486-.492 while `revise_table` F1 is .350 in every one of them —
    below the .370 that answering `revise_table` for everything scores.

    A second, cruder problem points the same way. ev_1 runs to a median 2126
    tokens against 20-40 for the question, so under a mean the question — which
    is the only thing that says which tables are NEEDED — contributes under 2% of
    the readout. The same effect was measured directly once before: embedding the
    rejected tables alone gave revise_table AUC .945, and pooling the question in
    with them dropped it to .545.

        mean   the incumbent
        max    can express "one span here is very wrong", which is the shape of
               an existential predicate
        cls    the standard fine-tuned readout; meaningful because this is a
               cross-encoder, not the frozen bi-encoder [CLS] would be useless on
        mean+max  concatenated, projected back down — keeps the global signal
               `revise_pipeline` needs while adding the existential one

    This is an ablation, not a fix: three independent method families all land
    within .05 of the constant baseline on `revise_table`, so the ceiling here is
    about .42. A better readout can explain why we are the worst of the four; it
    cannot move that ceiling.
    """
    if how == "mean":
        return masked_mean(h, mask)
    if how == "max":
        return masked_max(h, mask)
    if how == "cls":
        return h[:, 0]
    if how == "mean+max":
        return torch.cat([masked_mean(h, mask), masked_max(h, mask)], dim=-1)
    raise ValueError(f"unknown pooling {how!r}")


@dataclass
class StagedConfig:
    model_name: str = "answerdotai/ModernBERT-base"
    proj_dim: int = 16
    trunk_dim: int = 16
    jk_dim: int = 9
    dropout: float = 0.2
    freeze_encoder: bool = True
    pooling: str = "mean"          # mean | max | cls | mean+max — see `pool`
    tk_idx: tuple = ()             # indices into the exported `hand` vector
    tk_mean: tuple = ()            # per-feature train statistics, as for jk
    tk_std: tuple = ()
    jk_mean: tuple = ()
    jk_std: tuple = ()
    # --- per-table head ------------------------------------------------------
    # `revise_table` is an EXISTENTIAL claim — some rejected table is one the
    # question needs — and the state-level scorer has to certify it from a single
    # vector pooled over a 2000-token page holding six tables. Measured, it does
    # not: every neural arm predicts the class 8-9 times in 141 and the correct
    # ones are exactly the 7 dev tasks with `n_selected < 2`, i.e. the model
    # learned a table-COUNT rule and nothing about which table is missing. On the
    # 134 tasks where that rule does not fire, F1_table is exactly .000, against
    # .578 for gpt-5, whose stated reasons name the specific rejected table.
    #
    # The head below moves the decision to where the label lives. Cutting ev_1 at
    # its `[TABLE]` markers gives one vector per table; a shared linear scorer
    # says "this rejected table is needed"; the state-level score is the
    # log-sum-exp of those, which is a soft OR — differentiable, and unlike a
    # hard max it does not send the whole gradient down one path.
    #
    # It is also 20x the supervision from the same annotation: 1277 per-table
    # instances against 65 state-level `revise_table` labels, at no labelling
    # cost, because `tables_1` records which tables were gold and which were
    # rejected for every state we already exported.
    per_table: bool = False
    lambda_tab: float = 1.0    # weight on the per-table BCE; 0 = pure MIL
    tab_pos_weight: float = 1.0
    mil_only: bool = False     # drop the pooled state-level path for z_table
    # 0 = no projection: the head is Linear(hidden, 1) straight off the segment
    # mean. THE BOTTLENECK WAS THE BUG. Sharing `self.proj` put the per-table
    # score behind a 16-dim projection that three state-level scorers were also
    # pulling on under a three-way CE, and it cost almost everything: on the same
    # frozen encoder and the same segment vectors, a 768-dim logistic regression
    # reaches state-level F1_table .519 on the hard subset while the trained
    # 16-dim head reached .291 — below the .314 of answering `revise_table` for
    # everything. Nothing else about the two differs.
    tab_dim: int = 0
    table_agg: str = "logsumexp"   # logsumexp | max — `max` is what the probe used
    # Overriding EVIDENCE from the command line, so the assignment is an
    # ablation rather than a fact baked into the file.
    evidence: Dict[str, Dict] = field(default_factory=lambda: {k: dict(v)
                                                               for k, v in EVIDENCE.items()})


class StagedLocalizer(nn.Module):
    def __init__(self, cfg: StagedConfig, tokenizer_len: Optional[int] = None):
        super().__init__()
        from transformers import AutoModel
        self.cfg = cfg
        self.encoder = AutoModel.from_pretrained(cfg.model_name)
        self.n_added = 0
        if tokenizer_len is not None:
            before = self.encoder.get_input_embeddings().weight.shape[0]
            self.encoder.resize_token_embeddings(tokenizer_len)
            # HOW MANY ROWS ARE NEW, so `added_embeddings` can round-trip them.
            # The frozen encoder is recoverable from the hub by name; these rows
            # are NOT — `[TABLE]`, `[COL]`, `[JOIN]` were never pretrained, and
            # `resize_token_embeddings` draws them fresh every time the model is
            # built. Leaving them out of the checkpoint means the served model is
            # not the evaluated model: reloading a run that scored two-class
            # macro-F1 .527 reproduced .522, with the confusion matrix off by a
            # cell here and there rather than by rounding.
            self.n_added = max(tokenizer_len - before, 0)
        hidden = self.encoder.config.hidden_size
        if cfg.freeze_encoder:
            for p in self.encoder.parameters():
                p.requires_grad_(False)

        # One projection shared by all three bundles, as before: the grammar in
        # evidence_text.py describes a column of a rejected table and a column of
        # a produced table identically, so what is learned about columns should
        # transfer between passes rather than be learned three times.
        self.proj = nn.Linear(hidden * (2 if cfg.pooling == "mean+max" else 1),
                              cfg.proj_dim)
        self.norm = nn.LayerNorm(cfg.proj_dim)
        jkm = torch.tensor(cfg.jk_mean or [0.0] * cfg.jk_dim, dtype=torch.float)
        jks = torch.tensor(cfg.jk_std or [1.0] * cfg.jk_dim, dtype=torch.float)
        # Per-feature standardisation from fixed training statistics, never
        # LayerNorm: normalising the nine ratios WITHIN a sample destroys them,
        # since a state whose jaccard, yield and containment are all low is
        # exactly what broken looks like. Measured cost of getting this wrong was
        # .580 against .678 for logistic regression on the identical nine numbers.
        self.register_buffer("jk_mean", jkm)
        self.register_buffer("jk_std", jks.clamp(min=1e-6))
        k = len(cfg.tk_idx)
        self.register_buffer("tk_idx", torch.tensor(cfg.tk_idx, dtype=torch.long))
        self.register_buffer("tk_mean", torch.tensor(cfg.tk_mean or [0.0] * k,
                                                     dtype=torch.float))
        self.register_buffer("tk_std", torch.tensor(cfg.tk_std or [1.0] * k,
                                                    dtype=torch.float).clamp(min=1e-6))

        # The per-table path owns everything it uses. Sharing `self.proj` with
        # the state-level scorers was the previous version and it did not work;
        # see StagedConfig.tab_dim for the measurement. Linear, and by default
        # not projected at all, because the thing being reproduced is a logistic
        # regression on the 768-dim segment mean — that is the arm that matched
        # gpt-5, so the model should be it, not an approximation of it.
        self.tab_proj = None
        self.tab_head = None
        # Standardisation for the segment vector, filled in by `load_tab_head`.
        # Identity until then, so an unloaded model behaves exactly as before.
        self.register_buffer("tab_vmean", torch.zeros(hidden))
        self.register_buffer("tab_vstd", torch.ones(hidden))
        if cfg.per_table:
            d = hidden
            if cfg.tab_dim:
                self.tab_proj = nn.Sequential(nn.Linear(hidden, cfg.tab_dim),
                                              nn.LayerNorm(cfg.tab_dim))
                d = cfg.tab_dim
            self.tab_head = nn.Linear(d, 1)

        self.scorers = nn.ModuleDict()
        self.in_dim: Dict[str, int] = {}
        for name, ev in cfg.evidence.items():
            d = (cfg.proj_dim * len(ev["bundles"])
                 + (cfg.jk_dim if ev["jk"] else 0)
                 + (len(cfg.tk_idx) if ev.get("tk") else 0))
            self.in_dim[name] = d
            self.scorers[name] = nn.Sequential(
                nn.Linear(d, cfg.trunk_dim), nn.GELU(), nn.Dropout(cfg.dropout),
                nn.Linear(cfg.trunk_dim, 1))

    # ---------------------------------------------------------------- encoding
    def _bundle_vecs(self, batch: Dict[str, Any], keep: Sequence[str] = ()
                     ) -> tuple:
        """Encode only the bundles some scorer actually asks for.

        Dropping ev_2 costs a third of the forward pass, and the ablation that
        removes it should not silently keep paying for it.
        """
        wanted = sorted({b for ev in self.cfg.evidence.values() for b in ev["bundles"]}
                        | set(keep))
        out, hid = {}, {}
        for b in wanted:
            ids, mask = batch[f"{b}_input_ids"], batch[f"{b}_attention_mask"]
            # nullcontext, not enable_grad: enable_grad OVERRIDES an ambient
            # no_grad, which built a graph during EVALUATION and exhausted 16 GB
            # before a single training step.
            ctx = (torch.no_grad() if self.cfg.freeze_encoder
                   else contextlib.nullcontext())
            with ctx:
                h = self.encoder(input_ids=ids, attention_mask=mask).last_hidden_state
            out[b] = self.norm(self.proj(pool(h, mask, self.cfg.pooling)))
            if b in keep:
                hid[b] = h
        return out, hid

    def _table_scores(self, h: torch.Tensor, batch: Dict[str, Any]):
        """Per-table scores `s_i`, and their soft-OR over the REJECTED tables.

        `tab_seg` is a [B, K, L] membership matrix, so the per-segment mean is
        one batched matmul — no python loop over tables, and no second forward
        pass over the same 3072 tokens.

        The OR runs over rejected tables only. A selected table being needed is
        not evidence for `revise_table`; the action is defined as "a table the
        question needs was thrown away", and scoring the selected ones into the
        same aggregate would let a state be routed to `revise_table` for a table
        it already has.
        """
        seg = batch["tab_seg"].to(h.dtype)
        vec = torch.bmm(seg, h) / seg.sum(-1, keepdim=True).clamp(min=1e-6)
        vec = (vec - self.tab_vmean) / self.tab_vstd
        if self.tab_proj is not None:
            vec = self.tab_proj(vec)
        s = self.tab_head(vec).squeeze(-1)                             # [B, K]
        m = batch["tab_valid"] & batch["tab_rejected"]
        # -1e4 rather than -inf: exp(-1e4) is exactly 0 in the log-sum-exp, while
        # -inf makes the row NaN when a state rejected nothing at all.
        masked = s.masked_fill(~m, -1e4)
        mil = (masked.max(-1).values if self.cfg.table_agg == "max"
               else torch.logsumexp(masked, dim=-1))
        mil = torch.where(m.any(-1), mil, torch.zeros_like(mil))
        return s, m, mil

    def forward(self, batch: Dict[str, Any]) -> Dict[str, torch.Tensor]:
        keep = ("ev_1",) if self.cfg.per_table else ()
        vecs, hid = self._bundle_vecs(batch, keep=keep)
        jk = (batch["jk"] - self.jk_mean) / self.jk_std
        tk = None
        if len(self.cfg.tk_idx):
            if "hand" not in batch:
                raise KeyError("the tk channel is enabled but the batch has no `hand` vector; "
                               "StateDataset/Collator must be built with hand=True")
            tk = (batch["hand"].index_select(-1, self.tk_idx) - self.tk_mean) / self.tk_std
        z = {}
        for name, ev in self.cfg.evidence.items():
            parts = [vecs[b] for b in ev["bundles"]]
            if ev["jk"]:
                parts.append(jk)
            if ev.get("tk") and tk is not None:
                parts.append(tk)
            z[name] = self.scorers[name](torch.cat(parts, dim=-1)).squeeze(-1)

        extra: Dict[str, torch.Tensor] = {}
        if self.cfg.per_table:
            if "tab_seg" not in batch:
                raise KeyError("per_table is enabled but the batch has no tab_seg; "
                               "StateDataset/Collator must be built with tables=True")
            s, m, mil = self._table_scores(hid["ev_1"], batch)
            extra = {"tab_logits": s, "tab_mask": m, "tab_mil": mil}
            # Additive, not replacing: the pooled path is where the one thing the
            # model demonstrably learned lives (n_selected < 2), and gpt-5 gets
            # only 3/7 of those, so the two paths are complementary. `--mil-only`
            # exists to check whether the pooled path contributes anything else.
            z["table"] = mil if self.cfg.mil_only else z["table"] + mil
        # Column order matches CLASSES so `logits.argmax(-1)` indexes it.
        return {"logits": torch.stack([z["ok"], z["table"], z["pipeline"]], dim=-1),
                "z": z, **extra}

    def probabilities(self, logits: torch.Tensor):
        """`(p_trigger, p_router)` in the shape `evaluate.evaluate` consumes.

        p_router is renormalised over the two failure classes rather than reusing
        the raw posteriors. The routing question is asked only about states that
        were acted on, i.e. conditioned on not-ok, so P(table | not ok) is the
        quantity — and using the unconditional posteriors would let a large P(ok)
        shrink both and change nothing except the numbers' scale.
        """
        p = torch.softmax(logits, dim=-1)
        fail = p[:, 1:]
        return 1.0 - p[:, 0], fail / fail.sum(-1, keepdim=True).clamp(min=1e-9)

    def load_tab_head(self, path, freeze: bool = True) -> None:
        """Install the probe's fitted per-table scorer, by default frozen.

        WHY THIS IS TWO STAGES AND NOT ONE
        ----------------------------------
        Trained jointly, this head does not survive. On the hard subset the same
        768-dim head reaches F1_table .519 fitted alone on a frozen encoder, and
        .243 — precision .184 against a base rate of .187, i.e. exactly chance —
        when trained end to end beside the three-way CE with LoRA on. Two things
        pull it apart: the CE gradient reaches `tab_head` through `mil` and is
        far larger than what 832 instances of BCE push back with, and LoRA keeps
        moving the encoder, so the representation the head was learning against
        is not the one it ends up reading.

        Freezing is therefore the default rather than an option, and it also
        pins the encoder: `--tab-head` with `--lora` is refused in run.py,
        because a frozen head on a drifting encoder is the second failure above
        with extra steps.
        """
        import numpy as np
        d = np.load(path, allow_pickle=True)
        if self.tab_head is None:
            raise SystemExit("--tab-head requires --per-table")
        if self.tab_proj is not None:
            raise SystemExit("--tab-head was fitted on 768 dimensions and cannot be combined with --tab-dim")
        w = torch.tensor(d["w"], dtype=torch.float).view(1, -1)
        if w.shape[1] != self.tab_head.in_features:
            raise SystemExit(f"weight dimension {w.shape[1]} does not match the head input "
                             f"dimension {self.tab_head.in_features}")
        with torch.no_grad():
            self.tab_head.weight.copy_(w)
            self.tab_head.bias.copy_(torch.tensor([float(d["b"])]))
            self.tab_vmean.copy_(torch.tensor(d["mean"], dtype=torch.float))
            self.tab_vstd.copy_(torch.tensor(d["std"], dtype=torch.float).clamp(min=1e-6))
        if freeze:
            self.tab_head.weight.requires_grad_(False)
            self.tab_head.bias.requires_grad_(False)
        print(f"  per-table head loaded from {path}"
              f"  ({'frozen' if freeze else 'kept trainable'}, arm={d['arm']})")

    def trainable_parameters(self):
        return [p for p in self.parameters() if p.requires_grad]


def load_checkpoint(ck: dict, special_tokens: Sequence[str], device: str):
    """Rebuild exactly as `run.py` built it, then load the trainable tensors.

    The order matters and is not interchangeable: `run.py` resizes the embedding
    table for the added markers INSIDE the model constructor and wraps the
    encoder with LoRA AFTERWARDS, so the checkpoint's parameter names are the
    peft-wrapped ones. Building in the other order produces names that do not
    match and `strict=False` would hide it — hence the explicit check below.
    """
    from dataset import build_tokenizer

    cfg_d = dict(ck["cfg"])
    cfg_d.pop("evidence", None)
    cfg = StagedConfig(evidence={k: dict(v) for k, v in ck["evidence"].items()}, **cfg_d)
    tok, added = build_tokenizer(cfg.model_name, special_tokens)
    model = StagedLocalizer(cfg, tokenizer_len=len(tok) if added else None)
    if ck.get("lora"):
        from peft import LoraConfig, get_peft_model
        r = int(ck["lora"])
        model.encoder = get_peft_model(model.encoder, LoraConfig(
            r=r, lora_alpha=2 * r, lora_dropout=0.05,
            target_modules=["Wqkv", "Wo"] if "ModernBERT" in cfg.model_name
            else ["query", "value"]))
    add = ck.get("added_embeddings")
    if add is not None and model.n_added:
        w = model.encoder.get_input_embeddings().weight
        n = min(int(model.n_added), add.shape[0])
        with torch.no_grad():
            w[-n:] = add[-n:].to(w.device, w.dtype)
        print(f"  restored the embeddings of {n} added tokens (they are not in the pretrained weights)")
    elif model.n_added:
        print(f"  [warn] the checkpoint has no added_embeddings; the {model.n_added} added "
              f"token embeddings were randomly re-initialised - this is NOT the model that "
              f"was trained. Re-train with the current run.py to remove this warning.")
    missing, unexpected = model.load_state_dict(ck["state_dict"], strict=False)
    if unexpected:
        raise SystemExit(f"the checkpoint has {len(unexpected)} keys that do not match the model, "
                         f"first few: {unexpected[:4]}. The build order or --lora disagrees.")
    loaded = len(ck["state_dict"])
    print(f"  loaded {loaded} tensors; {len(missing)} model tensors were not overwritten (these should all be frozen encoder weights)")
    return model.to(device).eval(), tok, cfg


def staged_losses(out: Dict[str, torch.Tensor], batch: Dict[str, Any],
                  class_weight: Optional[torch.Tensor] = None,
                  lambda_tab: float = 0.0,
                  tab_pos_weight: Optional[float] = None) -> Dict[str, torch.Tensor]:
    """One three-way cross-entropy. Every row supervises every logit.

    `class_weight` is not optional in practice. The deliverable is dominated by
    `revise_table`, the rarest failure class (54 of 247 training rows) and the
    one every arm collapses on; unweighted CE optimises the two classes that are
    already easy.
    """
    y = batch["y_class"]
    ce = nn.functional.cross_entropy(out["logits"], y, weight=class_weight)
    if "tab_logits" not in out or lambda_tab <= 0:
        return {"total": ce, "ce": ce}

    # Per-table BCE, on rejected tables only, over every state regardless of its
    # own label. This is the point of the head: a healthy state's rejected tables
    # are negatives that its state-level label never expressed, and they are the
    # majority of the 1277 instances.
    m = out["tab_mask"]
    if not bool(m.any()):
        return {"total": ce, "ce": ce}
    pw = (None if tab_pos_weight is None
          else torch.as_tensor(tab_pos_weight, dtype=out["tab_logits"].dtype,
                               device=out["tab_logits"].device))
    tab = nn.functional.binary_cross_entropy_with_logits(
        out["tab_logits"][m], batch["tab_gold"][m], pos_weight=pw)
    return {"total": ce + lambda_tab * tab, "ce": ce, "tab": tab}
