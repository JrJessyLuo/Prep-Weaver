"""Stage 0 (offline): build the profiling-based join graph.

Input  (profiles/): dev_tables.json, dev_semantic_col_sim.json,
                    dev_uniqueness.json, dev_jaccard.json
Output (results/):  dw_join_keys_g_domain.json, edge_conf_g_domain.json

No ground-truth join key is used anywhere in this file.

The graph is built in three steps:

  1. Column-pair signals. Two variants are derived from the same profiling
     files: a strict "base" variant (containment + embedding + distinct-ratio
     thresholds) and a "refined" variant that additionally accepts a string
     column-name match and, when the names match, relaxes the containment
     floor. The refined variant trades edge precision for connectivity.
  2. Domain partition. The base column pairs are lifted to a weighted table
     graph and clustered hierarchically into domains; strongly connected
     domains are merged.
  3. Two-level graph. Intra-domain edges come from the strict base variant;
     cross-domain edges come from the refined variant and must additionally
     pass an OR-gate that requires several independent table-pair links
     between the two domains.

Only the domain-gated graph (g_domain) is produced: it is the graph the rest
of the pipeline consumes.

Run:
    python -m table_discovery.build_join_graph --dataset Beaver-Prep
"""
from __future__ import annotations

import argparse
import json
import logging
import math
from collections import defaultdict
from dataclasses import dataclass, field
from itertools import combinations
from typing import Any, Dict, List, Optional, Set, Tuple

import networkx as nx
import numpy as np
from scipy.cluster.hierarchy import fcluster, linkage
from scipy.spatial.distance import squareform

from common import paths as P

logger = logging.getLogger(__name__)


@dataclass
class Column:
    table: str
    name: str
    distinct_ratio: float


# ─────────────────────────────────────────────
# Load raw profiling files
# ─────────────────────────────────────────────
def load_data(tables_fpath: str, meta_sim_fpath: str,
              uniqueness_fpath: str, jaccard_fpath: str):
    with open(tables_fpath) as f:        tables_content = json.load(f)
    with open(meta_sim_fpath) as f:      meta_sim_dict = json.load(f)
    with open(uniqueness_fpath) as f:    uniqueness_dict = json.load(f)
    with open(jaccard_fpath) as f:       jaccard_dict = json.load(f)
    return tables_content, meta_sim_dict, uniqueness_dict, jaccard_dict


# ─────────────────────────────────────────────
# Column-ref / colpair-key normalization
# ─────────────────────────────────────────────
def normalize_col_key(x: str) -> str:
    x = str(x)
    if "#sep#" in x:
        parts = x.split("#sep#")
        if len(parts) >= 2:
            return f"{parts[-2]}-{parts[-1]}"
    if "." in x:
        table, col = x.split(".", 1)
        return f"{table}-{col}"
    return x


def normalize_col_ref(x: str):
    """table#sep#col | db#sep#table#sep#col | table-col | table.col  ->  'table-col'."""
    x = str(x).strip()
    if "#sep#" in x:
        parts = x.split("#sep#")
        if len(parts) >= 2:
            return f"{parts[-2]}-{parts[-1]}"
    if "." in x:
        table, col = x.split(".", 1)
        return f"{table}-{col}"
    if "-" in x:
        return x
    return None


def parse_combined_colpair_key(key: str):
    """'table1#sep#col1-table2#sep#col2' (or db-prefixed) -> ('table1-col1','table2-col2')."""
    key = str(key)
    if "-" not in key:
        return None, None
    parts = key.split("-")
    for i in range(1, len(parts)):
        left = normalize_col_ref("-".join(parts[:i]))
        right = normalize_col_ref("-".join(parts[i:]))
        if left is not None and right is not None:
            return left, right
    return None, None


def collect_pair_scores_for_db(nested_dict, db_id: str = ""):
    """
    Direction-agnostic pair scores: frozenset({table-col, table-col}) -> max score.
    Handles both:
      Format A: {"t1-t2": {"t1#sep#c1-t2#sep#c2": score}}
      Format B: {"t1#sep#c1": {"t2#sep#c2": score}}
    """
    pair_to_score = {}
    for outer_key, inner_map in nested_dict.items():
        if not isinstance(inner_map, dict):
            continue
        outer_col = normalize_col_ref(outer_key)
        for inner_key, score in inner_map.items():
            l, r = parse_combined_colpair_key(inner_key)        # Case 1: combined key
            if l is not None and r is not None:
                c1, c2 = l, r
            else:                                               # Case 2: outer/inner each a column
                inner_col = normalize_col_ref(inner_key)
                if outer_col is None or inner_col is None:
                    continue
                c1, c2 = outer_col, inner_col
            if c1 is None or c2 is None or c1 == c2:
                continue
            try:
                s = float(score) if score is not None else 0.0
            except Exception:
                s = 0.0
            pair = frozenset({c1, c2})
            if len(pair) != 2:
                continue
            pair_to_score[pair] = max(pair_to_score.get(pair, 0.0), s)
    return pair_to_score


