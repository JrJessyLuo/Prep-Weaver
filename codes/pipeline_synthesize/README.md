# Pipeline Synthesis

From the tables `table_discovery` selected, synthesize the relational schema and
then the pipeline that materialises it.

| Stage | File | Input | Output |
|---|---|---|---|
| 1 | `relational_schema.py` | `table_selection.jsonl` + raw tables | `relational_schema.jsonl` |
| 2 | `synthesize.py` | relational schema + raw tables | `pipeline.jsonl` |
| 2b | `candidate_graph.py` | per-table candidate pools | one chosen candidate per table |
| — | `engine/` | the search machinery stage 2 runs on | — |

`verify_graph_alignment.py` checks stage 2b against the original selector.

## Stage 1 — relational schema

```bash
python -m pipeline_synthesize.relational_schema --dataset Synth-Bird
python -m pipeline_synthesize.relational_schema --dataset Beaver-Prep --limit 5
```

Output: `results/pipeline_synthesize/schema/<Dataset>/relational_schema.jsonl`

```json
{"task_id": "...", "question": "...", "input_tables": ["..."],
 "tables":     [{"logical_table": "table_1", "input_file": "...",
                 "db_table": "...", "create_table_sql": "CREATE TABLE ..."}],
 "join_edges": [{"left_table": "table_1", "left_on": "id",
                 "right_table": "table_2", "right_on": "user_id"}]}
```

**The answer SQL is gone.** This stage declares the *shape* of the prepared
data — each table's post-preparation `CREATE TABLE` and the join keys between
them. Answering the question is a separate concern, so `sql` is no longer asked
for, produced, or stored, and the output key is `tables` rather than
`gold_tables` (which named a ground-truth artefact this stage does not have).

Everything else is unchanged: the four layout detectors, the grounding-evidence
rules, and the deterministic post-processing (transposed-key recovery, primary
key completion, edge validation) are carried over verbatim, because each of
those fixes a measured error and the record of why is in the docstrings.

## Stage 2b — joint candidate selection as maximum-weight clique

Stage 2 searches an operator chain per table and keeps several finished
candidates for each. Those pools must be combined into one selection, and the
choice cannot be made table by table: the candidate that looks best alone is
often the one that breaks the join.

### The graph

| | |
|---|---|
| part | one logical table |
| node | one terminal candidate of that table |
| node weight | `2.0 * declared-schema name coverage + 0.25 * search score` |
| edge weight | over the schema's join edges: `2.0 * best value-overlap ratio + 0.25 * key quality each side`; `-1.0` if a declared key column is missing from the frame |

Every candidate of table A pairs with every candidate of table B, so the graph
is **complete multipartite**: a clique holds at most one node per part, and a
maximum one holds exactly one. Cliques *are* the selections.

### Why it is an exact reformulation

The original objective is a sum of terms involving one table or two, so it
decomposes with no remainder into node weights, edge weights, and a constant
(the penalty for edges naming a table with no candidate pool — identical for
every selection, so it cannot change the winner, but is carried so reported
scores match).

Since the decomposition is exact and every transversal is a clique, an exact
max-weight clique **equals** the exhaustive argmax by construction. Tie-breaking
is part of the contract and is reproduced: parts in schema order, candidates in
rank order, improvement on a strict `>`, so among equal scores the first in the
original's `itertools.product` order still wins.

### The solver, and where it comes from

There is no off-the-shelf solver for this exact problem.
`networkx.max_weight_clique` implements Östergård's branch and bound (*A new
algorithm for the maximum-weight clique problem*, Discrete Applied Mathematics
120, 2002 — the Cliquer solver), but it takes **node weights only**; this
objective also has edge weights, which that formulation cannot express. Pushing
edge weights onto nodes by subdividing edges would destroy the multipartite
structure.

With node *and* edge weights and one label per part, the problem is exactly MAP
inference in a fully connected discrete pairwise Markov random field (parts =
variables, nodes = labels, node weights = unary potentials, edge weights =
pairwise potentials). The exact method there is branch and bound with a
decomposition bound, and that is what `candidate_graph.py` implements:
Östergård's skeleton, with the bound obtained by maximising every not-yet-fixed
term on its own — admissible because independent maxima can only overestimate a
joint maximum.

`method="exhaustive"` keeps the original enumeration as the reference
implementation.

### Cost

The product scores `|pool|^|tables|` combinations, each re-deriving the same
pairwise terms. The graph computes each pairwise term once — `Σ |A|x|B|` over
joined part pairs. For 7 tables x 6 candidates that is 756 pair evaluations
against 279,936 combination evaluations.

### Verifying it

```bash
python -m pipeline_synthesize.verify_graph_alignment --trials 400
```

