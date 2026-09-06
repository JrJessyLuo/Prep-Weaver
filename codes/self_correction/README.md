# Self-Correction

Diagnose a synthesized pipeline, revise it, keep what helps.

```
table_discovery → pipeline_synthesize → self_correction
```

## The tree

`tree.py` replaces the original 3-round linear loop with an explicit search tree.

| | |
|---|---|
| root | the state pipeline synthesis produced, before any revision |
| node | one state: subtables plus the artefacts that produced them |
| edge | the revise action that turned the parent into this node |

**Depth expansion** revises a node again, so round 2 builds on round 1 — the
only direction the original loop could go. **Breadth expansion** runs a
*different* action from the same parent. The original reached this only by
rolling back and retrying, which threw the candidate away; here both siblings
stay in the tree and both remain selectable.

Breadth exists because the localizer's four-class accuracy is 0.618 while hit@2
is 0.80. A single chain commits to a guess that is wrong a third of the time and
can only recover by spending a round discovering it.

Two decisions, deliberately separate:

```
delta > expand_threshold   →  EXPAND this node (a child builds on it)
max p_ok                   →  RETURN this node
```

The 0.05 threshold was calibrated for the first, where being wrong costs the
remaining budget. It is far too strict for the second, where being wrong costs
nothing: of 3 tasks whose metrics improved in the original run, 2 had deltas
below it and were rolled back — `bird_3f3aba77` at 0.0377 (subtable_full
False→True, join_key 0→1) and `bird_fcdb05fc` at 0.0007 (join_key 0→1).
Selecting only kept states would have scored 11/20 and 15/20 instead of 12/20
and 17/20. Note what 0.0007 says: delta's *magnitude* carries almost no
information. Only its sign is usable, at 0.758 agreement — which is why it gates
expansion and never selection.

```bash
python -m self_correction.loop --dataset Synth-Bird --limit 1
python -m self_correction.loop --dataset Synth-Bird --breadth 2 --max-depth 3
```

`--max-nodes` is the real cost cap: depth × breadth bounds the shape, but the
node budget bounds the spend.

Each record carries the whole tree, so a run can be re-read without re-running
it. `RepairTree.render()` prints it:

```
[0] root                     p_ok=0.4000
    [1] revise_table             p_ok=0.7000 (+0.3000)
        [3] revise_pipeline          p_ok=1.0000 (+0.3000) <- BEST
    [2] revise_pipeline          p_ok=0.7000 (+0.3000)
        [4] revise_table             p_ok=1.0000 (+0.3000)
```

## The three actions

| action | what it does | measured |
|---|---|---|
| `revise_table` | re-select input tables with the diagnosis fed in, then a fresh relational schema and full re-synthesis | 6/32 → 16/32 vs a retry-only control, McNemar p = 0.0063 |
| `revise_relational_plan` | conservative schema revision: abstention short-circuits, only additive column changes, tables matched by `input_file`, regression veto | 3/12 → 5/12 subtable_full, 6/12 → 9/12 join_key_full |
| `revise_pipeline` | rewrite one table's pipeline as pandas, applied **blind** | the "improved and not regressed" validator accepted 0/8; blind moved 5 |

Everything downstream of an action re-runs:

```
revise_table            → relational schema → pipeline synthesis
revise_relational_plan  →                     pipeline synthesis
revise_pipeline         →  (its output IS the tables; nothing follows)
```

## The localizer

The mainline is the **staged** model: a frozen `answerdotai/ModernBERT-base`
encoder (149M parameters) with trained heads on top, giving a posterior over
`revise_table | revise_relational_plan | revise_pipeline | no_revision_needed`.

The shipped checkpoint (`twostage_s1_fixed`) has **`lora: 0`** — no adapters at
all. All 25 trained tensors are heads and normalisation statistics (`proj`,
`norm`, `tab_head`, 12 `scorers`, the jk/tk/tab mean-std buffers), 16,326
elements total, plus the 4 added marker-token embeddings. The encoder is
untouched, so this is a linear probe over frozen ModernBERT features, not a
fine-tune. `model_staged.load_checkpoint` still handles a LoRA checkpoint if one
is trained later; this one simply has none.

Its own reported AUCs, from the checkpoint's `result` field over 141 tasks:

| head | AUC |
|---|---|
| trigger (is anything wrong) | 0.735 |
| revise_table | 0.770 |
| revise_pipeline | **0.543** |
| routing | 0.746 |

`revise_pipeline` at 0.543 is near chance, and that shows up in practice — see
"A measured limitation" below.

### Running it remotely (how this model has actually been run)