# ─────────────────────────────────────────────
# Build columns + colpair similarity for one db_id ("" = all tables)
# ─────────────────────────────────────────────
def build_inputs_for_db(
    db_id: str,
    meta_sim_dict: dict,
    jaccard_sim_dict: dict,
    uniqueness_dict: dict,
    default_distinct_ratio: float = 0.5,
    containment_threshold: float = 0.98,
    default_sim: float = 0.5,
    use_sim_pruning: bool = False,
    sim_threshold: float = 0.7,
    use_distinct_ratio_pruning: bool = False,
    distinct_ratio_threshold: float = 0.9,
) -> Tuple[List[Column], dict]:
    dbtab_uniqueness = {k: v for k, v in uniqueness_dict.items() if k.startswith(db_id)}

    columns: List[Column] = []
    seen = set()
    col_to_distinct_ratio = {}

    for key, distinct_ratio in dbtab_uniqueness.items():
        arrs = key.split("#sep#")
        if len(arrs) >= 3:        # db#sep#table#sep#column
            tab_name, col_name = arrs[-2], arrs[-1]
        elif len(arrs) == 2:      # table#sep#column
            tab_name, col_name = arrs[0], arrs[1]
        else:
            continue

        dr = distinct_ratio if distinct_ratio is not None else default_distinct_ratio
        dr = max(0.0, min(1.0, float(dr)))

        col_id = normalize_col_key(f"{tab_name}-{col_name}")
        col_to_distinct_ratio[col_id] = dr

        if (tab_name, col_name) in seen:
            continue
        seen.add((tab_name, col_name))
        columns.append(Column(table=tab_name, name=col_name, distinct_ratio=dr))

    meta_pair_scores  = collect_pair_scores_for_db(meta_sim_dict, db_id)
    containment_scores = collect_pair_scores_for_db(jaccard_sim_dict, db_id)

    colpair_col_sim = {}
    skipped_by_containment = skipped_by_sim = skipped_by_distinct_ratio = missing_meta = 0

    for pair, contain_score in containment_scores.items():
        if contain_score < containment_threshold:
            skipped_by_containment += 1
            continue
        pair_list = list(pair)
        if len(pair_list) != 2:
            continue
        c1, c2 = pair_list[0], pair_list[1]

        sim = meta_pair_scores.get(pair, None)
        if sim is None:
            missing_meta += 1
            sim = default_sim
        sim = max(0.0, min(1.0, float(sim)))

        if use_sim_pruning and sim < sim_threshold:
            skipped_by_sim += 1
            continue

        if use_distinct_ratio_pruning:
            dr1 = col_to_distinct_ratio.get(c1, default_distinct_ratio)
            dr2 = col_to_distinct_ratio.get(c2, default_distinct_ratio)
            if max(dr1, dr2) < distinct_ratio_threshold:        # at least one side key-like
                skipped_by_distinct_ratio += 1
                continue

        colpair_col_sim[(c1, c2)] = sim
        colpair_col_sim[(c2, c1)] = sim

    print(
        f"[{db_id or 'ALL'}] colpair_col_sim: {len(colpair_col_sim)//2} undirected pairs | "
        f"cont>={containment_threshold} sim_prune={use_sim_pruning}"
        f"({sim_threshold if use_sim_pruning else '-'}) "
        f"dr_prune={use_distinct_ratio_pruning}({distinct_ratio_threshold if use_distinct_ratio_pruning else '-'}) | "
        f"skip_cont={skipped_by_containment} skip_sim={skipped_by_sim} "
        f"skip_dr={skipped_by_distinct_ratio} miss_meta={missing_meta}"
    )
    return columns, colpair_col_sim


# ─────────────────────────────────────────────
# REFINED col-pair signals: string column-name signal + name-aware containment relax
# (shared by g_nodomain and g_domain).  Returns columns, pairs(c1,c2)->name_used,
# fkfk_only(name/value-anchored bridges for the OR-gate), and containment lookup.
# ─────────────────────────────────────────────
_STOPTOK = {"ID", "CODE", "NUM", "SORT"}     # too-generic single tokens


def _col_part(cid: str) -> str:
    return cid.split("-", 1)[1] if "-" in cid else cid


def name_string_sim(c1: str, c2: str) -> float:
    """1.0 exact column name | 0.8 token-subset(>=2 tokens, non-generic) | 0."""
    a, b = _col_part(c1), _col_part(c2)
    if a == b:
        return 1.0
    ta, tb = set(a.split("_")), set(b.split("_"))
    small, large = (ta, tb) if len(ta) <= len(tb) else (tb, ta)
    if small <= large and len(small) >= 2 and (small - _STOPTOK):
        return 0.8
    return 0.0


