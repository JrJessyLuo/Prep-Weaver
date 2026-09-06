"""Stages 4-5: bridge expansion + confidence voting -> the final table selection.

Input  (results/):  question_ranked_tables_gated.json   (stage 3)
                    dw_join_keys_g_domain.json          (stage 0)
                    edge_conf_g_domain.json             (stage 0)
       (profiles/): dev.json                            (gold labels, evaluation only)
Output (results/):  exp_g_domain_{5,10,15}.json         (the final selection)

Per question:

  1. Candidate solutions. group_select enumerates small table sets that cover
     every keyphrase, scores them with cov + beta * conn_bin over the join
     graph, deduplicates near-identical ones, and keeps the top N.
  2. Bridge expansion. A solution whose tables fall into several join
     components is reconnected with at most `max_hops` intermediate tables.
     Among equal-length bridge paths the one with the best minimum edge
     quality (profiling edge confidence) wins.
  3. Re-ranking. Expanded solutions are re-scored with the same objective, so
     a solution that became connected can overtake one that did not.
  4. Voting. Tables are ranked by how many of the top-N solutions contain them
     (consensus), optionally weighted by each solution's score.
  5. Budget backfill. If the top-N solutions contain fewer than k distinct
     tables, the selection is padded from the stage 3 ranking, so every method
     spends the same top-k budget in an @k comparison.

Gold tables are read only to print full-cover@k; they never influence the
selection.

Run:
    python -m table_discovery.expand_compare --dataset Beaver-Prep
"""

from __future__ import annotations

import argparse
import heapq
import itertools
import json
import os
from collections import defaultdict

from . import group_select as GS
from common import paths as P

norm = GS.norm

# ---------------- method settings (overridable from the CLI) ----------------
N_KEEP = 20        # candidate solutions carried forward per question
MAX_HOPS = 2       # bridge path length: 1 hop preferred, 2 at most
RERANK = True      # re-rank solutions after expansion
PAD_TO_K = True    # backfill each selection to k from the stage 3 ranking

# Aggregation across the top-N solutions:
#   "vote"  confidence-weighted voting; promotes tables recurring across many
#           high-scoring solutions, so the few gold tables of a low-|gold|
#           question land together in a small top-k
#   "union" rank-priority concatenation (each solution emitted whole, in order)
AGG_MODE = "vote"
VOTE_W_COUNT = 1.0    # weight on the normalized vote count (consensus)
VOTE_W_WEIGHT = 0.0   # weight on the normalized average vote weight (score)

EVAL_KS = (5, 10, 15)
SAVE_KS = (5, 10, 15)

def load_adj(path):
    return GS.load_adj(path)

def components(group, adj):
    g = set(group); seen = set(); out = []
    for s in g:
        if s in seen: continue
        c = {s}; seen.add(s); st = [s]
        while st:
            u = st.pop()
            for v in adj.get(u, set()):
                if v in g and v not in seen: seen.add(v); c.add(v); st.append(v)
        out.append(c)
    return out

def best_path(srcs, targets, adj, eq, block, max_hops):
    """from srcs to targets through non-`block` intermediates (<=max_hops);
    cost=(hops,-min_edge_quality). returns list of intermediates or None."""
    targets = set(targets); pq = [(0, -1.0, s, ()) for s in srcs]; heapq.heapify(pq)
    best = {}
    while pq:
        hops, negq, u, inter = heapq.heappop(pq)
        if u in best and best[u] <= (hops, negq): continue
        best[u] = (hops, negq); minq = -negq
        for v in adj.get(u, set()):
            w = eq(u, v); nminq = min(minq, w) if w > 0 else minq
            if v in targets:
                return list(inter)
            if v in block or v in srcs: continue
            if hops + 1 > max_hops: continue
            heapq.heappush(pq, (hops + 1, -nminq, v, inter + (v,)))
    return None

