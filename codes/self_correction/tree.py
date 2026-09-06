"""The repair search, as an explicit tree.

    root      the state pipeline synthesis produced, before any revision
    node      one state: a set of subtables plus the artefacts that produced it
    edge      the revise action that turned the parent state into this one

Two ways to grow it:

    DEPTH    revise a node again, so round 2 builds on round 1's output. This is
             what fixes a task needing two different repairs, and it is the only
             direction the original loop could go.
    BREADTH  run a DIFFERENT action from the same parent. The original loop
             reached this only by rolling back and retrying, which threw the
             candidate away; here both siblings stay in the tree and both remain
             selectable.

WHY BOTH, AND WHY THE TREE IS KEPT
----------------------------------
The localizer names the action to try, but four-class accuracy is 0.618 — hit@2
is 0.80 and expected rounds-to-hit is 1.68. A single chain therefore commits to a
guess that is wrong a third of the time, and its only recovery is to spend a
round discovering that. Breadth turns that into a choice made after seeing the
outcome.

Keeping every node matters for the same reason the original kept every round:
the answer is the BEST node, not the deepest one. The two decisions are
deliberately separate:

    delta > threshold   ->  this node is worth EXPANDING (a child builds on it)
    max p_ok            ->  this node is the ANSWER

The 0.05 threshold was calibrated for the first decision, where being wrong costs
the remaining budget. It is far too strict for the second, where being wrong
costs nothing. Measured on the original loop over 20 tasks: of the 3 tasks whose
metrics improved, 2 had deltas below the threshold and were rolled back —
bird_3f3aba77 at 0.0377 (subtable_full False -> True, join_key 0 -> 1) and
bird_fcdb05fc at 0.0007 (join_key 0 -> 1). Returning only kept states would have
scored 11/20 and 15/20 instead of 12/20 and 17/20.

Note what that says about delta: 0.0007 accompanied a real join-key fix, so its
MAGNITUDE carries almost no information. Only its sign is usable, and only at
0.758 agreement — which is why it gates expansion and never selection.

SCORING
-------
`p_ok` is the localizer's own P(no_revision_needed) on the state. It is the only
correctness estimate available without gold, and it was validated for exactly
this use: on 138 paired observations the sign of its delta agreed with the true
change 0.758 of the time.
"""

from __future__ import annotations

import itertools
import json
import time
import traceback
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Iterable, List, Optional, Sequence, Tuple

OK = "no_revision_needed"


@dataclass
class Node:
    """One state in the repair tree."""

    id: int
    state: Any                              # the State object; opaque here
    parent: Optional["Node"] = None
    action: Optional[str] = None            # the edge that produced this node
    depth: int = 0
    p_ok: Optional[float] = None            # localizer P(no_revision_needed)
    diag: Optional[dict] = None             # the diagnosis of THIS state
    ranked: List[Tuple[str, float]] = field(default_factory=list)
    children: List["Node"] = field(default_factory=list)
    usage: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None
    # Actions already attempted FROM this node, whether or not they produced a
    # child. Prevents breadth expansion from paying for the same action twice.
    tried: List[str] = field(default_factory=list)
    score: Optional[dict] = None            # gold score, when scoring is on

    @property
    def is_root(self) -> bool:
        return self.parent is None

    @property
    def delta(self) -> Optional[float]:
        """p_ok(this) - p_ok(parent); None at the root."""
        if self.parent is None or self.p_ok is None or self.parent.p_ok is None:
            return None
        return self.p_ok - self.parent.p_ok

    def path(self) -> List[str]:
        """The actions from the root down to this node."""
        out, n = [], self
        while n.parent is not None:
            out.append(n.action or "?")
            n = n.parent
        return list(reversed(out))

    def actions_on_path(self) -> set:
        return set(self.path())

    def summary(self) -> dict:
        """The columns and shape this node produced, per logical table.

        Recorded for EVERY node, not just the winner. Without it a run cannot be
        read back: two nodes with the same p_ok are indistinguishable in the
        record, so "the revision changed nothing" and "the revision changed the
        frame but the localizer scored it the same" look identical — and those
        call for opposite fixes. Frames themselves are not kept; columns and
        shape are what the question turns on.
        """
        produced = getattr(self.state, "produced", None) or {}
        out = {}
        for lt, df in produced.items():
            try:
                out[lt] = {"columns": [str(c) for c in df.columns],
                           "shape": list(df.shape)}
            except Exception:
                out[lt] = None
        return out

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "parent": self.parent.id if self.parent else None,
            "action": self.action,
            "depth": self.depth,
            "p_ok": None if self.p_ok is None else round(float(self.p_ok), 4),
            "delta": None if self.delta is None else round(float(self.delta), 4),
            "path": self.path(),
            "ranked": [[a, round(float(v), 4)] for a, v in self.ranked],
            "tried": list(self.tried),
            "usage": self.usage,
            "error": self.error,
            "score": self.score,
            "produced": self.summary(),
            # The tables this node SELECTED, not just the ones it produced.
            # `revise_table` changes the selection, so table identification
            # accuracy has to be read off the node that was finally chosen, not
            # off the first-pass selection file.
            "selected_tables": list(
                (getattr(self.state, "link", None) or {}).get("selected_tables") or []),
        }