def build_refined_colpairs(
    meta_sim_dict: dict, jaccard_sim_dict: dict, uniqueness_dict: dict,
    base_containment: float = 0.8, name_containment: float = 0.3,
    name_used_floor: float = 0.6, dr_floor: float = 0.9,
    fkfk_containment: float = 0.95, fkfk_embedding: float = 0.85,
) -> Tuple[List[Column], Dict[Tuple[str, str], float], Dict[Tuple[str, str], float], Dict[frozenset, float]]:
    cont = collect_pair_scores_for_db(jaccard_sim_dict, "")
    emb  = collect_pair_scores_for_db(meta_sim_dict, "")
    cols: List[Column] = []
    seen = set(); DR = {}
    for k, v in uniqueness_dict.items():
        a = k.split("#sep#")
        if len(a) < 2:
            continue
        t, c = a[-2], a[-1]
        try: dr = max(0.0, min(1.0, float(v)))
        except Exception: dr = 0.5
        DR[f"{t}-{c}"] = dr
        if (t, c) not in seen:
            seen.add((t, c)); cols.append(Column(t, c, dr))

    pairs: Dict[Tuple[str, str], float] = {}
    fkfk_only: Dict[Tuple[str, str], float] = {}
    n_pkfk = n_name = 0
    for pair, cv in cont.items():
        pl = list(pair)
        if len(pl) != 2:
            continue
        c1, c2 = pl
        if c1.split("-")[0] == c2.split("-")[0]:
            continue
        ns = name_string_sim(c1, c2)
        used = max(emb.get(pair, 0.0), ns)
        drmax = max(DR.get(c1, 0.5), DR.get(c2, 0.5))
        if drmax < dr_floor or used < name_used_floor:
            continue
        cont_floor = name_containment if ns >= 0.8 else base_containment
        if cv < cont_floor:
            continue
        pairs[(c1, c2)] = used; pairs[(c2, c1)] = used
        if cv >= base_containment:
            n_pkfk += 1
        else:                                   # name-anchored bridge (relaxed containment)
            n_name += 1
            fkfk_only[(c1, c2)] = used; fkfk_only[(c2, c1)] = used

    # original FK-FK recovery pass (embedding-only, no name boost -> avoid generic flood)
    n_fkfk = 0
    for pair, cv in cont.items():
        if cv < fkfk_containment:
            continue
        pl = list(pair)
        if len(pl) != 2:
            continue
        c1, c2 = pl
        if c1.split("-")[0] == c2.split("-")[0]:
            continue
        ev = emb.get(pair, 0.0)
        if ev < fkfk_embedding:
            continue
        if (c1, c2) not in pairs:
            pairs[(c1, c2)] = ev; pairs[(c2, c1)] = ev
            fkfk_only[(c1, c2)] = ev; fkfk_only[(c2, c1)] = ev
            n_fkfk += 1
    print(f"[refined colpairs] PK-FK={n_pkfk} name-anchored={n_name} fkfk-recovery={n_fkfk} "
          f"-> total undirected={len(pairs)//2}, bridges(fkfk_only)={len(fkfk_only)//2}")
    return cols, pairs, fkfk_only, cont



@dataclass
class TableGraphConfig:
    """weight = emb_sim^alpha * dr_weight^beta"""
    alpha: float = 1.0
    beta: float = 0.5
    agg: str = "max"            # "max" | "mean" | "sum"
    min_edge_weight: float = 0.0
    self_loops: bool = False


@dataclass
class ClusterConfig:
    algorithm: str = "hierarchical"   # "hierarchical" | (else) connected-components
    linkage_method: str = "average"
    distance_threshold: float = 0.25
    bridge_betweenness_pct: float = 0.75
    min_cluster_size: int = 2


@dataclass
class RecursiveSplitConfig:
    min_degree: int = 1
    min_density: float = 0.3
    min_split_size: int = 4
    min_cluster_size: int = 2
    max_depth: int = 6
    min_edge_ratio: float = 0.02
    cluster_config: ClusterConfig = field(default_factory=lambda: ClusterConfig(
        algorithm="hierarchical", linkage_method="average", distance_threshold=0.25,
    ))


@dataclass
class DomainResult:
    table_to_domain: Dict[str, int]
    domain_to_tables: Dict[int, List[str]]
    bridge_tables: List[str]
    isolated_tables: List[str]
    graph: nx.Graph
    debug: Dict[str, Any] = field(default_factory=dict)

    def summary(self) -> str:
        lines = [
            f"Domains  : {len(self.domain_to_tables)}",
            f"Clustered: {len(self.table_to_domain)} tables",
            f"Isolated : {len(self.isolated_tables)} tables",
            f"Bridges  : {self.bridge_tables}",
        ]
        for did, tbls in sorted(self.domain_to_tables.items()):
            lines.append(f"  [{did}] ({len(tbls)}): {sorted(tbls)}")
        return "\n".join(lines)


# ══════════════════════════════════════════════════════════════════════════════
# Step 1/2 – column pairs + table graph
# ══════════════════════════════════════════════════════════════════════════════

_LOG1P_ONE = math.log1p(1.0)


def _col_id_to_table(col_id: str) -> str:
    return col_id.split("-")[0]


def _dr_weight(dr1: float, dr2: float) -> float:
    return math.log1p(max(dr1, dr2)) / _LOG1P_ONE


