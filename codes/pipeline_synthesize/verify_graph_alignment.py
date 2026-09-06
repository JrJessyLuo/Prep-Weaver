"""Check that the graph formulation selects exactly what the original code did.

THE PROBLEM WITH COMPARING TWO LLM RUNS
---------------------------------------
Re-running the whole stage twice and comparing the outputs would measure the
LLM's nondeterminism, not the selection logic: the operator chains, and hence
the candidate pools, differ between runs. So this script does not re-run
anything. It takes candidate pools as FIXED INPUT and compares only the step
under test — which combination the two selectors pick from the same pools. The
LLM is out of the picture by construction.

WHAT IS COMPARED
----------------
    original   the shipped `_join_aware_select`: score every combination of
               `itertools.product`, keep the first strict maximum
    exhaustive the graph's own reference solver, same enumeration through the
               graph's decomposed weights
    b_and_b    the graph's branch-and-bound

Agreement is required to be EXACT, not approximate: the score decomposes into
per-table and per-pair terms with no remainder, and every transversal of a
complete multipartite graph is a clique, so the two searches optimise the same
function over the same feasible set. Any disagreement is a bug, not noise.

Run:
    python -m pipeline_synthesize.verify_graph_alignment            # synthetic
    python -m pipeline_synthesize.verify_graph_alignment --trials 500
"""

from __future__ import annotations

import argparse
import random
import time
from itertools import product
from typing import Any, Dict, List, Sequence

import pandas as pd

from .candidate_graph import (
    MultipartiteCandidateGraph,
    ValueCache,
    default_col_values,
    key_quality,
    max_weight_clique,
    _cf,
)


# --------------------------------------------------------------------------- #
# the ORIGINAL objective and search, transcribed verbatim
# --------------------------------------------------------------------------- #
# Copied from actions/pipeline_synthesize.py so the comparison is against the
# real thing rather than a paraphrase of it. Only `col_values` is swapped for
# the local equivalent, so this file runs without the search engine installed.

def original_combination_score(selected: Dict[str, dict],
                               edges: Sequence[dict],
                               plan_tables: Dict[str, dict],
                               cache) -> float:
    score = 0.0
    for lt, payload in selected.items():
        df = payload["df"]
        required = {_cf(c) for c in (plan_tables.get(lt, {}).get("schema") or {})}
        present = {_cf(c) for c in df.columns}
        cover = len(required & present) / max(len(required), 1)
        score += 2.0 * cover + 0.25 * float(payload.get("score") or 0.0)
    for e in edges:
        lt, rt = e["left_table"], e["right_table"]
        if lt not in selected or rt not in selected:
            score -= 2.0
            continue
        ldf, rdf = selected[lt]["df"], selected[rt]["df"]
        lv, rv = cache.values(ldf, e["left_on"]), cache.values(rdf, e["right_on"])
        if lv is None or rv is None:
            score -= 1.0
            continue
        if not lv or not rv:
            continue
        inter = len(lv & rv)
        score += 2.0 * max(inter / max(min(len(lv), len(rv)), 1),
                           inter / max(len(lv), 1),
                           inter / max(len(rv), 1))
        score += 0.25 * cache.key_quality(ldf, e["left_on"])
        score += 0.25 * cache.key_quality(rdf, e["right_on"])
    return score


def original_select(pools: Dict[str, List[dict]], edges, plan_tables):
    """The shipped exhaustive product search."""
    names = list(pools)
    best, best_score, seen = None, None, 0
    cache = ValueCache()
    for combo in product(*(pools[n] for n in names)):
        seen += 1
        selected = dict(zip(names, combo))
        s = original_combination_score(selected, edges, plan_tables, cache)
        if best_score is None or s > best_score:
            best_score, best = s, selected
    return best or {}, float(best_score or 0.0), seen


# --------------------------------------------------------------------------- #
# synthetic instances
# --------------------------------------------------------------------------- #