This deliberately does **not** re-run the LLM. Comparing two full runs would
measure the model's nondeterminism — different chains, different pools — not the
selector. Instead it fixes the candidate pools and compares only the step under
test, so the LLM is out of the picture by construction. Agreement is required to
be exact; a mismatch is a bug, not noise.

## Stage 2 — pipeline synthesis

```bash
python -m pipeline_synthesize.synthesize --dataset Synth-Bird --limit 1
```

Output: `results/pipeline_synthesize/pipeline/<Dataset>/pipeline.jsonl` — per
logical table the operator chain, its parameters, the resulting columns and
shape, the join keys, and the whole terminal candidate pool (frames dropped,
columns and shape kept, so "was a correct table ever reachable" stays answerable
after the fact).

Differences from the version this was extracted from:

- Reads a **relational schema**, not a plan, and never touches an answer SQL.
  The engine derives join edges by merging the explicit `join_edges` with edges
  parsed out of a `sql` field; with no SQL it uses the explicit set alone. This
  also changes the completion target: `_Loop` narrowed it to the columns the
  plan's own query referenced, and with no query the target is the full declared
  schema. That is a behaviour change worth watching in the first full run.
- Schema alignment is hard-OFF (it rewrote a predicted schema into the
  database's real one).
- The `oneshot` ablation generator is gone; `OP_GENERATOR` no longer applies.
- Joint selection goes through the graph.

## `engine/` — the search machinery

Twenty modules, ~7,000 lines, lifted from `novel_prep`: the bounded beam search,
the operator library and executor, the LLM parameter synthesizer, the feature
extractor and trained policy, join-key repair, and the schema conformance pass.

They import each other by bare name, as they did in the tree they came from.
Rewriting 7,000 lines of measured, working code into relative imports would be a
large edit whose only benefit is style, and every such edit is a chance to break
something. So the flat layout is preserved and `engine/__init__.py` puts its own
directory on `sys.path`. Importing the package therefore has a side effect on
`sys.path` — deliberate, and the price of not rewriting the engine.

`engine/paths.py` is the one place that resolves the engine's own files. The
original `NOVELPREP_ROOT` / `AUTOPREP_ROOT` variables still work as overrides,
but nothing defaults to them any more:

| what | where it lives now | size |
|---|---|---|
| multistep policy (next op given the chain prefix) | `Prep-Weaver/models/model_multistep_m4_prefix_history.joblib` | 12 MB |
| single-op classifier (`SingleOpInfer`) | `Prep-Weaver/models/model.joblib` | 3.2 MB |
| operation details, indexed by task_id | `engine/resources/operation_details.jsonl` | 836 KB |
| operator usage examples | `engine/resources/operation_usage_examples/` | 13 files |
| ground-truth schemas | unset — alignment-only, and alignment is off | — |

There are **two** classifiers, not one: the multistep policy predicts the next
operator given the chain prefix, while `SingleOpInfer` scores one operation in
isolation and is imported by six engine modules. Both are small enough to
version with the repository.

`lineage`, the external DeepPrep tracer, is now imported on first use rather
than at module level. It is needed only by `trace_code`, which scores exported
scripts, but it sat in `eval_react_subtables` — which `phase2_joinkey` imports
for join repair — so synthesis used to fail outright on any machine without a
DeepPrep checkout, for a function synthesis never calls.

`engine/prep_utils.py` supplies the `llm_generate_setup` / `timed_llm_generate`
the engine imports lazily, routed through `common/llm_client.py` so credentials
and retries live in one place. The laziness is also what makes the per-task
token meter work: `synthesize` rebinds that name, and the engine resolves it at
call time.

Verified after the move: no `novel_prep` entry on `sys.path`, the classifier
loads (`CalibratedClassifierCV`, 12 classes, 62 features), the 13 usage examples
resolve, and the operator executor runs a real chain.

## The operator classifier

```
model_multistep_m4_prefix_history.joblib      12 MB
```

Small enough to keep in the repository — smaller than a single input table — so
it lives in `Prep-Weaver/models/` and needs no external hosting. Override with
`--policy-model` or `PREPWEAVER_POLICY_MODEL`.

Source: `novel_prep/train_infer_single_ops/trained_model/`.

## Verification

Stage 2 has been run end to end with the LLM stubbed, which exercises the search,
both classifiers, feature extraction, candidate selection and join repair without
spending anything. That dry run is what found four resources the import trace had
missed — `model.joblib`, `operation_details.jsonl`, three lazily imported modules
(`features_multistep_v2`, `build_training_data`, `param_hints`), and the `lineage`
hard dependency — each of which was imported inside a function and so invisible
to a static or import-time scan.

Reproduce it before any expensive run:

```python
import prep_utils as PU
PU.llm_generate_setup = lambda p, **k: {"text": '{"params": {}}',
                                        "input_tokens": 0, "output_tokens": 0}
```

Still to watch on the first REAL task: the completion-target change described
above (full declared schema instead of the queried columns).
