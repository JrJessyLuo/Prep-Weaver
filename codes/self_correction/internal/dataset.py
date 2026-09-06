#!/usr/bin/env python3
"""
dataset.py
==========
Rows exported by `export_trainset.py` -> tensors, with the sentence-pair shape
these encoders expect.

Each state is THREE pairs sharing one encoder:

    [CLS] question [SEP] ev_1 [SEP]     selected + rejected raw tables
    [CLS] question [SEP] ev_2 [SEP]     the declared schema
    [CLS] question [SEP] ev_3 [SEP]     the produced tables

The question is repeated in every pair on purpose. Every one of the three
decisions is a RELEVANCE judgement against the same question — can these tables
support it, can this schema support it, do these tables answer it — and pair
classification is the format the encoder was pretrained for. It is also what a
frozen embedding model could not exploit: putting question and evidence in one
pooled vector dropped `revise_table` from 0.927 to 0.590, because pooling
dilutes where cross-attention aligns.

Per-bundle max lengths differ because the evidence does. Measured on the
exported dev split: ev_1 median 2126 tokens, ev_2 547, ev_3 1051. Padding ev_2
to ev_1's length would triple the compute for nothing.
"""
from __future__ import annotations

import json
import random
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

# Imported lazily so the pure-python helpers in this module — `anonymize_row`
# above all — can be used where torch is not installed. The REMOTE localizer arm
# is exactly that case: the model runs in the serving process and the loop only
# needs to BUILD the evidence row, yet a module-level `import torch` made the
# whole arm die with `ModuleNotFoundError: No module named 'torch'` after
# spending nothing and reporting "never attempted a repair: 15/15". Dropping
# anonymisation would also route around it and must not be used: table names
# carry `<benchmark>_<task>_input_N`, which leaks the gold label outright.
try:
    import torch
    from torch.utils.data import Dataset
except ImportError:  # not just ModuleNotFoundError: a torch that is installed but
                     # cannot load its CUDA libraries raises plain ImportError, and
                     # the evidence row does not need torch either way.
    torch = None

    class Dataset:  # minimal stand-in; StateDataset is unusable without torch
        pass

BUNDLES = ("ev_1", "ev_2", "ev_3")
# The marker `evidence_text.py` writes before every table block in ev_1. It is
# the only thing that makes per-table supervision possible: the block boundaries
# are recoverable from the token ids alone, so a segment can be aligned to the
# table it describes without re-tokenising or re-parsing the text.
TABLE_TOKEN = "[TABLE]"
# ev_1 carries the rejected tables, which are the single strongest evidence for
# `revise_table` (0.945 embedded alone), so it gets the long window.
DEFAULT_MAXLEN = {"ev_1": 3072, "ev_2": 768, "ev_3": 1536}
CLASSES = ("no_revision_needed", "revise_table", "revise_pipeline")


_BIRD_NAME = re.compile(r"bird_[0-9a-f]+_input_\d+")


