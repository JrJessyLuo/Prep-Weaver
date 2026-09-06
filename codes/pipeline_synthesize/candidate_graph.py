"""Joint candidate selection as maximum-weight clique on a complete multipartite graph.

WHAT THIS REPLACES
------------------
Stage 2 of pipeline synthesis searches an operator chain per logical table and
keeps up to `limit` finished candidates for each. Those per-table pools must
then be combined into ONE selection, and the choice cannot be made per table:
the candidate that looks best alone is often the one that breaks the join.

The original `_join_aware_select` enumerated the full Cartesian product of the
pools and scored every combination with `_combination_score`. That is correct
but does |pool|^|tables| work — 6 candidates over 7 tables is 279,936 scored
combinations, and every one of them re-derives the same pairwise join terms.

THE GRAPH
---------
    part          one logical table of the relational schema
    node          one terminal candidate of that table
    node weight   how well that candidate alone realises its declared schema
    edge weight   how well two candidates join, over the declared join edges

Every node of one part is compatible with every node of another (any candidate
of table A can be paired with any candidate of table B), so the graph is
COMPLETE multipartite. A clique therefore contains at most one node per part,
and a maximum clique contains exactly one — i.e. cliques are exactly the
selections, and maximum-weight clique is exactly the selection problem.

WHY THIS IS AN EXACT REFORMULATION, NOT AN APPROXIMATION
--------------------------------------------------------
`_combination_score` is a sum of terms that each involve either ONE table or
TWO, so it decomposes exactly:

    score(S) = Σ_t  [ 2.0 * name_coverage(t) + 0.25 * candidate_score(t) ]   <- node
             + Σ_e  [ join term for edge e ]                                  <- edge
             + Σ_e' [ -2.0 for each edge whose table is absent ]              <- const

The join term for an edge e between tables (l, r) depends only on the two
candidates chosen for l and r:

    both value sets readable and non-empty
        2.0 * max(|L∩R|/min(|L|,|R|), |L∩R|/|L|, |L∩R|/|R|)
        + 0.25 * key_quality(l) + 0.25 * key_quality(r)
    a declared key column missing from the frame     -> -1.0
    a value set empty                                ->  0.0

The constant term counts edges naming a table that has no candidate pool at
all. It is the same for every selection, so it cannot change which selection
wins; it is carried anyway so the reported score matches the original exactly.

Because the decomposition is exact and the graph is complete multipartite, an
exact maximum-weight clique equals the exhaustive argmax by construction. The
reformulation is a change of algorithm, not of objective — see
`verify_graph_alignment.py`, which checks it on real candidate pools.

WHY IT IS ALSO CHEAPER
----------------------
The product scores |pool|^|parts| combinations, each recomputing pairwise
terms. The graph computes each pairwise term once: Σ over part pairs of
|A|x|B|. For 7 tables x 6 candidates that is 756 pair evaluations instead of
279,936 combination evaluations, before the search even starts.

THE SOLVER
----------
See `max_weight_clique` below for the algorithm and its provenance.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from itertools import product
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple

import pandas as pd


# --------------------------------------------------------------------------- #
# value helpers (identical semantics to the originals)
# --------------------------------------------------------------------------- #

def _cf(x: Any) -> str:
    return re.sub(r"[^a-z0-9]", "", str(x).lower())


def key_quality(df: pd.DataFrame, col: Any) -> float:
    """min(non-null rate, uniqueness) — how key-like a column actually is."""
    m = {_cf(c): c for c in df.columns}
    real = m.get(_cf(col))
    if real is None:
        return 0.0
    s = df[real]
    if isinstance(s, pd.DataFrame):
        s = s.iloc[:, 0]
    if len(s) == 0:
        return 0.0
    nn = float(s.notna().mean())
    uq = float(s.dropna().astype(str).nunique() / max(int(s.notna().sum()), 1))
    return min(nn, uq)


def default_col_values(df: pd.DataFrame, col: Any):
    """Value set of a column, or None when the column is absent.

    The engine ships its own `col_values`; this is the fallback so the graph can
    be built and tested without importing the whole search stack.
    """
    m = {_cf(c): c for c in df.columns}
    real = m.get(_cf(col))
    if real is None:
        return None
    s = df[real]
    if isinstance(s, pd.DataFrame):
        s = s.iloc[:, 0]
    return set(s.dropna().astype(str).tolist())


class ValueCache:
    """Memoises value sets and key quality per (frame, column).

    `col_values` materialises the WHOLE column with no truncation, so on a
    million-row table one call costs a second or two. Keyed on id(frame), which
    is sound because the graph holds every candidate frame alive for its own
    lifetime — the cache never outlives them.
    """

    __slots__ = ("_v", "_k", "_values_fn")

    def __init__(self, values_fn: Optional[Callable] = None) -> None:
        self._v: Dict[tuple, Any] = {}
        self._k: Dict[tuple, float] = {}
        self._values_fn = values_fn or default_col_values

    def values(self, df: pd.DataFrame, col: Any):
        key = (id(df), _cf(col))
        if key not in self._v:
            self._v[key] = self._values_fn(df, col)
        return self._v[key]

    def key_quality(self, df: pd.DataFrame, col: Any) -> float:
        key = (id(df), _cf(col))
        if key not in self._k:
            self._k[key] = key_quality(df, col)
        return self._k[key]


# --------------------------------------------------------------------------- #
# weights — the exact terms of the original objective
# --------------------------------------------------------------------------- #

W_COVER = 2.0        # weight on per-table declared-schema name coverage
W_CAND = 0.25        # weight on the search's own candidate score
W_OVERLAP = 2.0      # weight on cross-table join-key value overlap
W_KEY_QUALITY = 0.25 # weight on each side's key quality
P_MISSING_COLUMN = -1.0   # a declared join column absent from the frame
P_MISSING_TABLE = -2.0    # an edge naming a table with no candidate pool


def node_weight(candidate: dict, declared_schema) -> float:
    """How well one candidate alone realises its table's declared schema."""
    df = candidate["df"]
    required = {_cf(c) for c in (declared_schema or {})}
    present = {_cf(c) for c in df.columns}
    cover = len(required & present) / max(len(required), 1)
    return W_COVER * cover + W_CAND * float(candidate.get("score") or 0.0)