def build_colpair_with_fkfk_recovery(
    db_id: str, meta_sim_dict: Dict, jaccard_sim_dict: Dict, uniqueness_dict: Dict,
    base_kwargs: Dict,
    fkfk_containment_threshold: float = 0.95,
    fkfk_sim_threshold: float = 0.85,
    fkfk_min_dr: float = 0.05,
) -> Tuple[List, Dict, Dict]:
    """Pass1 (DR-gated) -> PK-FK joins;  Pass2 (strict containment + low DR floor)
       -> recover FK-FK joins.  Returns (columns, merged_pairs, fkfk_only_pairs).
       (kept for reference; the entry point now uses build_refined_colpairs.)"""
    cols, pairs1 = build_inputs_for_db(db_id, meta_sim_dict, jaccard_sim_dict, uniqueness_dict, **base_kwargs)
    _, pairs2 = build_inputs_for_db(
        db_id, meta_sim_dict, jaccard_sim_dict, uniqueness_dict,
        **{**base_kwargs,
           "containment_threshold": fkfk_containment_threshold,
           "use_sim_pruning": True, "sim_threshold": fkfk_sim_threshold,
           "use_distinct_ratio_pruning": True, "distinct_ratio_threshold": fkfk_min_dr},
    )
    merged = {**pairs2, **pairs1}
    fkfk_only = {k: v for k, v in pairs2.items() if k not in pairs1}
    print(f"FK-FK recovery: +{len(fkfk_only)//2} undirected pairs "
          f"(cont>={fkfk_containment_threshold}, sim>={fkfk_sim_threshold}, DR>={fkfk_min_dr})")
    return cols, merged, fkfk_only


def build_table_graph(columns: List[Column], colpair_col_sim: Dict[Tuple[str, str], float],
                      config: TableGraphConfig = TableGraphConfig()) -> nx.Graph:
    col_lookup = {f"{c.table}-{c.name}": c for c in columns}
    edge_acc: Dict[frozenset, list] = defaultdict(list)
    for (c1, c2), emb_sim in colpair_col_sim.items():
        t1, t2 = _col_id_to_table(c1), _col_id_to_table(c2)
        if t1 == t2 and not config.self_loops:
            continue
        dr1 = col_lookup[c1].distinct_ratio if c1 in col_lookup else 0.5
        dr2 = col_lookup[c2].distinct_ratio if c2 in col_lookup else 0.5
        drw = _dr_weight(dr1, dr2)
        w = (emb_sim ** config.alpha) * (drw ** config.beta)
        edge_acc[frozenset({t1, t2})].append((w, emb_sim, drw, c1, c2))

    G = nx.Graph()
    for col in columns:
        G.add_node(col.table)
    for edge_key, records in edge_acc.items():
        pair = list(edge_key)
        t1, t2 = (pair[0], pair[0]) if len(pair) == 1 else (pair[0], pair[1])
        ws = [r[0] for r in records]
        final_w = max(ws) if config.agg == "max" else (float(np.mean(ws)) if config.agg == "mean" else float(np.sum(ws)))
        if final_w < config.min_edge_weight:
            continue
        G.add_edge(t1, t2, weight=final_w, n_col_pairs=len(records),
                   max_emb_sim=max(r[1] for r in records), max_dr_weight=max(r[2] for r in records),
                   col_pairs=[(r[3], r[4], r[1], r[0]) for r in records])
    return G


def inject_fkfk_edges(G: nx.Graph, columns: List[Column],
                      fkfk_only: Dict[Tuple[str, str], float],
                      min_sim: float = 0.85, agg: str = "max") -> nx.Graph:
    """Add recovered FK-FK pairs as table edges without the DR penalty (only upgrades)."""
    edge_acc: Dict[frozenset, List[float]] = defaultdict(list)
    for (c1, c2), emb_sim in fkfk_only.items():
        if emb_sim < min_sim:
            continue
        t1, t2 = _col_id_to_table(c1), _col_id_to_table(c2)
        if t1 != t2:
            edge_acc[frozenset({t1, t2})].append(emb_sim)
    for edge_key, sims in edge_acc.items():
        t1, t2 = list(edge_key)
        w = max(sims) if agg == "max" else float(np.mean(sims))
        if G.has_edge(t1, t2):
            if w > G[t1][t2]["weight"]:
                G[t1][t2]["weight"] = w
        else:
            G.add_edge(t1, t2, weight=w, n_col_pairs=len(sims),
                       max_emb_sim=max(sims), max_dr_weight=1.0, col_pairs=[], fkfk=True)
    return G


# ══════════════════════════════════════════════════════════════════════════════
# Step 3 – recursive density-guided clustering -> domains
# ══════════════════════════════════════════════════════════════════════════════

def find_isolated_tables(G: nx.Graph, min_degree: int = 1) -> List[str]:
    return [t for t in G.nodes() if G.degree(t) < min_degree]


def _cluster_hierarchical(G: nx.Graph, tables: List[str], config: ClusterConfig) -> Dict[str, int]:
    n = len(tables)
    idx = {t: i for i, t in enumerate(tables)}
    dist = np.ones((n, n)); np.fill_diagonal(dist, 0.0)
    for u, v, d in G.edges(data=True):
        s = d["weight"]
        dist[idx[u], idx[v]] = dist[idx[v], idx[u]] = max(0.0, 1.0 - s)
    Z = linkage(squareform(dist, checks=False), method=config.linkage_method)
    labels = fcluster(Z, t=config.distance_threshold, criterion="distance")
    return {tables[i]: int(labels[i]) for i in range(n)}