def expand(group, adj, eq, max_hops):
    """reconnect the solution's join components with <=max_hops bridge tables."""
    g = set(group); comps = components(g, adj)
    if len(comps) < 2: return set()
    comps = [set(c) for c in comps]; added = set()
    while len(comps) > 1:
        bestmove = None
        for i, j in itertools.combinations(range(len(comps)), 2):
            inter = best_path(comps[i] | added, comps[j] | added, adj, eq, g, max_hops)
            if inter is None: continue
            key = (len(inter),)
            if bestmove is None or key < bestmove[0]: bestmove = (key, i, j, inter)
        if bestmove is None: break
        _, i, j, inter = bestmove
        added |= set(inter)
        merged = comps[i] | comps[j] | set(inter)
        comps = [c for k, c in enumerate(comps) if k not in (i, j)] + [merged]
    return added

# ---------------- top-N candidate solutions (conn objective) ----------------
def top_solutions(rec, params, adj, n_keep):
    kp2t, tcr, kps = GS.build_candidates(rec, params)
    if not kps: return [], tcr, kp2t, kps
    sols = GS.gen_solutions(kp2t, kps, params)
    scored = sorted(sols, key=lambda g: -GS.score_group(g, kp2t, kps, adj, params))
    deduped = GS.parallel_dedup(scored, params["dedup_jaccard"])[:n_keep]
    return deduped, tcr, kp2t, kps

def pad_to_k(order, pad_rank, K):
    """Backfill `order` to K from pad_rank (first-stage ranking), order-preserving.
    When PAD_TO_K is False (or pad_rank empty) this is just a truncation to K."""
    if not PAD_TO_K:
        return list(order)[:K]
    out, seen = list(order), set(order)
    for t in (pad_rank or []):
        if len(out) >= K:
            break
        if t not in seen:
            seen.add(t); out.append(t)
    return out[:K]

# ---------------- build base/expand selections for a given join graph ----------------
def build_base_exp(rec, params, adj, eq):
    sols, tcr, kp2t, kps = top_solutions(rec, params, adj, N_KEEP)
    base = [(set(g), {t: (1, tcr.get(t, 0.0)) for t in g}) for g in sols]
    exp = []
    for g in sols:
        g = set(g); added = expand(g, adj, eq, MAX_HOPS)
        full = g | added
        sc = GS.score_group(full, kp2t, kps, adj, params)
        ordv = {t: (1, tcr.get(t, 0.0)) for t in g}
        for t in added: ordv[t] = (0, 1.0)
        exp.append((sc, full, ordv))
    if RERANK:
        exp.sort(key=lambda x: -x[0])
    pairs  = [(full, ordv) for _, full, ordv in exp]
    scores = [sc for sc, _, _ in exp]
    return base, pairs, scores, tcr


def aggregate_by_vote(exp, scores, tcr):
    """ARM-style confidence-weighted voting over the top-N solutions (each = a voter).
      vote_count(t)  = #solutions containing t           (consensus)
      vote_weight(t) = mean conn-score of solutions containing t  (CoRE-T coherence)
      confidence(t)  = w_count*norm(count) + w_weight*norm(avg_weight)
    Returns the FULL table ranking (high->low confidence); truncation/pad happens later."""
    vc = defaultdict(float); wsum = defaultdict(float); wn = defaultdict(float)
    for (full, _), sc in zip(exp, scores):
        for t in full:
            vc[t] += 1.0; wsum[t] += sc; wn[t] += 1.0
    if not vc:
        return []
    vwavg = {t: wsum[t] / wn[t] for t in vc}

    def nz(m):
        mx = max(m.values()) if m else 0.0
        return {k: (v / mx if mx > 0 else 0.0) for k, v in m.items()}

    nvc, nvw = nz(vc), nz(vwavg)
    conf = {t: VOTE_W_COUNT * nvc[t] + VOTE_W_WEIGHT * nvw[t] for t in vc}
    return sorted(conf, key=lambda t: (-conf[t], -tcr.get(t, 0.0)))