class RepairTree:
    """Grow a tree of repaired states and return the best one.

    actions        {name: fn(state, diag, chains, cfg) -> new state or None}
    rank_fn        (diag, state, exclude) -> [(action, prob), ...]
    p_ok_fn        (diag, state) -> float
    diagnose_fn    state -> diag
    score_fn       optional, state -> gold score dict, for reporting only
    """

    def __init__(self,
                 actions: Dict[str, Callable],
                 rank_fn: Callable,
                 p_ok_fn: Callable,
                 diagnose_fn: Callable,
                 *,
                 max_depth: int = 3,
                 breadth: int = 1,
                 max_nodes: int = 8,
                 expand_threshold: float = 0.05,
                 trigger_threshold: Optional[float] = None,
                 action_order: Optional[Sequence[str]] = None,
                 score_fn: Optional[Callable] = None,
                 stop_when_fixed: bool = False,
                 chains: Optional[dict] = None,
                 cfg: Optional[dict] = None,
                 verbose: bool = True):
        self.actions = actions
        self.rank_fn = rank_fn
        self.p_ok_fn = p_ok_fn
        self.diagnose_fn = diagnose_fn
        self.score_fn = score_fn
        self.max_depth = max_depth
        self.breadth = breadth
        self.max_nodes = max_nodes
        self.expand_threshold = expand_threshold
        self.trigger_threshold = trigger_threshold
        self.action_order = list(action_order or actions)
        self.stop_when_fixed = stop_when_fixed
        self.chains = chains or {}
        self.cfg = cfg or {}
        self.verbose = verbose

        self.nodes: List[Node] = []
        self.root: Optional[Node] = None
        self._ids = itertools.count()
        self.stop_reason: str = ""

    # ---- construction ----------------------------------------------------
    def _make_node(self, state, parent: Optional[Node], action: Optional[str]) -> Node:
        n = Node(id=next(self._ids), state=state, parent=parent, action=action,
                 depth=0 if parent is None else parent.depth + 1)
        n.diag = self.diagnose_fn(state)
        n.p_ok = self.p_ok_fn(n.diag, state)
        n.ranked = self.rank_fn(n.diag, state, exclude=tuple(n.actions_on_path()))
        if self.score_fn is not None:
            n.score = self.score_fn(state)
        self.nodes.append(n)
        if parent is not None:
            parent.children.append(n)
        return n

    def _log(self, msg: str) -> None:
        if self.verbose:
            print(msg)

    # ---- the search ------------------------------------------------------
    def run(self, root_state) -> Node:
        """Grow the tree from `root_state` and return the best node."""
        self.root = self._make_node(root_state, None, None)
        self._log(f"  [tree] root p_ok={self.root.p_ok:.4f} "
                  f"ranked={[(a, round(v, 3)) for a, v in self.root.ranked[:3]]}")

        if not self._should_act(self.root):
            return self.best()

        # The frontier is ordered by p_ok, so expansion always continues from the
        # most promising state seen so far, not merely the most recent one.
        frontier: List[Node] = [self.root]

        while frontier and len(self.nodes) < self.max_nodes:
            frontier.sort(key=lambda n: -(n.p_ok or 0.0))
            parent = frontier.pop(0)
            if parent.depth >= self.max_depth:
                continue

            for action in self._actions_for(parent):
                if len(self.nodes) >= self.max_nodes:
                    self.stop_reason = f"node budget {self.max_nodes} reached"
                    break
                child = self._expand(parent, action)
                if child is None:
                    continue
                if self.stop_when_fixed and self._is_fixed(child):
                    self.stop_reason = "a child was diagnosed as fixed"
                    return self.best()
                # DEPTH: only a child that improved is worth building on. Its
                # siblings stay in the tree and stay selectable — they are simply
                # not expanded further.
                d = child.delta
                if d is not None and d > self.expand_threshold:
                    frontier.append(child)

        if not self.stop_reason:
            self.stop_reason = "frontier exhausted"
        return self.best()

    def _should_act(self, node: Node) -> bool:
        """Whether this state is worth repairing at all.

        Default rule: stop when the localizer ranks `no_revision_needed` first.
        With a trigger threshold, act whenever p_ok is below it instead — the
        asymmetry is measured: on 141 tasks the loop acted on 14 already-correct
        tasks and damaged NONE of them (best-of-tree returned the original every
        time), while 24 genuinely broken tasks were never attempted. False
        triggers cost money; missed triggers cost tasks.
        """
        thr = self.trigger_threshold
        if thr is None:
            if node.ranked and node.ranked[0][0] == OK:
                self.stop_reason = "localizer says no revision needed"
                return False
            return True
        if (node.p_ok or 0.0) >= thr:
            self.stop_reason = f"p_ok {node.p_ok:.3f} >= trigger threshold {thr}"
            return False
        return True

    def _actions_for(self, parent: Node) -> List[str]:
        """Which actions to run from this node, best first.

        `breadth` of 1 is the original loop: take the localizer's top action.
        Above 1, take its top-k, which is what hit@2 = 0.80 is there to exploit.
        An action already on this node's path is excluded — repeating it from a
        state it just produced is what the original's `tried` list prevented.
        """
        used = parent.actions_on_path() | set(parent.tried)
        ranked = [a for a, _ in parent.ranked if a != OK and a in self.actions
                  and a not in used]
        # Fall back to the configured order for anything the localizer did not
        # rank, so breadth is not silently capped by a short ranking.
        for a in self.action_order:
            if a in self.actions and a not in used and a not in ranked:
                ranked.append(a)
        return ranked[:max(1, self.breadth)]

    def _expand(self, parent: Node, action: str) -> Optional[Node]:
        """Run one action from `parent` and attach the result as a child."""
        parent.tried.append(action)
        t0 = time.perf_counter()
        try:
            new_state = self.actions[action](parent.state, parent.diag,
                                             self.chains, self.cfg)
        except Exception as exc:  # noqa: BLE001
            # The type and message alone are not enough to fix anything: two
            # rounds once died on `TypeError: can only concatenate str (not
            # "dict") to str` and locating it meant reading every concatenation
            # in the action's call path, because the frame that raised was gone
            # by the time the record was written.
            self._log(f"  [tree] {action} from node {parent.id} raised "
                      f"{type(exc).__name__}: {exc}")
            n = Node(id=next(self._ids), state=None, parent=parent, action=action,
                     depth=parent.depth + 1,
                     error=f"{type(exc).__name__}: {exc}")
            n.usage = {"elapsed_seconds": round(time.perf_counter() - t0, 2),
                       "traceback": traceback.format_exc()[-2000:]}
            self.nodes.append(n)
            parent.children.append(n)
            return None
        if new_state is None:
            self._log(f"  [tree] {action} from node {parent.id}: no change proposed")
            return None

        child = self._make_node(new_state, parent, action)
        child.usage = {"elapsed_seconds": round(time.perf_counter() - t0, 2)}
        # Say whether the frame actually moved. A zero delta means two very
        # different things depending on this, and the record must distinguish
        # them: "the action proposed nothing" vs "it rewrote the table and the
        # localizer scored it the same".
        changed = child.summary() != parent.summary()
        self._log(f"  [tree] node {child.id} = {action} from {parent.id}  "
                  f"p_ok {parent.p_ok:.4f} -> {child.p_ok:.4f} "
                  f"(delta {child.delta:+.4f}, tables "
                  f"{'CHANGED' if changed else 'unchanged'})")
        return child

    def _is_fixed(self, node: Node) -> bool:
        return bool(node.ranked and node.ranked[0][0] == OK)

    # ---- results ---------------------------------------------------------
    def best(self) -> Node:
        """The highest-p_ok node, ties going to the shallowest then earliest.

        Selection deliberately ignores the expansion threshold: a node rolled
        back for expansion purposes is still a candidate answer.
        """
        live = [n for n in self.nodes if n.state is not None and n.p_ok is not None]
        if not live:
            return self.root
        return max(live, key=lambda n: (n.p_ok, -n.depth, -n.id))

    def to_dict(self) -> dict:
        b = self.best()
        return {
            "nodes": [n.to_dict() for n in self.nodes],
            "root": self.root.id if self.root else None,
            "best": b.id if b else None,
            "best_path": b.path() if b else [],
            "best_p_ok": None if not b or b.p_ok is None else round(float(b.p_ok), 4),
            "n_nodes": len(self.nodes),
            "max_depth_reached": max((n.depth for n in self.nodes), default=0),
            "stop": self.stop_reason,
        }

    def render(self) -> str:
        """The tree as indented text, for a run log."""
        lines = []

        def walk(n: Node, prefix: str = "") -> None:
            tag = "root" if n.is_root else n.action
            p = "  --" if n.p_ok is None else f"{n.p_ok:6.4f}"
            d = "" if n.delta is None else f" ({n.delta:+.4f})"
            mark = " <- BEST" if n is self.best() else ""
            err = f"  ERROR {n.error}" if n.error else ""
            lines.append(f"{prefix}[{n.id}] {tag:<24} p_ok={p}{d}{mark}{err}")
            for c in n.children:
                walk(c, prefix + "    ")

        if self.root:
            walk(self.root)
        lines.append(f"stop: {self.stop_reason}")
        return "\n".join(lines)