def edge_weight(left_candidate: dict, right_candidate: dict,
                edges: Sequence[dict], cache: ValueCache) -> float:
    """Join quality between two candidates, summed over the edges joining them."""
    ldf, rdf = left_candidate["df"], right_candidate["df"]
    total = 0.0
    for e in edges:
        lv = cache.values(ldf, e["left_on"])
        rv = cache.values(rdf, e["right_on"])
        if lv is None or rv is None:
            total += P_MISSING_COLUMN
            continue
        if not lv or not rv:
            continue
        inter = len(lv & rv)
        total += W_OVERLAP * max(inter / max(min(len(lv), len(rv)), 1),
                                 inter / max(len(lv), 1),
                                 inter / max(len(rv), 1))
        total += W_KEY_QUALITY * cache.key_quality(ldf, e["left_on"])
        total += W_KEY_QUALITY * cache.key_quality(rdf, e["right_on"])
    return total


# --------------------------------------------------------------------------- #
# the graph
# --------------------------------------------------------------------------- #

@dataclass
class CandidateNode:
    """One terminal candidate of one logical table."""
    part: str                 # logical table id, e.g. "table_2"
    index: int                # rank within its part, best-scoring first
    candidate: dict           # {df, chain, steps, score, ok, ...}
    weight: float = 0.0

    def __repr__(self) -> str:
        return f"<{self.part}#{self.index} w={self.weight:.3f}>"