def rank_tables(exp, scores, tcr):
    """Full table ranking under the active AGG_MODE (truncation/pad applied by caller)."""
    if AGG_MODE == "vote":
        return aggregate_by_vote(exp, scores, tcr)
    # union: rank-priority concatenation of whole solutions (legacy behaviour)
    order, seen = [], set()
    for full, ordv in exp:
        for t in sorted(full, key=lambda x: ordv.get(x, (1, 0.0)), reverse=True):
            if t not in seen:
                seen.add(t); order.append(t)
    return order

# ---------------- per-graph bridge-tiebreak eq sources ----------------
def conf_eq(conf_path):
    """bridge tiebreak from profiling edge confidence {'TA|TB': score}."""
    with open(conf_path) as f:
        conf = json.load(f)
    def eq(a, b):
        a, b = a.upper(), b.upper()
        k = f"{a}|{b}" if a < b else f"{b}|{a}"
        return conf.get(k, 0.0)
    return eq


def make_zero_eq():
    """Fallback bridge tiebreak: all legal edges get equal quality."""
    def eq(a, b):
        return 0.0
    return eq




# ============================================================
# Entry point
# ============================================================

def select_tables(paths: "P.Paths", params=None, graph_name: str = "g_domain"):
    """Run stages 4-5 and write exp_<graph>_{k}.json for every k in SAVE_KS.

    Prints gold full-cover@k as a sanity check. Gold labels come from dev.json
    and are used for reporting only.
    """
    params = params or dict(GS.DEFAULT_PARAMS)

    gated_path = paths.out("question_ranked_tables_gated.json")
    graph_path = paths.out(f"dw_join_keys_{graph_name}.json")
    conf_path = paths.out(f"edge_conf_{graph_name}.json")

    for p in (gated_path, graph_path):
        if not os.path.exists(p):
            raise FileNotFoundError(f"Missing required input: {p}")

    adj = load_adj(str(graph_path))
    eq = conf_eq(str(conf_path)) if os.path.exists(conf_path) else make_zero_eq()
    if not os.path.exists(conf_path):
        print(f"[WARN] edge confidence not found, bridge tiebreak disabled: {conf_path}")

    gated = GS.read_json(str(gated_path))
    dev = GS.read_json(str(paths.dev))

    # Gold references, for reporting only.
    #   gold: the tables of the gold SQL
    #   map : the tables the question's keyphrase->column mapping points at
    gold_by_q, map_by_q = {}, {}
    for it in dev:
        gold_by_q[it["question"]] = {norm(t) for t in it.get("gold_tables", [])}
        s = set()
        for _kp, cols in (it.get("mapping") or {}).items():
            for c in cols:
                s.add(norm(c.split(".")[0]))
        map_by_q[it["question"]] = s

    method = f"exp_{graph_name}"
    saved = {k: {} for k in SAVE_KS}
    acc = {me: {k: [0, 0] for k in EVAL_KS} for me in ("map", "gold")}

    for rec in gated.values():
        q = rec["question"]
        first_rank = [norm(x["table_id"]) for x in rec["ranked_tables"]]

        _base, exp, scores, tcr = build_base_exp(rec, params, adj, eq)
        ordered_full = rank_tables(exp, scores, tcr)

        ordered = pad_to_k(ordered_full, first_rank, max(SAVE_KS))
        for k in SAVE_KS:
            saved[k][q] = ordered[:k]

        if q not in gold_by_q:      # question absent from dev.json: nothing to score
            continue
        refs = {"gold": gold_by_q[q], "map": map_by_q.get(q, set())}
        for k in EVAL_KS:
            sel = set(pad_to_k(ordered_full, first_rank, k))
            for me in refs:
                acc[me][k][1] += 1
                acc[me][k][0] += int(refs[me].issubset(sel))

    n = acc["gold"][EVAL_KS[0]][1]
    print(
        f"\n===== {method} (n={n} scored)  n_keep={N_KEEP} hops={MAX_HOPS} "
        f"rerank={RERANK} pad_to_k={PAD_TO_K} agg={AGG_MODE} beta={params['beta']} ====="
    )
    for me, title in (("map", "mapping full-cover"), ("gold", "gold full-cover")):
        cells = " ".join(
            f"@{k}={acc[me][k][0] / acc[me][k][1]:.3f}" if acc[me][k][1] else f"@{k}=n/a"
            for k in EVAL_KS
        )
        print(f"  {title:<22} {cells}")

    for k, qmap in saved.items():
        out_path = paths.out(f"{method}_{k}.json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(qmap, f, ensure_ascii=False, indent=1)
        print(f"saved {len(qmap)} questions -> {out_path}")

    return saved


def parse_args():
    parser = argparse.ArgumentParser(
        description="Stages 4-5: bridge expansion + voting -> final table selection.")
    P.add_arguments(parser)
    parser.add_argument("--graph-name", type=str, default="g_domain",
                        help="Join graph to use, i.e. the suffix of "
                             "dw_join_keys_<graph>.json written by stage 0.")

    # Candidate-solution parameters (see group_select.DEFAULT_PARAMS).
    parser.add_argument("--top-k-seed", type=int, default=GS.DEFAULT_PARAMS["top_k_seed"])
    parser.add_argument("--cand", type=int, default=GS.DEFAULT_PARAMS["cand"])
    parser.add_argument("--beta", type=float, default=GS.DEFAULT_PARAMS["beta"])
    parser.add_argument("--dedup-jaccard", type=float, default=GS.DEFAULT_PARAMS["dedup_jaccard"])
    parser.add_argument("--pre-m", type=int, default=GS.DEFAULT_PARAMS["pre_m"])
    parser.add_argument("--n-groups", type=int, default=GS.DEFAULT_PARAMS["n_groups"])
    parser.add_argument("--max-combos", type=int, default=GS.DEFAULT_PARAMS["max_combos"])
    parser.add_argument("--include-pruned", action="store_true",
                        help="Keep the tables stage 3 marked as distractors.")

    # Expansion / aggregation parameters.
    parser.add_argument("--n-keep", type=int, default=N_KEEP)
    parser.add_argument("--max-hops", type=int, default=MAX_HOPS)
    parser.add_argument("--no-rerank", action="store_true")
    parser.add_argument("--no-pad-to-k", action="store_true")
    parser.add_argument("--agg-mode", choices=["vote", "union"], default=AGG_MODE)
    parser.add_argument("--vote-w-count", type=float, default=VOTE_W_COUNT)
    parser.add_argument("--vote-w-weight", type=float, default=VOTE_W_WEIGHT)
    parser.add_argument("--eval-ks", type=int, nargs="+", default=list(EVAL_KS))
    parser.add_argument("--save-ks", type=int, nargs="+", default=list(SAVE_KS))
    return parser.parse_args()


def params_from_args(a) -> dict:
    params = dict(GS.DEFAULT_PARAMS)
    params.update({
        "top_k_seed": a.top_k_seed,
        "exclude_pruned": not a.include_pruned,
        "cand": a.cand,
        "beta": a.beta,
        "dedup_jaccard": a.dedup_jaccard,
        "pre_m": a.pre_m,
        "n_groups": a.n_groups,
        "max_combos": a.max_combos,
    })
    return params


if __name__ == "__main__":
    a = parse_args()

    N_KEEP = a.n_keep
    MAX_HOPS = a.max_hops
    RERANK = not a.no_rerank
    PAD_TO_K = not a.no_pad_to_k
    AGG_MODE = a.agg_mode
    VOTE_W_COUNT = a.vote_w_count
    VOTE_W_WEIGHT = a.vote_w_weight
    EVAL_KS = tuple(a.eval_ks)
    SAVE_KS = tuple(a.save_ks)

    params = params_from_args(a)
    print("params:", params)
    select_tables(P.from_args(a), params=params, graph_name=a.graph_name)