def anonymize_row(row: dict) -> dict:
    """Replace every table name with a content-free id, consistently in one row.

    WHY THIS IS NOT OPTIONAL HYGIENE
    --------------------------------
    The benchmark materialises a task's designated input tables as
    `bird_<taskid>_input_N.pkl` and every other table as `<db>_<table>.pkl`, and
    gold tables are a subset of the first kind. On dev that is a PERFECT giveaway:
    of the rejected tables, 41 of 43 gold ones carry the `bird_` name and 0 of 652
    non-gold ones do. A rule reading nothing but the name — no question, no
    columns, no values — scores AUC .946 on the per-table label, which is most of
    the .960 a 768-dim probe on the encoder reached. Any result on `revise_table`
    measured with these names in the text is uninterpretable, ours and the LLM
    baseline's alike; gpt-5's accepted reasons quote the string `_input_0.pkl`
    directly.

    IDS ARE SHUFFLED, NOT POSITIONAL
    --------------------------------
    Numbering the tables in the order they appear would rebuild the leak one
    level down, because `tables_1` lists the selected tables before the rejected
    ones and the `bird_` tables cluster. The permutation is seeded on `task_id`
    so a row anonymises identically every time it is loaded — training and
    evaluation must not disagree about what a name means.
    """
    names = [t["name"] for t in (row.get("tables_1") or [])]
    names += _BIRD_NAME.findall(row.get("ev_1") or "")
    names += _BIRD_NAME.findall(row.get("ev_2") or "")
    # Longest first: `card_games_cards.pkl` must not be rewritten by a rule for
    # `card_games_cards`, leaving a dangling `.pkl`.
    uniq = sorted({n for n in names if n}, key=len, reverse=True)
    order = list(range(len(uniq)))
    random.Random(str(row.get("task_id"))).shuffle(order)
    sub = {n: f"tbl_{order[i]:02d}" for i, n in enumerate(uniq)}

    out = dict(row)
    for b in ("ev_1", "ev_2", "ev_3"):
        s = out.get(b)
        if not s:
            continue
        for n in uniq:                     # already longest-first
            s = s.replace(n, sub[n])
        out[b] = _BIRD_NAME.sub("tbl_xx", s)
    if out.get("tables_1"):
        out["tables_1"] = [{**t, "name": sub.get(t["name"], t["name"])}
                           for t in out["tables_1"]]
    return out


def load_rows(path: Path, roles: Optional[Sequence[str]] = None,
              min_ops: Optional[int] = None,
              anonymize: bool = False) -> List[dict]:
    rows = [json.loads(l) for l in Path(path).open() if l.strip()]
    if roles:
        rows = [r for r in rows if r.get("role") in set(roles)]
    if min_ops is not None:
        rows = [r for r in rows if r.get("dc_ops", 0) >= min_ops]
    if anonymize:
        rows = [anonymize_row(r) for r in rows]
    return rows


class StateDataset(Dataset):
    """One row per execution state. Tokenisation happens in the collator so that
    a batch pads to its own longest member rather than to the global maximum."""

    def __init__(self, rows: List[dict], jk_dim: int = 9, hand: bool = False,
                 tables: bool = False):
        self.rows = rows
        self.jk_dim = jk_dim
        self.hand = hand
        self.tables = tables
        if tables:
            missing = sum(1 for r in rows if not r.get("tables_1"))
            if missing == len(rows):
                raise SystemExit(
                    "--per-table needs `tables_1` in the export (each table's name/role/gold);"
                    "that field comes from the train2/dev2 re-export of export_trainset.py")
            if missing:
                print(f"  [warn] {missing}/{len(rows)} rows have no tables_1; their per-table loss is empty")

    def __len__(self) -> int:
        return len(self.rows)

    def __getitem__(self, i: int) -> dict:
        r = self.rows[i]
        out = {
            "task_id": r["task_id"],
            "question": r.get("question") or "",
            "y_trigger": int(r.get("y_trigger", 0)),
            "y_router": int(r.get("y_router", -1)),
            # The three-way target. Derived from `label` rather than from
            # y_trigger/y_router so a row can never carry two targets that
            # disagree — the staged model is trained on this one alone.
            "y_class": CLASSES.index(r["label"]),
            "jk": [float(x) for x in (r.get("jk") or [0.0] * self.jk_dim)],
        }
        for b in BUNDLES:
            out[b] = r.get(b) or "(none)"
        if self.hand:
            out["hand"] = [float(x) for x in (r.get("hand") or [])]
        if self.tables:
            out["tables"] = r.get("tables_1") or []
        return out