def _cluster_connected_components(G: nx.Graph) -> Dict[str, int]:
    return {t: cid for cid, comp in enumerate(nx.connected_components(G)) for t in comp}


def _merge_tiny_clusters(G: nx.Graph, t2d: Dict[str, int], min_size: int) -> Dict[str, int]:
    d2t: Dict[int, List[str]] = defaultdict(list)
    for t, d in t2d.items():
        d2t[d].append(t)
    tiny = {d for d, tbls in d2t.items() if len(tbls) < min_size}
    if not tiny:
        return t2d
    large = {d for d in d2t if d not in tiny}
    result = dict(t2d)
    for d in tiny:
        for t in d2t[d]:
            best_d, best_w = None, -1.0
            for nb in G.neighbors(t):
                nd = result.get(nb)
                if nd in large and G[t][nb].get("weight", 0.0) > best_w:
                    best_w, best_d = G[t][nb]["weight"], nd
            if best_d is not None:
                result[t] = best_d
            elif large:
                result[t] = min(large)
    return result


def _detect_bridge_tables(G: nx.Graph, t2d: Dict[str, int], pct: float) -> List[str]:
    if G.number_of_edges() == 0:
        return []
    bc = nx.betweenness_centrality(G, weight="weight", normalized=True)
    threshold = np.percentile(list(bc.values()), pct * 100)

    def spans(t: str) -> bool:
        own = t2d.get(t)
        return any(t2d.get(nb) != own for nb in G.neighbors(t))

    return [t for t, b in bc.items() if b >= threshold and b > 0 and spans(t)]


def cluster_tables(G: nx.Graph, config: ClusterConfig = ClusterConfig()) -> DomainResult:
    tables = list(G.nodes())
    if not tables:
        return DomainResult({}, {}, [], [], G, {"error": "empty graph"})
    if config.algorithm == "hierarchical":
        t2d = _cluster_hierarchical(G, tables, config)
    else:
        t2d = _cluster_connected_components(G)
    t2d = _merge_tiny_clusters(G, t2d, config.min_cluster_size)
    d2t: Dict[int, List[str]] = defaultdict(list)
    for t, d in t2d.items():
        d2t[d].append(t)
    bridges = _detect_bridge_tables(G, t2d, config.bridge_betweenness_pct)
    isolated = [t for t in tables if G.degree(t) == 0]
    return DomainResult(t2d, dict(d2t), bridges, isolated, G, {"n_domains": len(d2t)})


def _subgraph_density(G: nx.Graph, tables: List[str]) -> float:
    n = len(tables)
    if n < 2:
        return 1.0
    return G.subgraph(tables).number_of_edges() / (n * (n - 1) / 2)


def _recursive_split(G: nx.Graph, tables: List[str], config: RecursiveSplitConfig,
                     depth: int, id_counter: List[int]) -> Dict[str, int]:
    n = len(tables)
    density = _subgraph_density(G, tables)
    sub = G.subgraph(tables)
    max_possible = n * (n - 1) / 2 if n > 1 else 1
    edge_ratio = sub.number_of_edges() / max_possible
    if (density >= config.min_density or n < config.min_split_size or
            depth >= config.max_depth or edge_ratio < config.min_edge_ratio):
        cid = id_counter[0]; id_counter[0] += 1
        return {t: cid for t in tables}
    sub_result = cluster_tables(sub, config.cluster_config)
    if len(sub_result.domain_to_tables) <= 1:
        cid = id_counter[0]; id_counter[0] += 1
        return {t: cid for t in tables}
    result: Dict[str, int] = {}
    for sub_tables in sub_result.domain_to_tables.values():
        result.update(_recursive_split(G, sub_tables, config, depth + 1, id_counter))
    return result


def recursive_cluster(G: nx.Graph, config: RecursiveSplitConfig = RecursiveSplitConfig()) -> DomainResult:
    isolated = find_isolated_tables(G, config.min_degree)
    isolated_set = set(isolated)
    active = [t for t in G.nodes() if t not in isolated_set]
    if not active:
        return DomainResult({}, {}, [], isolated, G, {"error": "all isolated"})
    initial = cluster_tables(G.subgraph(active), config.cluster_config)
    id_counter = [0]; t2d: Dict[str, int] = {}
    for group_tables in initial.domain_to_tables.values():
        t2d.update(_recursive_split(G, group_tables, config, 0, id_counter))
    d2t: Dict[int, List[str]] = defaultdict(list)
    for t, d in t2d.items():
        d2t[d].append(t)
    bridges = _detect_bridge_tables(G.subgraph(active), t2d, config.cluster_config.bridge_betweenness_pct)
    return DomainResult(t2d, dict(d2t), bridges, isolated, G,
                        {"n_domains": len(d2t), "n_clustered": len(t2d), "n_isolated": len(isolated)})


# ══════════════════════════════════════════════════════════════════════════════
# Step 4 – domain merge
# ══════════════════════════════════════════════════════════════════════════════