def random_instance(rng: random.Random, n_tables: int, pool: int, rows: int = 40):
    """A random task: pools of candidate frames plus a declared schema.

    Frames deliberately share values so join overlaps land strictly between 0
    and 1, and some candidates deliberately DROP a declared join column so the
    -1.0 missing-column branch is exercised.
    """
    parts = [f"table_{i+1}" for i in range(n_tables)]
    key_pool = [f"k{n}" for n in range(rows)]

    plan_tables, pools = {}, {}
    for p in parts:
        n_cols = rng.randint(2, 5)
        schema = {f"c{j}": "TEXT" for j in range(n_cols)}
        schema["jk"] = "TEXT"                       # the join column
        plan_tables[p] = {"schema": schema}
        cands = []
        for _ in range(pool):
            keep = [c for c in schema if rng.random() > 0.3]
            data = {}
            for c in keep:
                if c == "jk":
                    k = rng.randint(3, rows)
                    data[c] = rng.sample(key_pool, k) + [None] * (rows - k)
                else:
                    data[c] = [f"{c}_{i}" for i in range(rows)]
            if not data:
                data = {"unrelated": list(range(rows))}
            cands.append({"df": pd.DataFrame(data),
                          "score": round(rng.uniform(0, 1), 3),
                          "chain": [f"op{rng.randint(0,3)}"]})
        # pools arrive best-scoring first, as the search produces them
        cands.sort(key=lambda c: -c["score"])
        pools[p] = cands

    edges = []
    for i in range(n_tables - 1):
        edges.append({"left_table": parts[i], "left_on": "jk",
                      "right_table": parts[i + 1], "right_on": "jk"})
    # sometimes reference a table that has no pool, to exercise the constant
    if rng.random() < 0.25:
        edges.append({"left_table": parts[0], "left_on": "jk",
                      "right_table": "table_absent", "right_on": "jk"})
    return pools, edges, plan_tables


def declared_schemas_of(plan_tables: Dict[str, dict]) -> Dict[str, Any]:
    return {lt: (v.get("schema") or {}) for lt, v in plan_tables.items()}


def compare_once(pools, edges, plan_tables) -> dict:
    """Run all three selectors on one instance and compare."""
    orig_sel, orig_score, orig_evals = original_select(pools, edges, plan_tables)

    graph = MultipartiteCandidateGraph.build(pools, edges,
                                             declared_schemas_of(plan_tables))
    ex_clique, ex_score, _ = max_weight_clique(graph, method="exhaustive")
    bb_clique, bb_score, bb_stats = max_weight_clique(graph, method="branch_and_bound")

    def ids(sel: Dict[str, dict]) -> Dict[str, int]:
        # Identity, not equality: a candidate holds a DataFrame, and comparing
        # two of those with == returns a frame, not a bool.
        out = {}
        for part, chosen in sel.items():
            out[part] = next(i for i, c in enumerate(pools[part]) if c is chosen)
        return out

    orig_ids = ids(orig_sel)
    ex_ids = {n.part: n.index for n in ex_clique}
    bb_ids = {n.part: n.index for n in bb_clique}

    return {
        "score_match_exhaustive": abs(orig_score - ex_score) < 1e-9,
        "score_match_bb": abs(orig_score - bb_score) < 1e-9,
        "pick_match_exhaustive": orig_ids == ex_ids,
        "pick_match_bb": orig_ids == bb_ids,
        "orig_score": orig_score, "bb_score": bb_score,
        "orig_ids": orig_ids, "bb_ids": bb_ids,
        "orig_evaluations": orig_evals,
        "bb_visited": bb_stats["visited"], "bb_pruned": bb_stats["pruned"],
        "stats": graph.stats(),
    }


def main():
    ap = argparse.ArgumentParser(
        description="Verify the graph selector reproduces the original selection.")
    ap.add_argument("--trials", type=int, default=200)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--max-tables", type=int, default=5)
    ap.add_argument("--pool", type=int, default=6,
                    help="Candidates per table (the shipped limit is 6).")
    a = ap.parse_args()

    rng = random.Random(a.seed)
    bad, tot_orig, tot_visited = [], 0, 0
    t_orig = t_bb = 0.0

    for t in range(a.trials):
        n = rng.randint(2, a.max_tables)
        pools, edges, plan_tables = random_instance(rng, n, a.pool)

        t0 = time.perf_counter(); original_select(pools, edges, plan_tables)
        t_orig += time.perf_counter() - t0

        graph = MultipartiteCandidateGraph.build(pools, edges,
                                                 declared_schemas_of(plan_tables))
        t0 = time.perf_counter(); max_weight_clique(graph)
        t_bb += time.perf_counter() - t0

        r = compare_once(pools, edges, plan_tables)
        tot_orig += r["orig_evaluations"]; tot_visited += r["bb_visited"]
        if not all((r["score_match_exhaustive"], r["score_match_bb"],
                    r["pick_match_exhaustive"], r["pick_match_bb"])):
            bad.append((t, r))

    print(f"\n===== graph alignment: {a.trials} random instances "
          f"(<= {a.max_tables} tables, {a.pool} candidates each) =====")
    print(f"  identical selection AND score : {a.trials - len(bad)}/{a.trials}")
    print(f"  mismatches                    : {len(bad)}")
    for t, r in bad[:5]:
        print(f"\n  trial {t}: orig={r['orig_score']:.6f} bb={r['bb_score']:.6f}")
        print(f"    orig picks {r['orig_ids']}")
        print(f"    bb   picks {r['bb_ids']}")
    print(f"\n  combinations scored, original : {tot_orig:,}")
    print(f"  leaves visited, branch & bound : {tot_visited:,}")
    print(f"  time  original / graph B&B     : {t_orig:.2f}s / {t_bb:.2f}s")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
