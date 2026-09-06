"""Candidate-solution generation and scoring (library; no entry point).

Imported by expand_compare.py. A "solution" is a small set of tables that
jointly covers every keyphrase of a question. Solutions are scored with the
connectivity objective:

    score(S) = sum_k max_{T in S} C_rel(k, T)  +  beta * conn_bin(S)

    conn_bin(S) = 1 - (#components(S) - 1) / (|S| - 1),  in [0, 1]

Components are counted over the full inferred join graph, so the term is
bounded (it cannot be inflated by dense clusters of near-duplicate tables) and
does not leak gold information (the whole graph is used, not a gold subgraph).

load_join_quality / make_eq are not part of the scoring path; they only supply
the bridge tiebreak used by expand_compare.
"""

from __future__ import annotations

import csv
import functools
import itertools
import json
import operator
from collections import defaultdict

# ---------- default method parameters ----------
DEFAULT_PARAMS = dict(
    top_k_seed    = 30,      # candidate tables read from the stage 2/3 ranking
    exclude_pruned= True,    # skip tables the stage 3 LLM marked as distractors
    cand          = 15,      # tables considered per keyphrase
    beta          = 3.0,     # weight on conn_bin
    dedup_jaccard = 0.60,    # solutions overlapping more than this are collapsed
    pre_m         = 1000,    # solutions kept after coverage prefiltering
    n_groups      = 20,      # solutions kept after scoring and dedup
    max_combos    = 200000,  # cap on the enumerated keyphrase-table product
)


def read_json(p):
    with open(p) as f: return json.load(f)

def norm(t):
    t = str(t).strip()
    return (t.split("#sep#")[-1] if "#sep#" in t else t).strip().upper()

def load_adj(path):
    """FULL binary join graph adjacency from dw_join_keys.json (no pruning)."""
    adj = defaultdict(set)
    for e in read_json(path):
        if len(e) != 2: continue
        a, b = norm(e[0].split(".")[0]), norm(e[1].split(".")[0])
        if a != b: adj[a].add(b); adj[b].add(a)
    return {k: set(v) for k, v in adj.items()}

def load_join_quality(csv_file):
    """edge quality = jaccard * unique_ratio (kept ONLY for bridge tiebreak)."""
    q = defaultdict(float)
    for r in csv.DictReader(open(csv_file)):
        a, b = norm(r["left_table"]), norm(r["right_table"])
        if a == b: continue
        def f(x):
            try: return float(r[x])
            except: return 0.0
        val = f("jaccard") * f("unique_ratio")
        k = frozenset((a, b))
        if val > q[k]: q[k] = val
    return q

def make_eq(q):
    def eq(a, b): return q.get(frozenset((a, b)), 0.0)
    return eq


# ============================================================
# ① candidates
# ============================================================
def build_candidates(rec, P):
    pool = rec["ranked_tables"][:P["top_k_seed"]]
    kp2t = defaultdict(dict)
    tcr  = defaultdict(float)
    for x in pool:
        if P["exclude_pruned"] and x.get("llm_pruned"):
            continue
        T = norm(x["table_id"])
        for ev in x.get("evidence", []):
            kp = ev.get("keyword")
            c = ev.get("column_similarity_rel") or 0.0
            if not kp: continue
            if c > kp2t[kp].get(T, 0): kp2t[kp][T] = c
            if c > tcr[T]: tcr[T] = c
    kps = [kp for kp in kp2t if kp2t[kp]]
    return kp2t, tcr, kps


# ============================================================
# generate solutions (coverage-prefiltered)
# ============================================================
def gen_solutions(kp2t, kps, P):
    cand = [sorted(kp2t[kp].items(), key=lambda x: -x[1])[:P["cand"]] for kp in kps]
    sz = functools.reduce(operator.mul, [len(l) for l in cand], 1) if cand else 0
    while sz > P["max_combos"] and max((len(l) for l in cand), default=0) > 2:
        cand = [l[:max(2, len(l) - 1)] for l in cand]
        sz = functools.reduce(operator.mul, [len(l) for l in cand], 1)
    cov_of = {}
    for combo in itertools.product(*cand):
        tabs = frozenset(T for T, _ in combo)
        cov = sum(c for _, c in combo)
        if tabs not in cov_of or cov > cov_of[tabs]:
            cov_of[tabs] = cov
    top = sorted(cov_of.items(), key=lambda x: -x[1])[:P["pre_m"]]
    return [set(t) for t, _ in top]


# ============================================================
# score (conn objective) + dedup + assemble
# ============================================================
def ncomp(S, adj):
    S = set(S); seen = set(); c = 0
    for x in S:
        if x in seen: continue
        c += 1; seen.add(x); st = [x]
        while st:
            u = st.pop()
            for v in adj.get(u, set()):
                if v in S and v not in seen: seen.add(v); st.append(v)
    return c

def score_group(group, kp2t, kps, adj, P):
    cov  = sum(max((kp2t[kp].get(T, 0) for T in group), default=0.0) for kp in kps)
    n    = len(group)
    conn = 1 - (ncomp(group, adj) - 1) / (n - 1) if n > 1 else 1.0
    return cov + P.get("beta", 3.0) * conn

def parallel_dedup(sorted_groups, thr):
    kept = []
    for g in sorted_groups:
        if any(len(g & k) / len(g | k) > thr for k in kept):
            continue
        kept.append(g)
    return kept

def select_groups(rec, P, adj):
    kp2t, tcr, kps = build_candidates(rec, P)
    if not kps:
        return [], tcr
    sols = gen_solutions(kp2t, kps, P)
    scored = sorted(sols, key=lambda g: -score_group(g, kp2t, kps, adj, P))
    deduped = parallel_dedup(scored, P["dedup_jaccard"])
    return deduped[:P["n_groups"]], tcr