def domain_inter_graph(result: DomainResult, agg: str = "max", min_cross_edges: int = 1) -> nx.Graph:
    G, t2d = result.graph, result.table_to_domain
    dg = nx.Graph(); dg.add_nodes_from(result.domain_to_tables.keys())
    edge_weights: Dict[Tuple[int, int], List[float]] = defaultdict(list)
    for u, v, d in G.edges(data=True):
        du, dv = t2d.get(u), t2d.get(v)
        if du is None or dv is None or du == dv:
            continue
        edge_weights[(min(du, dv), max(du, dv))].append(d["weight"])
    for (du, dv), ws in edge_weights.items():
        if len(ws) < min_cross_edges:
            continue
        w = max(ws) if agg == "max" else float(np.mean(ws))
        dg.add_edge(du, dv, weight=w, n_cross_edges=len(ws))
    return dg


def merge_domains(result: DomainResult, merge_groups: List[List[int]]) -> DomainResult:
    old_to_new: Dict[int, int] = {}; next_id = 0
    for group in merge_groups:
        for did in group:
            old_to_new[did] = next_id
        next_id += 1
    for did in result.domain_to_tables:
        if did not in old_to_new:
            old_to_new[did] = next_id; next_id += 1
    new_t2d = {t: old_to_new[d] for t, d in result.table_to_domain.items()}
    new_d2t: Dict[int, List[str]] = defaultdict(list)
    for t, d in new_t2d.items():
        new_d2t[d].append(t)
    bridges = _detect_bridge_tables(result.graph.subgraph(list(new_t2d.keys())), new_t2d, 0.75)
    return DomainResult(new_t2d, dict(new_d2t), bridges, result.isolated_tables, result.graph,
                        {**result.debug, "merged_from": merge_groups})


def auto_merge_domains(result: DomainResult, threshold: float = 0.85,
                       agg: str = "mean", min_cross_edges: int = 2) -> DomainResult:
    dg = domain_inter_graph(result, agg=agg, min_cross_edges=min_cross_edges)
    strong = nx.Graph(); strong.add_nodes_from(dg.nodes())
    for u, v, d in dg.edges(data=True):
        if d["weight"] >= threshold:
            strong.add_edge(u, v, weight=d["weight"])
    cliques = sorted([c for c in nx.find_cliques(strong) if len(c) >= 2], key=lambda c: -len(c))
    if not cliques:
        return result
    assigned: set = set(); merge_groups: List[List[int]] = []
    for clique in cliques:
        free = [d for d in clique if d not in assigned]
        if len(free) >= 2:
            merge_groups.append(free); assigned.update(free)
    return merge_domains(result, merge_groups)


# ══════════════════════════════════════════════════════════════════════════════
# Step 4b/5 – OR-gate inter-domain selection + two-level graph
# ══════════════════════════════════════════════════════════════════════════════

def select_inter_domain_pairs(result: DomainResult, fkfk_only: Dict[Tuple[str, str], float],
                              min_generic_edges: int = 2):
    """Keep a domain pair's inter-cluster edges iff it shows STRONG cross-evidence:
         (a) >=1 FK-FK / name-anchored bridge col-pair, OR
         (b) >=min_generic_edges independent table-pair edges (multi-evidence)."""
    G, t2d = result.graph, result.table_to_domain
    fkfk_tp: Set[frozenset] = set()
    for (c1, c2) in fkfk_only:
        a, b = _col_id_to_table(c1), _col_id_to_table(c2)
        if a != b:
            fkfk_tp.add(frozenset({a, b}))
    pair_edges, pair_fkfk = defaultdict(int), defaultdict(int)
    for u, v, d in G.edges(data=True):
        du, dv = t2d.get(u), t2d.get(v)
        if du is None or dv is None or du == dv:
            continue
        k = frozenset({du, dv}); pair_edges[k] += 1
        if frozenset({u, v}) in fkfk_tp:
            pair_fkfk[k] += 1
    keep = {k for k in pair_edges
            if pair_fkfk.get(k, 0) >= 1 or pair_edges[k] >= min_generic_edges}
    return keep, pair_edges, pair_fkfk


def build_two_level_kept(result: DomainResult, keep_pairs: Set[frozenset]) -> nx.Graph:
    """intra-domain edges: all kept;  inter-domain edges: only for keep_pairs."""
    G, t2d = result.graph, result.table_to_domain
    G_two = nx.Graph(); G_two.add_nodes_from(G.nodes(data=True))
    n_intra = n_inter = n_drop = 0
    for u, v, d in G.edges(data=True):
        du, dv = t2d.get(u), t2d.get(v)
        if du is None or dv is None or du == dv:
            G_two.add_edge(u, v, **d); n_intra += 1
        elif frozenset({du, dv}) in keep_pairs:
            G_two.add_edge(u, v, **d); n_inter += 1
        else:
            n_drop += 1
    print(f"  two-level kept: intra={n_intra}  inter={n_inter}  dropped_inter={n_drop}")
    return G_two


# ══════════════════════════════════════════════════════════════════════════════
# Step 6 – export to dw_join_keys.json format (+ per-edge confidence)
# ══════════════════════════════════════════════════════════════════════════════

