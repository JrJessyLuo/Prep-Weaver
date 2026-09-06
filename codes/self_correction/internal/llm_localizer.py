#!/usr/bin/env python3
"""
llm_localizer.py
================
The LLM-agent baseline: hand the model the same observations and let it name the
action, with no training.

    python llm_localizer.py --dev ../data/dev.jsonl --train ../data/train.jsonl \
        --out runs/llm_fewshot --shots 6 --k 3 --limit 20      # pilot first

WHY THIS IS THE MOST IMPORTANT BASELINE HERE
--------------------------------------------
Two methods now agree on the same failure. The 86 hand features reach
`revise_table` F1 .409-.419 and the trained staged model .350 — below the .370 a
constant "always answer revise_table" scores — while both do fine on
`revise_pipeline`. The explanation on offer is structural: dropping a table does
not make the later stages misbehave, they faithfully carry out a smaller task, so
the artifacts stay self-consistent (on the missed tasks, join-key uniqueness .996
and every declared column produced). Twenty gold-free signals all stayed under
.60 AUC on schema-linking faults against .759 on pipeline faults, and re-running
the linker to measure its own instability scored .487-.561.

But both methods read the SAME evidence through fitted models on 198 training
rows, so "your representations are the problem" is a live objection. An LLM given
the same evidence and no training at all is an independent third line. If it also
collapses on `revise_table`, the claim stops being "our classifier is weak" and
becomes "this is not observable at localization time". If it does not collapse,
the bottleneck is our representation and the direction has to change. Both
outcomes are worth the money.

FAIRNESS
--------
  same evidence     ev_1 / ev_2 / ev_3 and the nine join-key ratios, taken
                    verbatim from the exported rows. Not a re-designed input.
  same decision     one label out of three, from the model's own choice. Our
                    model ends in argmax too, so a label is the fair unit of
                    comparison and no calibrated score is required.
  same scoring      `evaluate(pred_labels=...)`, the identical function every
                    other arm goes through.
  few-shot          the label rule verbatim plus `--shots` examples drawn from
                    TRAIN, stratified by class. Prompting weakly and reporting
                    the number would not be a baseline.
  self-consistency  `--k` samples, majority vote. NOTE: gpt-5 takes the
                    responses branch in llm.py and never receives `temperature`,
                    so its k samples are near-duplicates — perturb_stage measured
                    schema linking re-sampling to an IDENTICAL selection on 79%
                    of tasks. Voting is informative for gpt-4o and mostly
                    decorative for gpt-5; the per-task votes are stored so the
                    agreement rate can be reported rather than assumed.
  cost              printed. If the LLM matches us, our contribution is cost and
                    latency rather than accuracy, and that has to be said plainly.

The few-shot examples are truncated hard (`--shot-chars`) while the QUERY keeps
its full evidence. Six untruncated examples would be ~12k tokens of prompt before
the question is even asked.
"""
from __future__ import annotations