@dataclass
class MultipartiteCandidateGraph:
    """Complete multipartite graph over the per-table candidate pools.

    parts     logical tables, in the order the schema declares them
    nodes     part -> its candidates, ordered best-scoring first
    pair_w    (part_a, part_b) -> matrix of edge weights, a before b in `parts`
    const     score terms that no selection can change
    """
    parts: List[str] = field(default_factory=list)
    nodes: Dict[str, List[CandidateNode]] = field(default_factory=dict)
    pair_w: Dict[Tuple[str, str], List[List[float]]] = field(default_factory=dict)
    const: float = 0.0

    # ---- construction ----
    @classmethod
    def build(cls,
              pools: Dict[str, List[dict]],
              edges: Sequence[dict],
              declared_schemas: Dict[str, Any],
              cache: Optional[ValueCache] = None) -> "MultipartiteCandidateGraph":
        """Build the graph from per-table candidate pools and the schema's edges.

        pools             logical table -> its candidates, best-scoring first
        edges             the relational schema's join_edges
        declared_schemas  logical table -> the columns its schema declares
        """
        cache = cache or ValueCache()
        parts = list(pools)
        g = cls(parts=parts)

        for part in parts:
            schema = declared_schemas.get(part) or {}
            g.nodes[part] = [
                CandidateNode(part=part, index=i, candidate=c,
                              weight=node_weight(c, schema))
                for i, c in enumerate(pools[part])
            ]

        # Group the schema's edges by the table pair they connect. An edge whose
        # table has no pool cannot be satisfied by any selection, so its penalty
        # is constant and goes to `const`.
        by_pair: Dict[Tuple[str, str], List[dict]] = {}
        present = set(parts)
        for e in edges or []:
            lt, rt = e["left_table"], e["right_table"]
            if lt not in present or rt not in present:
                g.const += P_MISSING_TABLE
                continue
            # Orient the pair by the part order, and the edge with it, so the
            # weight matrix is indexed consistently.
            if parts.index(lt) <= parts.index(rt):
                by_pair.setdefault((lt, rt), []).append(e)
            else:
                by_pair.setdefault((rt, lt), []).append(
                    {"left_table": rt, "left_on": e["right_on"],
                     "right_table": lt, "right_on": e["left_on"]})

        for (a, b), es in by_pair.items():
            g.pair_w[(a, b)] = [
                [edge_weight(u.candidate, v.candidate, es, cache)
                 for v in g.nodes[b]]
                for u in g.nodes[a]
            ]
        return g

    # ---- queries ----
    def weight_between(self, u: CandidateNode, v: CandidateNode) -> float:
        """Edge weight between two nodes of different parts; 0 when the schema
        declares no join between their tables."""
        if u.part == v.part:
            return 0.0
        key = (u.part, v.part)
        if key in self.pair_w:
            return self.pair_w[key][u.index][v.index]
        key = (v.part, u.part)
        if key in self.pair_w:
            return self.pair_w[key][v.index][u.index]
        return 0.0

    def score(self, clique: Sequence[CandidateNode]) -> float:
        """Total weight of a clique: its node weights, its edge weights, and the
        constant. Identical to the original `_combination_score`."""
        total = self.const + sum(n.weight for n in clique)
        for i, u in enumerate(clique):
            for v in clique[i + 1:]:
                total += self.weight_between(u, v)
        return total

    def stats(self) -> dict:
        n_nodes = sum(len(v) for v in self.nodes.values())
        n_pairs = sum(len(m) * len(m[0]) for m in self.pair_w.values() if m and m[0])
        combos = 1
        for p in self.parts:
            combos *= max(len(self.nodes[p]), 1)
        return {
            "parts": len(self.parts),
            "nodes": n_nodes,
            "pool_sizes": {p: len(self.nodes[p]) for p in self.parts},
            "joined_part_pairs": len(self.pair_w),
            "pair_evaluations": n_pairs,
            "cartesian_combinations": combos,
            "const": self.const,
        }


# --------------------------------------------------------------------------- #
# maximum-weight clique
# --------------------------------------------------------------------------- #
# PROVENANCE OF THE ALGORITHM
#
# There is no off-the-shelf solver for this exact problem, and it is worth being
# precise about why rather than pretending otherwise:
#
#   networkx.algorithms.clique.max_weight_clique implements the branch-and-bound
#   of Östergård, "A new algorithm for the maximum-weight clique problem"
#   (Discrete Applied Mathematics 120, 2002; the Cliquer solver), later refined
#   by San Segundo et al. It takes NODE weights only — the objective here also
#   has EDGE weights, which that formulation cannot express, so it cannot be
#   used directly.
#
#   In the general graph case one can push edge weights onto nodes by
#   subdividing edges, but that destroys the multipartite structure and blows up
#   the instance.
#
# With node and edge weights and one label per part, this problem is exactly MAP
# inference in a fully connected discrete pairwise Markov random field: parts are
# variables, nodes are labels, node weights are unary potentials, edge weights
# are pairwise potentials. The exact method used there is branch and bound with a
# decomposition bound, which is what is implemented below:
#
#   Östergård's B&B skeleton (extend a partial clique, prune on an optimistic
#   bound), with the bound computed by maximising each remaining term
#   independently — the standard MRF decomposition bound, admissible because
#   independently maximising each term can only overestimate their joint
#   maximum.
#
# The instances here are small (a handful of parts, <= 6 candidates each), so the
# search is exact and finishes immediately; the bound exists to skip the bulk of
# a Cartesian product that grows exponentially in the number of tables.
#
# TIE-BREAKING is part of the contract. The original scored `itertools.product`
# in order and kept a new combination only on a strict `>`, so among equally
# scoring selections the FIRST in product order won — that is, the
# lexicographically smallest tuple of candidate indices, with pools ordered
# best-scoring first. Both solvers below reproduce that exactly: parts are
# visited in schema order, candidates in rank order, and improvements require a
# strict `>`.