def _to_dot(cid: str) -> str:                    # "TABLE-COL" -> "TABLE.COL"
    t = cid.split("-")[0]
    return f"{t}.{cid[len(t) + 1:]}"


def export_join_keys(kept_table_edges: Set[frozenset], pairs: Dict[Tuple[str, str], float],
                     cont: Dict[frozenset, float], out_path: str, conf_path: str):
    """Write surviving table edges' justifying column pairs + per-edge confidence
       (containment * name_used).  Works for any kept_table_edges set."""
    out, seen = [], set()
    conf: Dict[str, float] = defaultdict(float)
    for (c1, c2), used in pairs.items():
        t1, t2 = _col_id_to_table(c1), _col_id_to_table(c2)
        if t1 == t2 or frozenset({t1, t2}) not in kept_table_edges:
            continue
        a, b = _to_dot(c1), _to_dot(c2)
        key = tuple(sorted([a, b]))
        if key not in seen:
            seen.add(key); out.append([a, b])
        cv = cont.get(frozenset({c1, c2}), 0.0)
        ck = f"{t1.upper()}|{t2.upper()}" if t1.upper() < t2.upper() else f"{t2.upper()}|{t1.upper()}"
        conf[ck] = max(conf[ck], cv * used)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1, ensure_ascii=False)
    with open(conf_path, "w", encoding="utf-8") as f:
        json.dump(conf, f)
    print(f"  wrote {len(out)} join-key pairs ({len(kept_table_edges)} table edges) -> {out_path}")
    print(f"  wrote {len(conf)} edge confidences -> {conf_path}")
    return out
def _domain_result_with_partition(G: nx.Graph, t2d: Dict[str, int]) -> DomainResult:
    """Wrap a graph with an EXISTING table->domain partition (so both graphs share domains)."""
    d2t: Dict[int, List[str]] = defaultdict(list)
    for t, d in t2d.items():
        d2t[d].append(t)
    return DomainResult(dict(t2d), dict(d2t), [], [], G, {})




# ══════════════════════════════════════════════════════════════════════════════
# Entry point
# ══════════════════════════════════════════════════════════════════════════════

