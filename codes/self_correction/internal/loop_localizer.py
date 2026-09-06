#!/usr/bin/env python3
"""
loop_localizer.py
=================
The three localizers behind one interface, so `repair_loop.py` can run any of
them as an arm without knowing what is inside.

    staged   the trained two-stage model  (checkpoint + frozen per-table head)
    remote   the same model, over HTTP     (loop local, GPU remote)
    llm      an LLM asked for the label   (the baseline; one API call per state)
    hand     the 86 diagnostics           (multinomial L1, the incumbent)

WHY AN ADAPTER RATHER THAN THREE LOOPS
--------------------------------------
The downstream question is what the localizer is WORTH, and that is a difference
between arms: same repair actions, same acceptance rule, same round budget, one
variable changed. Three separate scripts would not hold the rest fixed, and the
first thing anyone would ask about a gain is whether it came from the localizer
or from something else that moved with it.

WHAT EACH ONE NEEDS, AND WHY THE PROTOCOL GREW A `state`
--------------------------------------------------------
`prep_utils.localize` localizers read `diag`, a flat dict of 86 diagnostics, so
`p_ok(diag)` was enough. The trained model does not read diagnostics — it reads
the EVIDENCE TEXT, rebuilt from the raw tables, the plan and the produced
subtables, none of which survive into `diag`. Same for the LLM. So the two
text-based arms declare `wants_state = True` and get the `State` object as well;
`hand` ignores it and the old classes are untouched.

Every arm exposes `p_ok`, `rank`, `delta`, `accept` and `delta_threshold`, which
is exactly what the loop calls.

THE ACCEPTANCE RULE IS NOT COMPARABLE ACROSS ARMS AND MUST BE SET PER ARM
------------------------------------------------------------------------
`accept` keeps a repair when `p_ok(after) - p_ok(before) > delta_threshold`. The
default .05 was calibrated against the hand localizer's p_ok scale. A softmax
over three logits does not live on that scale, and an LLM's confidence/100 lives
on no scale at all — it is nearly always .8 or .9, so a delta rule on it accepts
almost nothing. `--delta-threshold` therefore has to be set per arm, and the
honest default here is 0.0: keep a repair unless the localizer says it got
worse. That is the rule the repair-acceptance experiment already settled on
("no visible regression" rather than "must improve"), because the observables
saturate and a positive threshold rejects everything.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
for _p in (str(ROOT), str(ROOT / "prep_utils"), str(ROOT / "training"),
           str(ROOT / "construct_training_data")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

OK = "no_revision_needed"
CLASSES = (OK, "revise_table", "revise_pipeline")

# Set by repair_loop to its `meter_add`, so a localizer that spends money is
# counted in the same per-task ledger as the repair actions. Without it the LLM
# arm reported only what the REVISE calls cost — its own 300-odd localizer calls,
# the thing the arm exists to pay for, were invisible in every cost table.
METER = None
MIN_SELECTED_TABLES = 2


# --------------------------------------------------------------------------- #
# shared
# --------------------------------------------------------------------------- #
class _Base:
    """Ranking, the contract short-circuit, and the acceptance rule.

    Subclasses supply `_posterior(diag, state) -> [p_ok, p_table, p_pipeline]`
    and nothing else, so the three arms cannot drift apart on the parts that are
    supposed to be identical.
    """

    wants_state = False
    delta_threshold = 0.0
    # The `n_selected < 2` contract check. True for OUR arms, where it is part of
    # the deployed localizer; False for the LLM baseline, which must be the model
    # alone or the comparison is against model-plus-rule.
    use_contract_rule = True
    # Does this localizer produce a scalar that can be COMPARED ACROSS STATES?
    #
    # The loop's `max(history, key=p_ok)` needs one; the trigger and the routing
    # do not. Our model emits a calibrated three-way softmax, so it has one for
    # free. An LLM asked to classify emits a LABEL — demanding a scalar as well
    # gives the baseline an interface it does not natively have, and the first
    # attempt at faking one (label confidence) put 106 of 141 states at exactly
    # .05 and made best-of-history return the unrepaired state 133 times.
    #
    # So the two kinds get the selection rule that fits what they produce, and
    # the ABILITY to produce a usable score is reported as a property of the
    # method rather than papered over.
    emits_score = True

    def _posterior(self, diag, state=None) -> np.ndarray:
        raise NotImplementedError

    # ---- interface the loop calls ----------------------------------------
    def p_ok(self, diag: Dict[str, Any], state=None) -> float:
        return float(self._posterior(diag, state)[0])

    def rank(self, diag: Dict[str, Any], exclude: Sequence[str] = (),
             link: Optional[Dict[str, Any]] = None, state=None,
             min_tables: int = MIN_SELECTED_TABLES) -> List[Tuple[str, float]]:
        ex = set(exclude)
        p = self._posterior(diag, state)
        out = {c: float(v) for c, v in zip(CLASSES, p)}
        # `revise_relational_plan` is in the loop's action set but not in this
        # three-class label space. It is ranked last with a nominal score rather
        # than dropped, so `--all-actions` and `exclude`-driven fallback still
        # reach it and the arms differ only in the classes they actually predict.
        out.setdefault("revise_relational_plan", 0.0)
        # Schema linking's own prompt says the selection is two tables or more,
        # so fewer than two violates the stage's contract without consulting
        # gold. It is deployed behaviour and part of OUR localizer.
        #
        # IT IS NOT PART OF THE LLM BASELINE, and giving it to that arm made two
        # arms that are supposed to differ by their localizer differ by a rule as
        # well. On dev the rule fires on 7 tasks whose label is `revise_table` in
        # every case; it answered all 7 correctly for free, while gpt-5 asked
        # about the same 7 without it answered 2, 3 and 2 across three runs. That
        # is roughly the whole of a .047 macro-recall gap that was reported as a
        # difference between the two models. `llm_localizer.py`, the offline
        # baseline, has never had the rule, so the loop arm now matches it.
        if self.use_contract_rule and link is not None and "revise_table" not in ex:
            if len(link.get("selected_tables") or []) < min_tables:
                rest = [(a, v) for a, v in sorted(out.items(), key=lambda kv: -kv[1])
                        if a not in ex | {"revise_table"}]
                return [("revise_table", 1.0)] + rest
        return [(a, v) for a, v in sorted(out.items(), key=lambda kv: -kv[1])
                if a not in ex]

    def delta(self, before, after, s_before=None, s_after=None) -> float:
        return self.p_ok(after, s_after) - self.p_ok(before, s_before)

    def accept(self, before, after, s_before=None, s_after=None) -> bool:
        return self.delta(before, after, s_before, s_after) > self.delta_threshold


# Overridable so the evidence WIDTH can be swept without touching call sites.
# ev_1 lists the selected tables first and the REJECTED ones last, and the
# rejected tables are the strongest evidence for revise_table (see
# dataset.anonymize_row). ev_1 is capped at 3072 tokens, so on a benchmark whose
# states are much wider than training the tail — i.e. exactly that evidence — is
# what truncation removes. Median columns per task: spider 20, bird 58, beaver
# 212, against a training median of 58. On beaver the remote localizer predicted
# revise_table for 1 of 119 tasks (true label: 93), and 0 of the 49 tasks where
# a better table was actually available, which is BELOW its own training prior
# of 13-23% — a prior-reverting model would still emit it sometimes.
# Narrowing each table lets all of them fit, which is a hypothesis about
# truncation, not a tuning knob: sweep it, do not guess it.
_MAX_COLS = int(os.environ.get("LOOP_EVIDENCE_MAX_COLS", "40"))
_N_VALS = int(os.environ.get("LOOP_EVIDENCE_N_VALS", "6"))


def _evidence(state, anonymize: bool, max_cols: int = None, n_vals: int = None) -> Dict:
    """Rebuild the exported row from a live loop State.

    Cached ON THE STATE, not in a dict keyed by id(): the loop drops all but one
    State per task after each round, and CPython reuses ids, so an id-keyed cache
    can return another task's evidence. This is the kind of bug that produces a
    plausible number.
    """
    max_cols = _MAX_COLS if max_cols is None else max_cols
    n_vals = _N_VALS if n_vals is None else n_vals
    hit = getattr(state, "_evidence_cache", None)
    if hit is not None:
        return hit
    from evidence_text import build_evidence, joinkey_features
    shard = {"subtables": state.produced, "edges": state.edges}
    ev = build_evidence(state.task, state.link, state.plan, shard,
                        state.bench_dir, max_cols=max_cols, n_vals=n_vals)
    jkf = joinkey_features(shard)
    ev["jk"] = [float(jkf.get(k, 0.0) or 0.0) for k in _JK_NAMES]
    ev["task_id"] = state.task.get("task_id") or state.task.get("id") or ""
    ev["label"] = OK          # unused; keeps the row shaped like an export row
    if anonymize:
        from dataset import anonymize_row
        ev = anonymize_row(ev)
    state._evidence_cache = ev
    return ev


_JK_NAMES = ("jk_containment", "jk_jaccard", "jk_yield", "jk_fanout",
             "jk_left_unique", "jk_right_unique", "jk_left_nonnull",
             "jk_right_nonnull", "jk_present")


# --------------------------------------------------------------------------- #
# arm: the trained two-stage model
# --------------------------------------------------------------------------- #
class StagedLoopLocalizer(_Base):
    wants_state = True

    def __init__(self, checkpoint: Path, meta: Path, device: Optional[str] = None,
                 anonymize: bool = True, delta_threshold: float = 0.0,
                 batch: int = 1):
        import torch
        from model_staged import load_checkpoint
        self.delta_threshold = delta_threshold
        self.anonymize = anonymize
        if device is None:
            device = ("cuda" if torch.cuda.is_available()
                      else "mps" if torch.backends.mps.is_available() else "cpu")
        self.device = device
        ck = torch.load(checkpoint, map_location="cpu", weights_only=False)
        st = json.loads(Path(meta).read_text())["special_tokens"]
        self.model, self.tok, self.cfg = load_checkpoint(ck, st, device)
        self.tables = bool(getattr(self.model.cfg, "per_table", False))
        if self.tables and not any(n.startswith("tab_head")
                                   for n in ck["state_dict"]):
            raise SystemExit(
                f"{checkpoint} is a --per-table model but its state_dict has no tab_head. "
                "That is a bug in an early run.py (the frozen parameters were not saved), so "
                "the head loads as random. Re-train with the fixed run.py before using it downstream.")
        self.batch = batch
        self._n = 0

    def _posterior(self, diag, state=None) -> np.ndarray:
        if state is None:
            raise RuntimeError("StagedLoopLocalizer needs a state; "
                               "the repair loop must call it the wants_state way")
        cached = getattr(state, "_post_cache", None)
        if cached is not None:
            return cached
        import torch
        from torch.utils.data import DataLoader
        from dataset import Collator, DEFAULT_MAXLEN, StateDataset
        row = _evidence(state, self.anonymize)
        dl = DataLoader(StateDataset([row], tables=self.tables), batch_size=1,
                        collate_fn=Collator(self.tok, DEFAULT_MAXLEN,
                                            tables=self.tables))
        b = next(iter(dl))
        bb = {k: (v.to(self.device) if hasattr(v, "to") else v) for k, v in b.items()}
        with torch.no_grad():
            p = torch.softmax(self.model(bb)["logits"], -1)[0].float().cpu().numpy()
        del bb
        if self.device == "cuda":
            torch.cuda.empty_cache()
        state._post_cache = p
        self._n += 1
        return p

    def report(self) -> str:
        return f"staged: {self._n} forward passes"


class RemoteLoopLocalizer(_Base):
    """Same arm as `staged`, with the forward pass on the machine that has the GPU.

    The loop has to run where the data is — `repair_loop` re-runs schema linking
    and re-synthesises pipelines against the benchmark's pickles, and its states
    exist only in that process. The model has to run where the encoder weights
    and the GPU are. This is the seam between those two facts: evidence text out,
    three probabilities back.

    Table names are anonymised CLIENT-SIDE, before the request, so the two ends
    cannot disagree about what the model read and no real file name is sent.

    Retries are deliberate but bounded. A single dropped request would otherwise
    abort a task that has already paid for several LLM calls; an endpoint that is
    genuinely down should still stop the run rather than have every state fall
    back to a default posterior, which would silently turn this arm into a
    constant classifier.
    """

    wants_state = True

    def __init__(self, url: str = "http://127.0.0.1:8077", anonymize: bool = True,
                 delta_threshold: float = 0.0, timeout: float = 120.0,
                 retries: int = 2):
        import urllib.request
        self.url = url.rstrip("/")
        self.anonymize = anonymize
        self.delta_threshold = delta_threshold
        self.timeout, self.retries = timeout, retries
        self._n = 0
        try:
            with urllib.request.urlopen(self.url + "/health", timeout=10) as r:
                h = json.loads(r.read())
            self.health = h
        except Exception as exc:
            raise SystemExit(
                f"cannot reach {self.url}: {type(exc).__name__}: {exc}\n"
                f"server: python training/serve_localizer.py --checkpoint ... --meta ...\n"
                f"tunnel: ssh -N -L 8077:localhost:8077 <user>@<host>") from None

    def _posterior(self, diag, state=None) -> np.ndarray:
        if state is None:
            raise RuntimeError("RemoteLoopLocalizer needs a state")
        cached = getattr(state, "_post_cache", None)
        if cached is not None:
            return cached
        import urllib.error
        import urllib.request
        row = _evidence(state, self.anonymize)
        body = json.dumps({k: row.get(k) for k in
                           ("question", "ev_1", "ev_2", "ev_3", "tables_1",
                            "jk", "task_id", "label")}).encode()
        last = None
        for attempt in range(self.retries + 1):
            try:
                req = urllib.request.Request(
                    self.url + "/posterior", data=body,
                    headers={"Content-Type": "application/json"})
                with urllib.request.urlopen(req, timeout=self.timeout) as r:
                    p = np.array(json.loads(r.read())["posterior"], dtype=float)
                state._post_cache = p
                self._n += 1
                return p
            except Exception as exc:                       # noqa: BLE001
                last = exc
                if attempt < self.retries:
                    import time as _t
                    _t.sleep(1.5 * (attempt + 1))
        raise RuntimeError(f"the localizer service failed ({self.retries + 1} attempts): "
                           f"{type(last).__name__}: {last}")

    def report(self) -> str:
        h = getattr(self, "health", {})
        return (f"remote {self.url}  device {h.get('device')}  "
                f"per_table {h.get('per_table')}  {self._n} requests this run")


# --------------------------------------------------------------------------- #
# arm: the LLM baseline
# --------------------------------------------------------------------------- #
class LLMLoopLocalizer(_Base):
    """One API call per state, including every candidate the loop proposes.

    COST IS NOT A FOOTNOTE HERE. A round-0 pass over dev is 141 calls; inside the
    loop every proposed successor is re-diagnosed too, so `--all-actions` with
    three rounds multiplies that by roughly the action count per round. Round-0
    alone measured $12.4 at k=3 and about a third of that at k=1, which is why
    k defaults to 1 in this class and the call count is printed at the end.
    """

    wants_state = True

    def __init__(self, model: str = "gpt-4o-2024-08-06", shots: Optional[List] = None,
                 shot_chars: int = 2500, k: int = 1, temperature: float = 0.0,
                 max_tokens: int = 0, anonymize: bool = True,
                 delta_threshold: float = 0.0, use_score: bool = False,
                 effort: str = "minimal", with_jk: bool = True,
                 with_rejected: bool = True, with_audit: bool = False):
        # These two must be passed through explicitly. They were not, and the
        # result was that an offline arm run with `--no-jk` and the loop arm it
        # was supposed to correspond to were built from different prompts.
        self.with_jk, self.with_rejected = with_jk, with_rejected
        self.with_audit = with_audit
        # Matches `llm_localizer.py`, which has no contract rule.
        self.use_contract_rule = False
        self.delta_threshold = delta_threshold
        self.emits_score = bool(use_score)
        self.effort = effort
        self.anonymize = anonymize
        self.model, self.k = model, k
        self.shots = shots or []
        self.shot_chars, self.temperature = shot_chars, temperature
        self.max_tokens = max_tokens or (4096 if model.startswith("gpt-5") else 512)
        self.usage = {"calls": 0, "input": 0, "output": 0}

    def _posterior(self, diag, state=None) -> np.ndarray:
        if state is None:
            raise RuntimeError("LLMLoopLocalizer needs a state")
        cached = getattr(state, "_post_cache", None)
        if cached is not None:
            return cached
        import collections
        from llm import llm_generate_setup
        from llm_localizer import build_prompt, parse
        row = _evidence(state, self.anonymize)
        prompt = build_prompt(row, self.shots, self.shot_chars,
                              ask_score=self.emits_score,
                              with_jk=self.with_jk,
                              with_rejected=self.with_rejected,
                              with_audit=self.with_audit)
        votes, confs, healths = [], [], []
        for _ in range(self.k):
            r = llm_generate_setup(prompt, model=self.model,
                                   temperature=self.temperature,
                                   json_format=True, max_tokens=self.max_tokens,
                                   reasoning_effort=self.effort)
            self.usage["calls"] += 1
            self.usage["input"] += r.get("input_tokens", 0)
            self.usage["output"] += r.get("output_tokens", 0)
            if METER is not None:
                METER({"input": r.get("input_tokens", 0),
                       "output": r.get("output_tokens", 0), "calls": 1,
                       "model": self.model}, self.model)
            d = parse(r.get("text") or r.get("content") or "")
            if d.get("label") in CLASSES:
                votes.append(d["label"])
                confs.append(d.get("confidence"))
                healths.append(d.get("health"))
        p = np.full(3, 1.0 / 3)
        if votes:
            top, n = collections.Counter(votes).most_common(1)[0]
            # p_ok COMES FROM `health`, NOT FROM THE LABEL'S CONFIDENCE.
            #
            # The loop uses p_ok twice and the two uses want different things: to
            # decide whether to act (a property of THIS state) and to rank states
            # against each other (a comparison ACROSS states). Label confidence
            # answers neither — it is a self-report about the label, it sits near
            # .9 almost always, and using it made 106 of 141 states score exactly
            # .05. Deltas were then 0 for 85% of candidates, best-of-history
            # returned the unrepaired state 133 times out of 141, and 36
            # correctly-routed repairs produced one fix.
            #
            # `health` is asked for separately and explicitly as a cross-state
            # quantity. Measured on 141 dev states with gpt-5: 24 distinct values,
            # collision probability .085 (the trained model's is .28), AUC .726
            # for healthy-vs-broken. With gpt-4o it also separates (.681) but the
            # LABEL collapses — `no_revision_needed` predicted twice in 141 — so
            # this fixes ranking, not a weak model.
            h = [x for x in healths if x is not None] if self.emits_score else []
            if h:
                p_ok = min(max(float(np.mean(h)) / 100.0, 0.01), 0.99)
                rest = 1.0 - p_ok
                p = np.full(3, rest / 2)
                p[0] = p_ok
                if top != OK:
                    # The remaining mass goes to the label the model named, so
                    # ranking among the failure classes still follows the label
                    # while the OK-vs-broken decision follows `health`.
                    p[:] = [p_ok, rest * 0.15, rest * 0.15]
                    p[CLASSES.index(top)] = rest * 0.85
                else:
                    p = np.array([p_ok, rest / 2, rest / 2])
            else:
                # LABEL ONLY. A fixed shape carrying the vote share and nothing
                # else — the point of this mode is that the model is not asked
                # for a magnitude, so none is invented. The loop reads only the
                # ARGMAX of this, and selects states by the label, not by p_ok.
                share = n / max(len(votes), 1)
                p = np.full(3, (1.0 - share) / 2)
                p[CLASSES.index(top)] = share
            p = p / p.sum()
        state._post_cache = p
        return p

    def report(self) -> str:
        # The prompt variant is printed, not assumed. Two arms that differ only
        # in which evidence blocks the prompt carries are not comparable, and the
        # difference is otherwise invisible in the log — the `--effort` mix-up
        # that cost a day was exactly this failure mode.
        return (f"llm {self.model} k={self.k} effort={self.effort} "
                f"shots={len(self.shots)}@{self.shot_chars or 'full'} "
                f"{'score' if self.emits_score else 'label-only'} "
                f"jk={'on' if self.with_jk else 'OFF'} "
                f"rejected={'on' if self.with_rejected else 'OFF'} "
                f"audit={'ON' if self.with_audit else 'off'} "
                f"contract_rule={'on' if self.use_contract_rule else 'OFF'}: "
                f"{self.usage['calls']} calls  "
                f"in {self.usage['input']:,} / out {self.usage['output']:,}")


# --------------------------------------------------------------------------- #
# arm: the 86 hand diagnostics
# --------------------------------------------------------------------------- #
class HandLoopLocalizer(_Base):
    """The incumbent, fitted here so the arm cannot silently use a stale model.

    Reads `diag` only, like the classes in `prep_utils.localize` — the point of
    this arm is that it needs nothing the loop does not already compute.
    """

    wants_state = False

    def __init__(self, train: Path, delta_threshold: float = 0.0, C: float = 1.0):
        from sklearn.linear_model import LogisticRegression
        from sklearn.preprocessing import StandardScaler
        self.delta_threshold = delta_threshold
        rows = [json.loads(l) for l in Path(train).open() if l.strip()]
        rows = [r for r in rows if r.get("hand")]
        meta = json.loads(Path(str(train).replace(".jsonl", ".meta.json")).read_text())
        self.cols = list(meta["hand_names"])
        X = np.nan_to_num(np.array([r["hand"] for r in rows], float))
        y = np.array([CLASSES.index(r["label"]) for r in rows])
        self.sc = StandardScaler().fit(X)
        self.clf = LogisticRegression(C=C, penalty="l1", solver="saga",
                                      max_iter=8000).fit(self.sc.transform(X), y)
        self.classes_ = list(self.clf.classes_)

    def _posterior(self, diag, state=None) -> np.ndarray:
        import pandas as pd
        from localize import flatten
        v = (pd.Series(flatten(diag), dtype="float64").reindex(self.cols)
             .fillna(0.0).to_numpy(float).reshape(1, -1))
        pr = self.clf.predict_proba(self.sc.transform(np.nan_to_num(v)))[0]
        out = np.zeros(3)
        for i, c in enumerate(self.classes_):
            out[int(c)] = pr[i]
        return out

    def report(self) -> str:
        return f"hand: {len(self.cols)} diagnostic features, L1 multinomial"


# --------------------------------------------------------------------------- #
def build(kind: str, args) -> _Base:
    """One place where an arm is chosen, so `repair_loop` stays a loop."""
    if kind == "staged":
        return StagedLoopLocalizer(args.staged_checkpoint, args.staged_meta,
                                   anonymize=not args.no_anonymize,
                                   delta_threshold=args.delta_threshold or 0.0)
    if kind == "remote":
        return RemoteLoopLocalizer(args.localizer_url,
                                   anonymize=not args.no_anonymize,
                                   delta_threshold=args.delta_threshold or 0.0)
    if kind == "llm":
        shots = []
        if args.llm_shots and args.llm_train:
            from llm_localizer import pick_shots
            pool = [json.loads(l) for l in Path(args.llm_train).open() if l.strip()]
            if not args.no_anonymize:
                from dataset import anonymize_row
                pool = [anonymize_row(r) for r in pool]
            shots = pick_shots(pool, args.llm_shots, 0)
        return LLMLoopLocalizer(model=args.llm_model, shots=shots, k=args.llm_k,
                                anonymize=not args.no_anonymize,
                                delta_threshold=args.delta_threshold or 0.0,
                                use_score=bool(getattr(args, "llm_use_score", False)),
                                effort=getattr(args, "llm_effort", "minimal"),
                                with_jk=not getattr(args, "llm_no_jk", False),
                                with_rejected=not getattr(args, "llm_no_rejected",
                                                          False),
                                with_audit=bool(getattr(args, "llm_audit", False)),
                                shot_chars=int(getattr(args, "llm_shot_chars", 2500)))
    if kind == "hand":
        return HandLoopLocalizer(args.hand_train,
                                 delta_threshold=args.delta_threshold or 0.0)
    raise SystemExit(f"unknown localizer kind {kind!r}")