@dataclass
class Collator:
    tokenizer: Any
    maxlen: Dict[str, int]
    hand: bool = False
    tables: bool = False

    # Counted across the whole epoch rather than printed per batch: the number
    # that matters is how much per-table supervision truncation destroys, and a
    # per-batch figure over four samples says nothing. `run.py` reads it once.
    dropped: List[int] = field(default_factory=lambda: [0, 0])

    def _table_segments(self, batch: List[dict], ids, mask) -> Dict[str, Any]:
        """Cut ev_1 at the `[TABLE]` markers and align the pieces to `tables_1`.

        Segment k runs from its own marker to the next one (the last to the end
        of the unpadded sequence), so it holds exactly one table's block,
        marker included.

        ALIGNMENT IS TRUNCATION-AWARE, AND HAS TO BE
        --------------------------------------------
        `tables_1` was filtered to the blocks that survived truncation in
        `evidence_text.py`, but the tokenizer truncates again at
        `DEFAULT_MAXLEN["ev_1"]`, and ev_1 runs to a median 2126 tokens with a
        long tail. Zipping the two lists blindly would silently pair segment k
        with a different table's gold flag — a label permutation, which is worse
        than a missing label. Taking the first `min(n_segments, len(list))` of each is
        safe because both lists are in the same order and truncation only ever
        removes a suffix.
        """
        import torch as _t
        tid = self.tokenizer.convert_tokens_to_ids(TABLE_TOKEN)
        if tid is None or tid == self.tokenizer.unk_token_id:
            raise SystemExit(f"{TABLE_TOKEN} is not in the tokenizer; "
                             "build_tokenizer must add meta['special_tokens'] first")
        B, L = ids.shape
        lens = mask.sum(1).tolist()
        marks = [(ids[i] == tid).nonzero(as_tuple=True)[0].tolist() for i in range(B)]
        metas = [x.get("tables") or [] for x in batch]
        K = max(1, max(min(len(m), len(t)) for m, t in zip(marks, metas)))

        seg = _t.zeros(B, K, L)
        valid = _t.zeros(B, K, dtype=_t.bool)
        rej = _t.zeros(B, K, dtype=_t.bool)
        gold = _t.zeros(B, K)
        for i, (mk, meta) in enumerate(zip(marks, metas)):
            n = min(len(mk), len(meta))
            self.dropped[0] += len(meta) - n
            self.dropped[1] += len(meta)
            for k in range(n):
                end = mk[k + 1] if k + 1 < len(mk) else int(lens[i])
                if end <= mk[k]:
                    continue
                seg[i, k, mk[k]:end] = 1.0
                valid[i, k] = True
                rej[i, k] = meta[k].get("role") == "rejected"
                gold[i, k] = float(meta[k].get("gold", 0))
        return {"tab_seg": seg, "tab_valid": valid,
                "tab_rejected": rej, "tab_gold": gold}

    def __call__(self, batch: List[dict]) -> Dict[str, Any]:
        out: Dict[str, Any] = {
            "task_id": [b["task_id"] for b in batch],
            "y_trigger": torch.tensor([b["y_trigger"] for b in batch], dtype=torch.float),
            "y_router": torch.tensor([b["y_router"] for b in batch], dtype=torch.long),
            "y_class": torch.tensor([b["y_class"] for b in batch], dtype=torch.long),
            "jk": torch.tensor([b["jk"] for b in batch], dtype=torch.float),
        }
        for b in BUNDLES:
            enc = self.tokenizer([x["question"] for x in batch],
                                 [x[b] for x in batch],
                                 padding=True, truncation="only_second",
                                 max_length=self.maxlen[b], return_tensors="pt")
            out[f"{b}_input_ids"] = enc["input_ids"]
            out[f"{b}_attention_mask"] = enc["attention_mask"]
        if self.hand and batch[0].get("hand"):
            out["hand"] = torch.tensor([b["hand"] for b in batch], dtype=torch.float)
        if self.tables:
            out.update(self._table_segments(batch, out["ev_1_input_ids"],
                                            out["ev_1_attention_mask"]))
        return out


def build_tokenizer(model_name: str, special_tokens: Sequence[str]):
    """Add the grammar's markers as real tokens.

    `[TABLE]`, `[COL]`, `[JOIN]` are structural, not English. Left as ordinary
    text they fragment into subwords and mix with whatever those pieces mean in
    the pretraining corpus; as added tokens they get their own embeddings and can
    learn a role. `role=rejected` versus `role=selected` is the distinction the
    whole `revise_table` decision turns on, so it should not be spelled in a way
    the tokenizer scatters.
    """
    from transformers import AutoTokenizer
    tok = AutoTokenizer.from_pretrained(model_name)
    added = tok.add_special_tokens({"additional_special_tokens": list(special_tokens)})
    return tok, added