def _pair_max(graph: MultipartiteCandidateGraph) -> Dict[Tuple[str, str], float]:
    """Largest edge weight for each joined part pair, for the bound."""
    return {k: max(max(row) for row in m) if m and m[0] else 0.0
            for k, m in graph.pair_w.items()}


def max_weight_clique(graph: MultipartiteCandidateGraph,
                      method: str = "branch_and_bound"
                      ) -> Tuple[List[CandidateNode], float, dict]:
    """Highest-weight clique: exactly one candidate per logical table.

    method="branch_and_bound"  exact, with the decomposition bound above
    method="exhaustive"        exact, scoring every transversal — the original
                               algorithm, kept as the reference implementation

    Returns (clique, score, stats). Both methods return the same clique.
    """
    if method == "exhaustive":
        return _exhaustive(graph)
    if method != "branch_and_bound":
        raise ValueError(f"unknown method {method!r}")
    return _branch_and_bound(graph)


def _exhaustive(graph: MultipartiteCandidateGraph
                ) -> Tuple[List[CandidateNode], float, dict]:
    """Score every transversal. O(prod |pool|); the original behaviour."""
    parts = graph.parts
    if not parts:
        return [], graph.const, {"method": "exhaustive", "evaluated": 0}
    best, best_score, seen = None, None, 0
    for combo in product(*(graph.nodes[p] for p in parts)):
        seen += 1
        s = graph.score(combo)
        if best_score is None or s > best_score:   # strict: first wins ties
            best_score, best = s, list(combo)
    return best or [], float(best_score or graph.const), {
        "method": "exhaustive", "evaluated": seen}


def _branch_and_bound(graph: MultipartiteCandidateGraph
                      ) -> Tuple[List[CandidateNode], float, dict]:
    """Depth-first over parts, pruning on the decomposition bound."""
    parts = graph.parts
    if not parts:
        return [], graph.const, {"method": "branch_and_bound", "visited": 0,
                                 "pruned": 0}

    pair_max = _pair_max(graph)

    def pmax(i: int, j: int) -> float:
        a, b = parts[i], parts[j]
        return pair_max.get((a, b), pair_max.get((b, a), 0.0))

    # Optimistic score still available once parts 0..d-1 are fixed. Every term
    # not already accounted for by the running score is maximised on its own:
    #
    #   - the node weight of each remaining part
    #   - every pair (i, j), i < j, with j >= d
    #
    # The pair set must include the PREFIX-to-remaining pairs (i < d <= j), not
    # only the remaining-to-remaining ones. Omitting them makes the bound smaller
    # than the true best completion, which prunes branches that contain the
    # optimum — the bound stops being admissible and the search returns a
    # sub-optimal clique.
    #
    # Maximising each term independently can only overestimate their joint
    # maximum, so the bound never prunes a branch that could win.
    n = len(parts)
    suffix_bound = [0.0] * (n + 1)
    for d in range(n - 1, -1, -1):
        nodes = sum(max((x.weight for x in graph.nodes[parts[i]]), default=0.0)
                    for i in range(d, n))
        pairs = sum(pmax(i, j)
                    for j in range(d, n) for i in range(j))
        suffix_bound[d] = nodes + pairs

    best: List[CandidateNode] = []
    best_score = float("-inf")
    chosen: List[CandidateNode] = []
    stats = {"visited": 0, "pruned": 0}

    def descend(depth: int, running: float) -> None:
        nonlocal best, best_score
        if depth == len(parts):
            stats["visited"] += 1
            if running > best_score:           # strict: first in order wins ties
                best_score, best = running, list(chosen)
            return
        # Admissible bound: nothing below this node can beat it.
        if running + suffix_bound[depth] <= best_score:
            stats["pruned"] += 1
            return
        for node in graph.nodes[parts[depth]]:   # rank order, best first
            gain = node.weight + sum(graph.weight_between(u, node) for u in chosen)
            chosen.append(node)
            descend(depth + 1, running + gain)
            chosen.pop()

    descend(0, graph.const)
    stats["method"] = "branch_and_bound"
    return best, best_score, stats


def select_candidates(pools: Dict[str, List[dict]],
                      edges: Sequence[dict],
                      declared_schemas: Dict[str, Any],
                      cache: Optional[ValueCache] = None,
                      method: str = "branch_and_bound") -> Dict[str, dict]:
    """Build the graph and return {logical_table: chosen candidate}.

    Drop-in replacement for the original `_join_aware_select` body, once the
    per-table pools have been trimmed to `limit` distinct candidates.
    """
    graph = MultipartiteCandidateGraph.build(pools, edges, declared_schemas, cache)
    clique, _score, _stats = max_weight_clique(graph, method=method)
    return {n.part: n.candidate for n in clique}