def build_join_graph(
    paths: "P.Paths",
    dense_min_edge_weight: float = 0.4,
    min_generic_edges: int = 2,
    base_containment_threshold: float = 0.8,
    base_sim_threshold: float = 0.6,
    base_distinct_ratio_threshold: float = 0.9,
    fkfk_containment_threshold: float = 0.95,
    fkfk_sim_threshold: float = 0.85,
    fkfk_min_dr: float = 0.05,
    refined_base_containment: float = 0.8,
    refined_name_containment: float = 0.3,
    refined_name_used_floor: float = 0.6,
    refined_dr_floor: float = 0.9,
    refined_fkfk_containment: float = 0.95,
    refined_fkfk_embedding: float = 0.85,
    cluster_distance_threshold: float = 0.25,
    auto_merge_threshold: float = 0.80,
) -> Dict[str, Any]:
    """Build the domain-gated join graph for one dataset."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

    out_domain = paths.out("dw_join_keys_g_domain.json")
    conf_domain = paths.out("edge_conf_g_domain.json")

    tables, meta_sim, uniq, jac = load_data(
        str(paths.profile("tables")),
        str(paths.profile("semantic_col_sim")),
        str(paths.profile("uniqueness")),
        str(paths.profile("jaccard")),
    )

    # (A) strict base column pairs -> intra-domain edges + the domain partition
    cols, pairs_base, fkfk_base = build_colpair_with_fkfk_recovery(
        "",
        meta_sim,
        jac,
        uniq,
        base_kwargs=dict(
            containment_threshold=base_containment_threshold,
            use_sim_pruning=True,
            sim_threshold=base_sim_threshold,
            use_distinct_ratio_pruning=True,
            distinct_ratio_threshold=base_distinct_ratio_threshold,
        ),
        fkfk_containment_threshold=fkfk_containment_threshold,
        fkfk_sim_threshold=fkfk_sim_threshold,
        fkfk_min_dr=fkfk_min_dr,
    )

    # (B) refined column pairs (string name signal + name-aware containment relax)
    #     -> cross-domain edges
    _, pairs_ref, fkfk_ref, cont = build_refined_colpairs(
        meta_sim,
        jac,
        uniq,
        base_containment=refined_base_containment,
        name_containment=refined_name_containment,
        name_used_floor=refined_name_used_floor,
        dr_floor=refined_dr_floor,
        fkfk_containment=refined_fkfk_containment,
        fkfk_embedding=refined_fkfk_embedding,
    )

    # ---- domain partition: cluster the strict base table graph ----
    G_base = build_table_graph(
        cols, pairs_base,
        TableGraphConfig(beta=0.5, min_edge_weight=dense_min_edge_weight),
    )
    G_base = inject_fkfk_edges(G_base, cols, fkfk_base, min_sim=fkfk_sim_threshold)

    cfg = RecursiveSplitConfig(
        min_degree=1,
        min_density=0.3,
        cluster_config=ClusterConfig(
            algorithm="hierarchical",
            distance_threshold=cluster_distance_threshold,
        ),
    )
    res = recursive_cluster(G_base, cfg)
    res = auto_merge_domains(res, threshold=auto_merge_threshold, agg="mean", min_cross_edges=2)
    t2d = res.table_to_domain
    print(f"\n[domains] {len(res.domain_to_tables)} domains")

    # ---- g_domain: strict intra-domain edges + gated refined cross-domain edges ----
    keep_base, _, _ = select_inter_domain_pairs(res, fkfk_base, min_generic_edges)
    G_two_base = build_two_level_kept(res, keep_base)

    G_ref = build_table_graph(
        cols, pairs_ref,
        TableGraphConfig(beta=0.5, min_edge_weight=dense_min_edge_weight),
    )
    G_ref = inject_fkfk_edges(G_ref, cols, fkfk_ref, min_sim=0.80)

    res_ref = _domain_result_with_partition(G_ref, t2d)  # reuse the same partition
    keep_ref, _, _ = select_inter_domain_pairs(res_ref, fkfk_ref, min_generic_edges)

    edges_domain: Set[frozenset] = set()
    for u, v in G_two_base.edges():  # intra-domain: strict edges
        if t2d.get(u) is not None and t2d.get(u) == t2d.get(v):
            edges_domain.add(frozenset({u, v}))

    n_cross = 0
    for u, v in G_ref.edges():  # cross-domain: refined edges, OR-gated
        du, dv = t2d.get(u), t2d.get(v)
        if du is not None and dv is not None and du != dv and frozenset({du, dv}) in keep_ref:
            edges_domain.add(frozenset({u, v}))
            n_cross += 1

    print(f"  g_domain: intra(strict)={len(edges_domain) - n_cross} cross(refined,gated)={n_cross}")

    pairs_all = {**pairs_ref, **pairs_base}
    export_join_keys(edges_domain, pairs_all, cont, str(out_domain), str(conf_domain))

    return {
        "dataset": paths.dataset,
        "join_graph": str(out_domain),
        "edge_conf": str(conf_domain),
        "num_table_edges": len(edges_domain),
        "num_domains": len(res.domain_to_tables),
    }


def parse_args():
    parser = argparse.ArgumentParser(
        description="Stage 0: build the profiling-based join graph (g_domain).")
    P.add_arguments(parser)

    # Domain partition / gate.
    parser.add_argument("--dense-min-edge-weight", type=float, default=0.4,
                        help="Minimum table-edge weight when building the dense "
                             "table graph used for clustering.")
    parser.add_argument("--min-generic-edges", type=int, default=2,
                        help="Cross-domain OR-gate: a domain pair is opened only "
                             "if it has at least this many independent table links.")
    parser.add_argument("--cluster-distance-threshold", type=float, default=0.25,
                        help="Hierarchical clustering distance threshold.")
    parser.add_argument("--auto-merge-threshold", type=float, default=0.80,
                        help="Threshold for auto-merging strongly connected domains.")

    # Strict base column-pair thresholds.
    parser.add_argument("--base-containment-threshold", type=float, default=0.8)
    parser.add_argument("--base-sim-threshold", type=float, default=0.6)
    parser.add_argument("--base-distinct-ratio-threshold", type=float, default=0.9)
    parser.add_argument("--fkfk-containment-threshold", type=float, default=0.95)
    parser.add_argument("--fkfk-sim-threshold", type=float, default=0.85)
    parser.add_argument("--fkfk-min-dr", type=float, default=0.05)

    # Refined column-pair thresholds.
    parser.add_argument("--refined-base-containment", type=float, default=0.8)
    parser.add_argument("--refined-name-containment", type=float, default=0.3)
    parser.add_argument("--refined-name-used-floor", type=float, default=0.6)
    parser.add_argument("--refined-dr-floor", type=float, default=0.9)
    parser.add_argument("--refined-fkfk-containment", type=float, default=0.95)
    parser.add_argument("--refined-fkfk-embedding", type=float, default=0.85)
    return parser.parse_args()


if __name__ == "__main__":
    a = parse_args()
    build_join_graph(
        P.from_args(a),
        dense_min_edge_weight=a.dense_min_edge_weight,
        min_generic_edges=a.min_generic_edges,
        base_containment_threshold=a.base_containment_threshold,
        base_sim_threshold=a.base_sim_threshold,
        base_distinct_ratio_threshold=a.base_distinct_ratio_threshold,
        fkfk_containment_threshold=a.fkfk_containment_threshold,
        fkfk_sim_threshold=a.fkfk_sim_threshold,
        fkfk_min_dr=a.fkfk_min_dr,
        refined_base_containment=a.refined_base_containment,
        refined_name_containment=a.refined_name_containment,
        refined_name_used_floor=a.refined_name_used_floor,
        refined_dr_floor=a.refined_dr_floor,
        refined_fkfk_containment=a.refined_fkfk_containment,
        refined_fkfk_embedding=a.refined_fkfk_embedding,
        cluster_distance_threshold=a.cluster_distance_threshold,
        auto_merge_threshold=a.auto_merge_threshold,
    )
