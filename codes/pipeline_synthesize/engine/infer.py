"""
infer.py
--------
Single-table "next operation" inferrer, designed to replace the LLM generation step in

Given a table file (or DataFrame) plus a schema specification:
  1. build schema-conditioned features;
  2. use the trained classifier (plus hard rules) to propose candidate operations
  3. for each selected candidate op, retrieve from training_data the case with the same
     op and the nearest feature vector, and render it as a usage example (formatted like

Main interface:
    infer = SingleOpInfer()
    out = infer.predict(table, schema_spec, top_k=1)
    #   out["candidates"]  -> [op, ...]        the op decision, replacing the LLM's
    #   out["ranked"]      -> [(op, prob), ...] full calibrated probabilities
    #   out["examples"]    -> {op: markdown}    a retrieved usage example per candidate

schema_spec may be:
    - a dict (the react runner's table_spec style: create_table_sql / column_types /
    - a str  (a single CREATE TABLE ... statement)
"""
from __future__ import annotations
import json, os, re, glob
import numpy as np
import pandas as pd
import joblib

from features import featurize, sanitize, FEATURE_NAMES
from schema_spec import spec_to_schema, parse_create_table, schema_to_sql, expand_view_to_full

HERE = os.path.dirname(os.path.abspath(__file__))
from engine_paths import SINGLE_OP_MODEL as _SINGLE_OP_MODEL
MODEL = os.environ.get("SINGLE_OP_MODEL_PATH", str(_SINGLE_OP_MODEL))
from engine_paths import OPERATION_DETAILS as _OPERATION_DETAILS
DETAILS = os.environ.get("PREPWEAVER_OPERATION_DETAILS", str(_OPERATION_DETAILS))
# Resolved by engine/paths.py; the examples ship with the engine.
from engine_paths import USAGE_EXAMPLES_DIR as _USAGE_EXAMPLES_DIR
USAGE_DIR = str(_USAGE_EXAMPLES_DIR)

_MONTHS = ("jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec")
def _norm(x): return re.sub(r"[^a-z0-9]", "", str(x).lower())


# ---------------- hard rules (injected after threshold filtering; see the earlier
def hard_rules(df, schema, pk, aggressive_datetime=False) -> list:
    hits = []
    cur_cols = [str(c) for c in df.columns]
    tgt_norm = [_norm(t) for t in schema]

    # WideToLong: some target column name is expanded as a prefix by >=2 current columns,
    cur_norm_set = {_norm(c) for c in cur_cols}
    unmatched_tgt = [t for t in tgt_norm if t and t not in cur_norm_set
                     and not any(_norm(c).startswith(t) for c in cur_cols)]
    for t in tgt_norm:
        if len(t) < 3: continue
        exp = [c for c in cur_cols if _norm(c) != t and _norm(c).startswith(t)]
        if len(exp) >= 2 and len(unmatched_tgt) >= 1:
            hits.append("WideToLong"); break

    # StandardizeDatetime: off by default (many tables happen to hold non-ISO date columns
    if aggressive_datetime:
        _t = r"(\s+\d{1,2}:\d{2}(:\d{2})?\s*([AaPp][Mm])?)?"
        md = r"(?i)(" + "|".join(_MONTHS) + r")[a-z]*\.?\s+\d{1,2},?\s+\d{4}" + _t
        md2 = r"(?i)\d{1,2}\s+(" + "|".join(_MONTHS) + r")[a-z]*\.?\s+\d{4}" + _t
        nd = r"\d{1,4}[/\-.]\d{1,2}[/\-.]\d{1,4}" + _t
        date_full = f"({md})|({md2})|({nd})"
        sdf = df.iloc[:200, :60]
        for c in sdf.columns:
            s = sdf[c].astype(str).str.strip()
            if pd.to_numeric(s, errors="coerce").notna().mean() > 0.8: continue
            if s.str.fullmatch(date_full).mean() > 0.5 and s.str.fullmatch(r"\d{4}-\d{2}-\d{2}").mean() < 0.9:
                hits.append("StandardizeDatetime"); break
    return hits


# ---------------- op definitions (the Definition lines of operation_usage_examples) ----
def _load_definitions():
    defs = {}
    for p in glob.glob(os.path.join(USAGE_DIR, "*.md")):
        txt = open(p).read()
        m = re.search(r"^##\s+(\w+)", txt, re.M)
        d = re.search(r"Definition:\s*(.+)", txt)
        if m and d:
            defs[m.group(1)] = d.group(1).strip()
    return defs