The loop must execute where the DATA is — it re-runs table selection and
re-synthesises pipelines against the raw pickles, and its states exist only in
that process. The encoder must execute where the GPU is. `--localizer-kind
remote` is the seam between those two facts: evidence text out, three
probabilities back. Table names are anonymised **client-side**, before the
request, so the two ends cannot disagree about what the model read and no real
file name leaves the machine.

On the GPU box:

```bash
python serve_localizer.py --checkpoint runs/twostage_s1_fixed/checkpoint.pt \
                          --meta ../data/train2.meta.json --port 8077
```

(`internal/serve_localizer.py` is the same server, if you serve from this
checkout.)

Tunnel, then run:

```bash
ssh -N -L 8077:localhost:8077 <user>@<host>
python -m self_correction.loop --dataset Synth-Spider --localizer-kind remote
```

Default endpoint is `http://127.0.0.1:8077`; override with `--localizer-url` or
`PREPWEAVER_LOCALIZER_URL`.

### Running it locally

**The checkpoint is small and belongs in the repository.** It stores only the
*trainable* tensors — LoRA weights, the heads, the added marker tokens'
embeddings. The frozen encoder is rebuilt from its HuggingFace name, so the file
is a few hundred KB rather than the ~600 MB a full state dict would be, and
`transformers` downloads and caches the base encoder on first use. No external
hosting needed.

Two files, from the **same** training run, in `Prep-Weaver/models/`:

| file | server-side source |
|---|---|
| `localizer_staged.pt` | `training/runs/twostage_s1_fixed/checkpoint.pt` |
| `localizer_staged.meta.json` | `data/train2.meta.json` — **already in the repo** |

The tokenizer must match exactly. A mismatched meta maps the marker tokens to
different ids and the heads then read noise rather than failing loudly, so the
`.meta.json` must come from the run that produced the `.pt`.

Override with `PREPWEAVER_LOCALIZER` / `PREPWEAVER_LOCALIZER_META`, or
`--checkpoint` / `--meta`. `--localizer-kind llm` is the comparison arm.

## Connecting to the upstream modules

`internal/` holds the diagnostic, evidence, scoring and localizer code lifted
from the research tree. Three of its modules are **shims** that map the old
names onto Prep-Weaver's stages, so the action code connects unchanged:

| old name | now backed by |
|---|---|
| `schema_linking` | `table_discovery.table_selection` (with `prompt_suffix`) |
| `relational_plan` | `pipeline_synthesize.relational_schema` |
| `pipeline_synthesize` | `pipeline_synthesize.synthesize` |

`prompt_suffix` is the hook `revise_table` needs: a repair must differ from the
first pass by the diagnostic evidence and **nothing else**, or an A/B measures
the prompt rewrite instead of the evidence.

`load_state` reads the three upstream artefacts and re-materialises the
subtables by replaying each recorded chain on its raw frame — `pipeline.jsonl`
stores columns and shape, not frames.

Like `engine/`, `internal/` goes on `sys.path` rather than being rewritten into
relative imports. Its config module is named `engine_paths.py`, not `paths.py`,
because a bare `paths` on the flat path silently shadowed `self_correction/paths.py`.

## A worked example

On `spider_05ce58d1` the localizer scored the synthesized state 0.6013 and
ranked `no_revision_needed` first. Forced to act with `--trigger-threshold 0.8`,
`revise_pipeline` concatenated `Name_Part1 + Name_Part2` into `Region_Name` and
the localizer scored that lower, so the tree kept the original.

The external evaluator then scored the original state `subtable_cov 1.0,
join_key 1.0` — it was already fully correct. So the localizer's decision was
right on both counts: nothing needed fixing, and the proposed change was
unnecessary. This is the intended behaviour of the trigger and of best-of-tree
selection, not a limitation.

Two things it does illustrate. First, a repair action will happily propose a
plausible-looking change on a state that is already correct, which is why the
tree keeps every node and returns the best rather than the last. Second, three
runs of the same command gave deltas of +0.0000, -0.0041 and -0.0062:
`revise_pipeline` is two nondeterministic gpt-5 calls, so single-task deltas of
this size carry no signal. Only delta's sign is usable, at 0.758 agreement.

The checkpoint's own `revise_pipeline` AUC is 0.543, near chance, so a genuine
limitation is expected somewhere — it just is not this task.

## Status

**Runs end to end.** Verified on `spider_05ce58d1` with the real ModernBERT
checkpoint: state loading from the upstream artefacts, chain replay, diagnosis,
localizer inference on MPS, all three actions, tree search, and the record.

Not yet exercised:

- Beaver-Prep and Synth-Bird through this module (only Synth-Spider so far)
- multi-task runs
- `revise_relational_plan` — the shipped checkpoint has three classes and no
  head for it, so it always ranks 0.0 and is reachable only through the breadth
  fallback order
- the `export_for_eval` path, and gold scoring per node