import argparse
import collections
import json
import random
import re
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional, Sequence

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
for _p in (str(HERE), str(ROOT), str(ROOT / "prep_utils")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from evaluate import ACTIONS, CLASSES, evaluate, render      # noqa: E402

OK = "no_revision_needed"

# Verbatim from build_labels.py / export_trainset.cascade. The model is judged
# against these labels, so it is told exactly what they mean; withholding the
# rule would measure whether it can guess our convention, not whether the
# evidence supports the decision.
RULE = """A data-preparation trajectory has three stages:
  1. schema linking       picks which raw tables are needed
  2. relational planning  declares the schema and join edges
  3. pipeline synthesis   transforms the raw tables into the produced subtables

The ground-truth label is assigned upstream-first:
  - no_revision_needed : the produced subtables AND the join keys are both fully
                         correct.
  - revise_table       : otherwise, if the set of tables the query truly needs is
                         NOT a subset of the tables that were selected. (A
                         superset is fine; a MISSING table is not, because no
                         later stage can recover it.)
  - revise_pipeline    : otherwise. Both upstream stages are sound and the
                         produced tables are still wrong.

Answer with the single label that this state would receive."""

_G_HEAD = """The evidence uses a fixed grammar:
  [TABLE] name=... role={roles} rows=... cols=...
  [COL] name=... type=... distinct=... unique=... nonnull=... values= v1 ; v2
  [JOIN] left=t1.c1 right=t2.c2
"""
_G_EV1 = ("EVIDENCE 1 is the raw tables, both the ones schema linking SELECTED "
          "and the ones it REJECTED.")
# `--no-rejected` hides the rejected tables. The label rule still asks whether the
# needed tables are a subset of the selected ones, which stays answerable — the
# question becomes "are the selected tables SUFFICIENT for this question" rather
# than "is one of these listed candidates missing". Saying so explicitly matters:
# without it the model looks for a REJECTED block, finds none, and reads the
# absence as evidence that nothing is missing.
_G_EV1_NOREJ = ("EVIDENCE 1 is the raw tables that schema linking SELECTED. The "
                "tables it rejected are NOT shown, so judge `revise_table` by "
                "whether the selected tables are SUFFICIENT to answer the "
                "question — not by looking for a rejected candidate. Their "
                "absence from the prompt is not evidence that none is missing.")
_G_TAIL = (" EVIDENCE 2 is the declared schema and join edges. EVIDENCE 3 is the\n"
           "produced subtables.")
_G_JK = (" JOIN KEY RATIOS are computed on the produced join, all\n"
         "scale-free, all in [0,1] unless stated.")
_G_AUDIT = ("""
EVIDENCE 4 is a TRANSFORMATION AUDIT, derived from EVIDENCE 1 and 3:
  [AUDIT] produced=... source=... rows=A->B cols=C->D [dropped=..] status=...
      status=IDENTITY means the produced table has the SAME row count, the same
      column count and the same column names as its source: the pipeline emitted
      the source table unchanged. Row counts are exact. If the question requires
      a filter, an aggregation or a projection, IDENTITY means the pipeline did
      not perform it — this is `revise_pipeline`, not a healthy state.
      status=TRANSFORMED means something was applied; it does not say it was
      correct.
  [LITERAL] "x" is in the source samples and is still present / ABSENT FROM ...
      A value the question names. Only literals that are visible in the source
      samples are listed at all, so a line saying ABSENT means the pipeline
      dropped a value the question asks for. Absent literals are simply not
      listed; that is not evidence either way.""")


def grammar(with_jk: bool = True, with_rejected: bool = True,
            with_audit: bool = False) -> str:
    """The grammar block, describing exactly the sections the prompt contains.

    Every flag that removes a section must also remove its sentence here:
    telling the model to read a block that is not there is worse than not
    describing it at all.
    """
    roles = ("selected|rejected|declared|produced" if with_rejected
             else "selected|declared|produced")
    s = _G_HEAD.format(roles=roles)
    s += (_G_EV1 if with_rejected else _G_EV1_NOREJ) + _G_TAIL
    s += (_G_JK if with_jk else "")
    return s + (_G_AUDIT if with_audit else "")


GRAMMAR = grammar()
GRAMMAR_NOJK = grammar(with_jk=False)

JK_NAMES = ("containment", "jaccard", "yield", "fanout", "left_unique",
            "right_unique", "left_nonnull", "right_nonnull", "present")


def _parse_tables(ev: Optional[str]) -> Dict[str, dict]:
    """`[TABLE]`/`[COL]` text back into a dict. Read-only over evidence we
    already send — no new access to the benchmark, so this cannot disagree with
    what the model was shown."""
    out: Dict[str, dict] = {}
    cur = None
    for line in (ev or "").splitlines():
        if line.startswith("[TABLE]"):
            kv = dict(re.findall(r"(\w+)=(\S+)", line))
            cur = {"role": kv.get("role"), "rows": kv.get("rows"),
                   "cols": kv.get("cols"), "source": kv.get("source"),
                   "colnames": [], "samples": {}}
            out[kv.get("name", "")] = cur
        elif line.startswith("[COL]") and cur is not None:
            m = re.match(r"\[COL\] name=(\S+)", line)
            if not m:
                continue
            cur["colnames"].append(m.group(1))
            vm = re.search(r"values=\s*(.*)$", line)
            if vm:
                cur["samples"][m.group(1)] = [x.strip() for x in vm.group(1).split(";")]
    return out


def _int(x) -> Optional[int]:
    try:
        return int(str(x))
    except Exception:
        return None


_LIT = re.compile(r"'([^']{2,40})'|\"([^\"]{2,40})\"|\b([A-Z][a-z]+(?: [A-Z][a-z]+)+)\b")


def transform_audit(row: dict) -> str:
    """What the pipeline actually DID, stated as facts the model can check.

    WHY THIS BLOCK EXISTS. `revise_pipeline` is the residual class — "both
    upstream stages are sound and the produced tables are still wrong" — so
    every structural signal already in the prompt is positive for it BY
    CONSTRUCTION: the tables are sufficient, the join lines up, the produced
    schema matches the declared one. A model that checks those and finds them
    all sound has no remaining reason to answer anything but
    `no_revision_needed`, which is exactly what it did: 15 of 17 recall misses
    on the hard subset were this class, every one of them justified with some
    variant of "selected tables suffice, join keys align, produced subtables
    match the schema".

    The discriminating fact is not structural, it is whether the transformation
    HAPPENED. A produced table with the same row and column count as its source
    is the source, and if the question asks to filter, aggregate or project,
    that is a pipeline failure visible without gold. Row counts are exact, not
    sampled, so IDENTITY is a hard fact rather than an inference.

    The literal check is deliberately reported as three-valued. `values=` holds
    a handful of samples, so absence from the produced samples is weak on its
    own; absence from the produced samples while PRESENT in the source samples
    is the informative case, and the block says which one it is rather than
    collapsing both to "not found".
    """
    src = _parse_tables(row.get("ev_1"))
    dec = _parse_tables(row.get("ev_2"))
    prod = _parse_tables(row.get("ev_3"))
    lines: List[str] = []
    for name, p in prod.items():
        s_name = (dec.get(name) or {}).get("source") or ""
        s = src.get(s_name)
        if not s:
            lines.append(f"[AUDIT] produced={name} source=? "
                         f"rows={p['rows']} cols={p['cols']} status=NO_SOURCE_LINK")
            continue
        pr, sr = _int(p["rows"]), _int(s["rows"])
        pc, sc = _int(p["cols"]), _int(s["cols"])
        same_rows = pr is not None and pr == sr
        same_cols = pc is not None and pc == sc
        dropped = [c for c in s["colnames"] if c not in p["colnames"]]
        added = [c for c in p["colnames"] if c not in s["colnames"]]
        status = ("IDENTITY" if (same_rows and same_cols and not dropped and not added)
                  else "TRANSFORMED")
        bits = [f"rows={sr}->{pr}", f"cols={sc}->{pc}"]
        if dropped:
            bits.append(f"dropped={len(dropped)}{dropped[:4]}")
        if added:
            bits.append(f"added={len(added)}{added[:4]}")
        lines.append(f"[AUDIT] produced={name} source={s_name} "
                     + "  ".join(bits) + f"  status={status}")

    q = row.get("question") or ""
    seen = set()
    for m in _LIT.finditer(q):
        lit = next(g for g in m.groups() if g)
        low = lit.lower()
        if low in seen or len(low) < 3:
            continue
        seen.add(low)
        in_src = any(low in v.lower() for t in src.values()
                     for vs in t["samples"].values() for v in vs)
        if not in_src:
            # Not checkable. `values=` holds six samples per column, so a literal
            # absent from the SOURCE samples says nothing about the pipeline —
            # across all 141 dev tasks the informative yes/no case never fired
            # once, and emitting `no/no` would spend tokens teaching the model to
            # read a field that is always the same.
            continue
        in_prod = any(low in v.lower() for t in prod.values()
                      for vs in t["samples"].values() for v in vs)
        lines.append(f'[LITERAL] "{lit}" is in the source samples and is '
                     f'{"still present in" if in_prod else "ABSENT FROM"} '
                     f"the produced samples")
    return "\n".join(lines) if lines else "(none)"


def drop_rejected(ev1: Optional[str]) -> str:
    """Keep only the `role=selected` tables in EVIDENCE 1.

    `ev_1` is a flat sequence of `[TABLE] ...` headers each followed by its
    `[COL]` lines, so a block ends where the next `[TABLE]` begins. Anything
    before the first header (there is normally nothing) is kept.
    """
    if not ev1:
        return ev1 or ""
    out, keep = [], True
    for line in ev1.splitlines():
        if line.lstrip().startswith("[TABLE]"):
            keep = "role=rejected" not in line
        if keep:
            out.append(line)
    return "\n".join(out)


def render_state(r: dict, max_chars: Optional[int] = None,
                 with_jk: bool = True, with_rejected: bool = True,
                 with_audit: bool = False) -> str:
    def cut(x, n):
        x = x or "(none)"
        return x if (n is None or len(x) <= n) else x[:n] + "\n...[truncated]"
    # 0 and None both mean "do not truncate". The examples used to be capped at
    # 2500 chars while the query was never capped, which left each example block
    # with ~830 characters of evidence — table headers and almost no `[COL]`
    # lines. The examples then demonstrated a mapping from MUTILATED evidence to
    # a label, teaching the label prior rather than the judgement, and the query
    # arrived at a density the examples never showed. Same density on both sides
    # or the examples are not examples of the task.
    max_chars = max_chars or None
    n = None if max_chars is None else max_chars // 3
    ev1 = r.get("ev_1") if with_rejected else drop_rejected(r.get("ev_1"))
    ev1_hdr = ("raw tables: selected + rejected" if with_rejected
               else "raw tables: selected only")
    body = (f"QUESTION: {r.get('question', '')}\n\n"
            f"EVIDENCE 1 ({ev1_hdr})\n{cut(ev1, n)}\n\n"
            f"EVIDENCE 2 (declared schema + join edges)\n{cut(r.get('ev_2'), n)}\n\n"
            f"EVIDENCE 3 (produced subtables)\n{cut(r.get('ev_3'), n)}")
    if with_jk:
        jk = "  ".join(f"{k}={v:.3f}" for k, v in zip(JK_NAMES, r.get("jk") or []))
        body += f"\n\nJOIN KEY RATIOS\n{jk}"
    if with_audit:
        # Never truncated. It is short by construction — one line per produced
        # table plus one per question literal — and it is the only block that
        # carries a positive signal for the residual class.
        body += f"\n\nEVIDENCE 4 (transformation audit)\n{transform_audit(r)}"
    return body


# ASK FOR ONLY WHAT IS USED.
# Extra fields are not free: adding `health` to this schema moved gpt-4o's
# `no_revision_needed` predictions from 22 of 141 to 2 of 141. A field the caller
# ignores still changes the label, so the two modes get two schemas rather than
# one schema and a discarded value.
_ASK_LABEL = ('Reply with JSON only: {"label": "<one of no_revision_needed, '
              'revise_table, revise_pipeline>", "reason": "<one short sentence>"}')
_ASK_SCORE = ('Reply with JSON only: {"label": "<one of no_revision_needed, '
              'revise_table, revise_pipeline>", "confidence": <0-100>, '
              '"health": <0-100>, "reason": "<one short sentence>"}\n\n'
              "`health` is 0-100 for HOW CORRECT THE PRODUCED TABLES ARE, "
              "independently of the label: 100 = they already answer the "
              "question, 0 = they are unusable. It must be comparable ACROSS "
              "states, because it is used to decide whether a repaired state is "
              "better than the one before it. `confidence` is about your label; "
              "`health` is about the data. Do not copy one into the other.")


def build_prompt(query: dict, shots: List[dict], shot_chars: int,
                 ask_score: bool = True, with_jk: bool = True,
                 with_rejected: bool = True, with_audit: bool = False) -> str:
    # The examples go through the same renderer as the query, so a section the
    # query does not have cannot survive in a shot — an example still showing
    # rejected tables would teach the model to expect a block that is gone.
    kw = dict(with_jk=with_jk, with_rejected=with_rejected, with_audit=with_audit)
    parts = [RULE, "", grammar(**kw), ""]
    if shots:
        parts.append(f"Here are {len(shots)} labelled examples.")
        for i, s in enumerate(shots, 1):
            parts += [f"\n===== EXAMPLE {i} =====",
                      render_state(s, shot_chars, **kw),
                      f"LABEL: {s['label']}"]
        parts.append("\n===== END OF EXAMPLES =====\n")
    ask = _ASK_SCORE if ask_score else _ASK_LABEL
    parts += ["Now label this state.", "", render_state(query, **kw), "", ask]
    return "\n".join(parts)


def pick_shots(train: List[dict], n: int, seed: int) -> List[dict]:
    """Stratified over the three classes, so the prompt cannot imply a prior."""
    by = collections.defaultdict(list)
    for r in train:
        by[r["label"]].append(r)
    rng = random.Random(seed)
    per = max(1, n // len(CLASSES))
    out: List[dict] = []
    for c in CLASSES:
        pool = by.get(c) or []
        rng.shuffle(pool)
        out += pool[:per]
    rng.shuffle(out)
    return out[:n]


def parse(text: str) -> Dict:
    """Label, confidence and REASON.

    The reason was discarded in the first version and that was the wrong call:
    the confusion matrix says gpt-5 sends 25 of 67 healthy states to
    `revise_pipeline` and misses 20 broken ones as `no_revision_needed`, but a
    matrix cannot say WHY, and the model already wrote the answer in every reply.
    Re-running to recover it costs a full pass over dev.
    """
    label, conf, why = None, None, ""
    # `d` must exist even when there is no JSON to load: `llm.py` returns
    # `{"text": ""}` for a call that exhausted its retries, and reading
    # `d.get("health")` off an unbound name then killed the whole 141-task pass
    # over one refused prompt.
    d: dict = {}
    m = re.search(r"\{.*\}", text or "", re.S)
    if m:
        try:
            d = json.loads(m.group(0))
            label = d.get("label")
            conf = d.get("confidence")
            why = str(d.get("reason") or "")
        except Exception:
            pass
    if label not in CLASSES:
        # Fall back to a plain scan. A malformed reply is recorded as such rather
        # than silently becoming a guess; `unparsed` is reported.
        hits = [c for c in CLASSES if c in (text or "")]
        label = hits[0] if len(hits) == 1 else None
    try:
        conf = float(conf)
    except Exception:
        conf = None
    h = d.get("health")
    try:
        h = float(h)
    except Exception:
        h = None
    return {"label": label, "confidence": conf, "health": h, "reason": why}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[3])
    ap.add_argument("--dev", type=Path, required=True)
    ap.add_argument("--train", type=Path, default=None, help="few-shot pool")
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--model", default="gpt-4o-2024-08-06")
    ap.add_argument("--shots", type=int, default=6, help="0 = zero-shot arm")
    ap.add_argument("--audit", action="store_true",
                    help="add EVIDENCE 4, a per-table transformation audit "
                         "(rows/cols source->produced, IDENTITY vs TRANSFORMED). "
                         "OFF by default because it MEASURABLY HURT: two-class "
                         "macro-F1 .539 -> .506 on full dev at 41% more cost. It "
                         "pushed `revise_pipeline` predictions 57 -> 67 while "
                         "precision fell .404 -> .358 — the grammar told the "
                         "model IDENTITY means `revise_pipeline`, which is wrong: "
                         "a state missing a table is also IDENTITY, because the "
                         "pipeline has nothing to work with. Kept as a flag so "
                         "the ablation is reproducible, not as a default.")
    ap.add_argument("--shot-chars", type=int, default=2500,
                    help="per-example evidence cap; 0 = no cap. The query is "
                         "never capped, so at 2500 each example carries ~830 "
                         "characters of evidence against a full-density query. "
                         "Lifting the cap was tried and did not pay: it was run "
                         "TOGETHER WITH --audit, so the two are not separately "
                         "attributable, and the bundle lost .033 macro-F1 while "
                         "prompts grew 19k -> 27k chars.")
    ap.add_argument("--k", type=int, default=3, help="self-consistency samples")
    ap.add_argument("--max-tokens", type=int, default=0,
                    help="output cap. 0 picks 512 for a plain chat model and 4096 "
                         "for gpt-5, because REASONING TOKENS ARE BILLED AND "
                         "COUNTED AGAINST THIS CAP. At 512 with effort=medium the "
                         "entire budget went to reasoning and every one of 30 calls "
                         "returned an empty string — output tokens came to exactly "
                         "512 x 30, which is the only reason it was noticed. The "
                         "run still printed a clean-looking table of zeros.")
    ap.add_argument("--temperature", type=float, default=0.7,
                    help="ignored by gpt-5 (responses branch never passes it)")
    ap.add_argument("--limit", type=int, default=None, help="pilot on the first N")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--no-jk", action="store_true",
                    help="drop the nine join-key ratios from the prompt. They are "
                         "the one numeric block an LLM cannot obviously use — it "
                         "reads them as text — while for our own model they are a "
                         "separate input channel to the pipeline scorer.")
    ap.add_argument("--no-rejected", action="store_true",
                    help="show only the SELECTED raw tables in EVIDENCE 1. An "
                         "ablation, not an improvement: `revise_table` is defined "
                         "as `the needed tables are not a subset of the selected "
                         "ones`, so hiding the rejected candidates turns it from "
                         "`spot the missing one in this list` into `are these "
                         "enough`. It isolates how much of gpt-5's lead on that "
                         "class is the candidate list rather than the judgement, "
                         "and it is also the only variant our own encoder could "
                         "not exploit either, since its per-table head scores "
                         "exactly the rejected tables.")
    ap.add_argument("--label-only", action="store_true",
                    help="ask for label+reason only, matching the loop's "
                         "label mode. The default asks for confidence and "
                         "health as well, which is what the score mode needs "
                         "— and which measurably changes the label: adding "
                         "`health` moved gpt-4o from 22 `no_revision_needed` "
                         "predictions to 2.")
    ap.add_argument("--anonymize", action="store_true",
                    help="rewrite table names to shuffled content-free ids before "
                         "building the prompt. WITHOUT IT THIS BASELINE READS A "
                         "LABEL LEAK: the benchmark names gold input tables "
                         "bird_<task>_input_N, which on dev separates gold from "
                         "non-gold rejected tables 41/43 against 0/652, and gpt-5's "
                         "accepted reasons quote that string directly. Our own arms "
                         "get the same switch in run.py, so both sides move together.")
    ap.add_argument("--api-seed", type=int, default=None,
                    help="OpenAI `seed`, chat models only — reasoning models "
                         "reject it, which is exactly why this arm exists. With "
                         "seed and temperature both pinned, any label that still "
                         "flips between runs flipped BEFORE the sampling step, "
                         "so the variance is the serving stack, not the decoder. "
                         "`system_fingerprint` is recorded per task alongside it: "
                         "a flip across different fingerprints is a backend "
                         "change, not a failed seed, and the two must not be "
                         "reported as one number.")
    ap.add_argument("--effort", default="minimal",
                    choices=("minimal", "low", "medium", "high"),
                    help="gpt-5 reasoning effort. This was previously implicit — "
                         "llm.py falls back to $REASONING_EFFORT and then to "
                         "`minimal`, so every arm ran at whatever the environment "
                         "happened to hold. It is set explicitly and recorded in "
                         "meta.json now, because a loop run at `low` against "
                         "offline runs at `minimal` once looked like a 0.16 "
                         "macro-F1 sampling swing.")
    ap.add_argument("--hand-ref", type=float, default=None,
                    help="the hand-feature macro-F1 to print alongside")
    args = ap.parse_args(argv)
    args.out.mkdir(parents=True, exist_ok=True)

    from llm import llm_generate_setup

    from dataset import anonymize_row
    dev = [json.loads(l) for l in args.dev.open() if l.strip()]
    if args.anonymize:
        dev = [anonymize_row(r) for r in dev]
        print('  table names anonymised (tbl_NN)')
    if args.limit:
        dev = dev[: args.limit]
    train = ([json.loads(l) for l in args.train.open() if l.strip()]
             if args.train else [])
    if args.anonymize:
        train = [anonymize_row(r) for r in train]
    shots = pick_shots(train, args.shots, args.seed) if (train and args.shots) else []
    shot_ids = {s["task_id"] for s in shots}
    if shot_ids & {r["task_id"] for r in dev}:
        raise SystemExit("few-shot examples overlap dev - examples must come from train only")
    if not args.max_tokens:
        args.max_tokens = 4096 if args.model.startswith("gpt-5") else 512
    print(f"  max_tokens {args.max_tokens}"
          + ("   (gpt-5: reasoning tokens count toward this cap)"
             if args.model.startswith("gpt-5") else ""))
    print(f"dev {len(dev)}   few-shot {len(shots)} "
          f"({dict(collections.Counter(s['label'] for s in shots))})   "
          f"k={args.k}   model={args.model}")

    def one(r: dict) -> dict:
        prompt = build_prompt(r, shots, args.shot_chars,
                              ask_score=not args.label_only,
                              with_jk=not args.no_jk,
                              with_rejected=not args.no_rejected,
                              with_audit=args.audit)
        votes, confs, healths, reasons, usage = [], [], [], [], collections.Counter()
        errs: List[str] = []
        fps: set = set()
        for _ in range(args.k):
            resp = llm_generate_setup(prompt, model=args.model,
                                      temperature=args.temperature,
                                      json_format=True,
                                      max_tokens=args.max_tokens,
                                      reasoning_effort=args.effort,
                                      seed=args.api_seed)
            # llm.py normalises to input_tokens / output_tokens and keeps the
            # provider's own dict under raw_usage; the cached count lives there.
            # Reading the wrong key names is silent — the first run of this
            # script reported $0.00 for 90 calls.
            # A call that never returned and a reply that could not be parsed are
            # both `label=None` downstream, and they are not the same failure:
            # one is the API, one is the model. Keep them apart.
            if resp.get("error"):
                errs.append(str(resp["error"])[:200])
            if resp.get("system_fingerprint"):
                fps.add(str(resp["system_fingerprint"]))
            u = resp.get("usage") or {}
            raw = u.get("raw_usage") or {}
            usage["input"] += int(u.get("input_tokens") or 0)
            usage["output"] += int(u.get("output_tokens") or 0)
            usage["cached"] += int(
                ((raw.get("prompt_tokens_details") or {}) or {}).get("cached_tokens")
                or ((raw.get("input_tokens_details") or {}) or {}).get("cached_tokens")
                or 0)
            usage["calls"] += 1
            if int(u.get("output_tokens") or 0) >= args.max_tokens:
                usage["capped"] += 1
            p = parse(resp.get("text") or "")
            if p["label"]:
                votes.append(p["label"])
            if p["confidence"] is not None:
                confs.append(p["confidence"])
            if p.get("health") is not None:
                healths.append(p["health"])
            if p.get("reason"):
                reasons.append(p["reason"])
        # Majority vote. Ties and total parse failure are recorded, never guessed:
        # an arm that silently defaults to the majority class would look better
        # than it is.
        top = collections.Counter(votes).most_common()
        label = top[0][0] if top and (len(top) == 1 or top[0][1] > top[1][1]) else None
        return {"task_id": r["task_id"], "label": label, "votes": votes,
                "health": (float(np.mean(healths)) if healths else None),
                "agreement": (top[0][1] / len(votes)) if votes else 0.0,
                "confidence": float(np.mean(confs)) if confs else None,
                "reasons": reasons, "api_errors": errs,
                "fingerprints": sorted(fps),
                "true": r["label"], "usage": dict(usage),
                "n_selected": r.get("n_selected"), "n_rejected": r.get("n_rejected"),
                "trunc": r.get("trunc"), "dc_ops": r.get("dc_ops"),
                "prompt_chars": len(prompt)}

    t0 = time.time()
    results: List[dict] = []
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        for i, res in enumerate(ex.map(one, dev), 1):
            results.append(res)
            print(f"    {i}/{len(dev)}", end="\r", flush=True)
    print()

    capped = sum(r["usage"].get("capped", 0) for r in results)
    if capped:
        print(f"  [warn] {capped}/{sum(r['usage']['calls'] for r in results)} calls"
              f" hit max_tokens={args.max_tokens}; the reply was truncated and"
              f" the label most likely did not parse. Raise --max-tokens and re-run.")
    unparsed = [r for r in results if r["label"] is None]
    if unparsed:
        print(f"  [warn] {len(unparsed)} tasks have no usable label (parse failure or a tied vote);"
              f" counted as {OK}, which lowers recall on the two action classes - the conservative direction")
    failed = [r for r in results if r.get("api_errors")]
    if failed:
        # Distinct from `unparsed`: these tasks never got an answer at all, so
        # they measure the connection, not the model. If the count is more than a
        # couple the run should be repeated rather than reported.
        import collections as _c
        kinds = _c.Counter(e.split(":")[0] for r in failed for e in r["api_errors"])
        print(f"  [warn] {len(failed)}/{len(results)} tasks had a failed API call: "
              + "  ".join(f"{k} x{v}" for k, v in kinds.most_common(4))
              + "\n         these are not model judgements, they are calls that never returned; if the count is large, re-run rather than reporting it")
    pred = [r["label"] or OK for r in results]
    true = [r["true"] for r in results]

    tot = collections.Counter()
    for r in results:
        for k, v in r["usage"].items():
            tot[k] += v
    # Cached input is billed at a discount and the `--k` samples of one task
    # share an identical prefix, so ignoring `cached` overstates the bill —
    # materially, since the few-shot block is the bulk of every prompt and is
    # byte-identical across all tasks. Rates are gpt-4o's at the time of writing
    # and are only an estimate; the authoritative number is the provider's meter.
    # Rates PER MODEL, mirroring repair_loop.PRICES. Hard-coding gpt-4o's rates
    # priced a gpt-5 run at $4.17 when its own input rate is half that — $2.13.
    # The two files are the only places a dollar figure is produced, and they
    # disagreeing is worse than either being wrong.
    _PRICES = {"gpt-4o": {"in": 2.50, "cached": 1.25, "out": 10.0},
               "gpt-5":  {"in": 1.25, "cached": 0.125, "out": 10.0}}
    pr = _PRICES["gpt-5"] if args.model.startswith("gpt-5") else _PRICES["gpt-4o"]
    fresh = max(tot["input"] - tot["cached"], 0)
    cost = (fresh / 1e6 * pr["in"] + tot["cached"] / 1e6 * pr["cached"]
            + tot["output"] / 1e6 * pr["out"])
    cost_nocache = tot["input"] / 1e6 * pr["in"] + tot["output"] / 1e6 * pr["out"]
    n = len(results)

    res = evaluate([r["task_id"] for r in results], true, pred_labels=pred)
    ref = ({"hand-86 (reference)": {"macro_f1_actions": args.hand_ref,
                             "per_class": {}}} if args.hand_ref else None)
    print("\n" + render(res, f"LLM {args.model} shots={args.shots} k={args.k}",
                        extra_reference=ref))
    print(f"\n  vote agreement  median {np.median([r['agreement'] for r in results]):.2f}"
          f"   prompt median {int(np.median([r['prompt_chars'] for r in results])):,} chars")
    if tot["calls"] and not tot["input"]:
        print("  [warn] usage is 0 - the provider returned no token counts, so the cost estimate is not trustworthy")
    print(f"  usage {tot['calls']} calls   in {tot['input']:,} "
          f"(cached {tot['cached']:,}) / out {tot['output']:,} tok")
    print(f"  estimated ${cost:.2f}  (without the cache discount ${cost_nocache:.2f})   "
          f"${cost/max(n,1):.4f}/task   {time.time()-t0:.0f}s")
    if args.limit:
        print(f"  extrapolated to the 141 dev tasks  ~ ${cost / max(n, 1) * 141:.2f}")

    # ---- is `health` usable as a cross-state score? -----------------------
    # The loop ranks states by p_ok and returns the best one, so the score has to
    # VARY and has to track correctness. The previous LLM arm failed on the first
    # count alone: p_ok took 6 distinct values over 141 states, 85% of deltas were
    # exactly 0, and best-of-history therefore returned the unrepaired state 133
    # times out of 141 — 36 correctly-routed repairs produced 1 fix. This block
    # is the pre-check that says whether asking for `health` fixes that, BEFORE
    # another full arm is paid for.
    hs = [(r.get("health"), r["true"]) for r in results if r.get("health") is not None]
    if hs:
        import numpy as _np
        v = _np.array([h for h, _ in hs], float)
        ok = _np.array([t == "no_revision_needed" for _, t in hs])
        print(f"\nhealth score  n={len(hs)}/{len(results)}   distinct values {len(set(v.round(2)))}"
              f"   mean {v.mean():.1f}  sd {v.std():.1f}"
              f"   percentiles {_np.percentile(v,[10,50,90]).round(1).tolist()}")
        print(f"  healthy group mean {v[ok].mean():.1f}   broken group mean {v[~ok].mean():.1f}")
        try:
            from sklearn.metrics import roc_auc_score
            print(f"  AUC separating healthy from broken {roc_auc_score(ok, v):.3f}")
        except Exception:
            pass
        # THE CRITERION IS THE TIE RATE, NOT THE NUMBER OF DISTINCT VALUES.
        # Distinct values was the wrong proxy and said so on its first use:
        # gpt-4o produced only 9 values yet a tie rate of .208, BETTER than the
        # trained model's measured .28, because those 9 values are well spread.
        # What breaks best-of-history is two states scoring EQUAL — a repaired
        # state that ties its predecessor loses the argmax to it — so the
        # quantity to check is P(two states collide), estimated here as the
        # collision probability of the observed distribution.
        import collections as _c
        cnt = _c.Counter(v.round(4))
        tie = sum((c / len(v)) ** 2 for c in cnt.values())
        print(f"  tie rate (two states landing on the same score) {tie:.3f}"
              f"   reference: the old p_ok measured 0.85 (unusable), the trained model 0.28 (usable)")
        print("  Criterion: only a tie rate <= 0.35 AND an AUC >= 0.65 justifies re-running the whole arm with it.")

    with (args.out / "predictions_llm.jsonl").open("w") as fh:
        for r in results:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    (args.out / "report_llm.json").write_text(json.dumps(
        {"args": {k: str(v) for k, v in vars(args).items()},
         "result": res, "usage": dict(tot), "cost_usd": cost,
         "unparsed": len(unparsed)}, indent=1))
    print(f"\n-> {args.out}/report_llm.json, predictions_llm.jsonl")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