class SingleOpInfer:
    def __init__(self, thresh=0.15):
        self.thresh = thresh
        bundle = joblib.load(MODEL)
        self.clf = bundle["clf"]
        self.fnames = bundle["feature_names"]
        self.train_X = np.array(bundle["train_X"], float)
        self.train_y = np.array(bundle["train_y"])
        self.train_ids = np.array(bundle["train_ids"])
        # Standardisation scale (for nearest neighbour), ignoring nan
        self.mu = np.nanmean(self.train_X, axis=0)
        self.sd = np.nanstd(self.train_X, axis=0); self.sd[self.sd == 0] = 1.0
        # Detail store (task_id -> record), used to render the example
        self.details = {json.loads(l)["task_id"]: json.loads(l) for l in open(DETAILS)}
        self.defs = _load_definitions()

    # ---- normalise the schema spec ----
    @staticmethod
    def _resolve_schema(schema_spec):
        if isinstance(schema_spec, str):
            return parse_create_table(schema_spec)
        return spec_to_schema(schema_spec)

    @staticmethod
    def _load_table(table):
        if isinstance(table, pd.DataFrame):
            return table
        if str(table).endswith(".pkl"):
            return pd.read_pickle(table)
        if str(table).endswith(".csv"):
            return pd.read_csv(table)
        return pd.read_pickle(table)

    def _impute(self, x):
        x = x.copy()
        m = np.isnan(x)
        x[m] = self.mu[m]
        return x

    def _nearest(self, x, op):
        """Among the training samples with the same op, the task_id with the nearest feature vector."""
        idx = np.where(self.train_y == op)[0]
        if len(idx) == 0:
            return None
        xz = (self._impute(x) - self.mu) / self.sd
        best, bd = None, np.inf
        for i in idx:
            xi = (self._impute(self.train_X[i]) - self.mu) / self.sd
            d = np.linalg.norm(xz - xi)
            if d < bd: bd, best = d, self.train_ids[i]
        return best

    def _render_example(self, op, task_id):
        """Render the retrieved case as a usage example (matching the operation_usage_examples format)."""
        rec = self.details.get(task_id)
        definition = self.defs.get(op, "")
        if not rec:
            return f"## {op}\n\nDefinition: {definition}\n(no retrieved case)"
        return (
            f"## {op}\n\n"
            f"Definition: {definition}\n\n"
            f"Pattern (retrieved nearest case: {task_id}):\n"
            f"Raw table preview:\n```text\n{rec['raw_table_preview']}\n```\n"
            f"Target schema:\n```sql\n{rec['target_schema_sql']}\n```\n"
            f"Correct operation:\n```json\n{rec['operation']}\n```\n"
        )

    def predict(self, table, schema_spec, top_k=1, aggressive_datetime=False,
                db_id=None, source=None):
        """When db_id and source are given, expand the (possibly minimal view) schema into
        the full DB table schema, aligning it with the training distribution. This is key to inference accuracy: a view schema drifts the features."""
        df = sanitize(self._load_table(table))
        if db_id is not None and source is not None:
            schema, pk = expand_view_to_full(schema_spec, db_id, source)
        else:
            schema, pk = self._resolve_schema(schema_spec)
        x = featurize(df, schema, pk)

        proba = self.clf.predict_proba(x.reshape(1, -1))[0]
        ranked = sorted([(op, float(p)) for op, p in zip(self.clf.classes_, proba)],
                        key=lambda t: -t[1])

        # candidates: top-k first, then anything over the threshold (de-duplicated), with
        cands = [op for op, _ in ranked[:top_k]]
        for op, p in ranked[top_k:]:
            if p >= self.thresh and op not in cands:
                cands.append(op)
        for op in hard_rules(df, schema, pk, aggressive_datetime):
            if op not in cands:
                cands.insert(0, op)

        examples = {op: self._render_example(op, self._nearest(x, op)) for op in cands}
        return {"ranked": ranked, "candidates": cands, "examples": examples,
                "target_schema": schema, "primary_key": sorted(pk)}


if __name__ == "__main__":
    infer = SingleOpInfer()
    # demo: use one benchmark sample
    rec = json.loads(open(DETAILS).readline())
    tid = rec["task_id"]
    # locate its original table
    import glob as _g
    bench = [json.loads(l) for l in open(os.environ["SINGLE_OP_TRAINING_BENCHMARK"])]
    br = next(r for r in bench if r["task_id"] == tid)
    src_dir = os.path.join(os.environ["AUTOPREP_ROOT"], os.path.dirname(br["source_file"]))
    df = pd.read_pickle(os.path.join(src_dir, br["input_table"][0]))
    out = infer.predict(df, rec["target_schema_sql"], top_k=1)
    print("gold op:", rec["op_type"])
    print("candidates:", out["candidates"])
    print("ranked top3:", out["ranked"][:3])
    print("\n--- example for top candidate ---")
    print(out["examples"][out["candidates"][0]])
