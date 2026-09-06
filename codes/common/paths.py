"""Profile-input and per-module output path resolution.

A single dataset name is enough to run every stage:

    python -m table_discovery.column_retrieval --dataset Beaver-Prep

Every path can still be overridden explicitly, so nothing has to be copied or
duplicated on disk.

Default layout
--------------
Inputs (read-only, shipped with the benchmark):

    <repo>/datasets/<Dataset>/profiles/
        dev.json                    questions + gold tables + join keys
        dev_tables.json             table schemas
        dev_semantic_col_sim.json   column-name embedding similarity
        dev_uniqueness.json         per-column distinct ratio
        dev_jaccard.json            column-value containment

Outputs (everything this module writes):

    <repo>/results/table_discovery/offline_online/<Dataset>/
        dw_join_keys_g_domain.json      stage 0
        edge_conf_g_domain.json         stage 0
        column_embeddings.pt            stage 1 cache
        question_keywords.json          stage 1
        question_keywords_top{N}_columns.json   stage 1
        question_ranked_tables_only_C.json      stage 2
        question_ranked_tables_gated.json       stage 3
        exp_g_domain_{5,10,15}.json             stage 5 (final)
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path

# <repo>/codes/common/paths.py -> <repo>
REPO_ROOT = Path(__file__).resolve().parents[2]

DEFAULT_PROFILE_SUBDIR = "profiles"

# Each stage group writes under results/<module>/<group>/<Dataset>/.
DEFAULT_MODULE = "table_discovery"
DEFAULT_GROUP = "offline_online"

# Input files expected under the profile directory.
PROFILE_FILES = {
    "dev": "dev.json",
    "tables": "dev_tables.json",
    "semantic_col_sim": "dev_semantic_col_sim.json",
    "uniqueness": "dev_uniqueness.json",
    "jaccard": "dev_jaccard.json",
}


class Paths:
    """Resolved input/output locations for one dataset."""

    def __init__(self, dataset: str, profile_dir: Path, out_dir: Path):
        self.dataset = dataset
        self.profile_dir = Path(profile_dir)
        self.out_dir = Path(out_dir)

    # ---- inputs -------------------------------------------------------
    def profile(self, key: str) -> Path:
        """Path of one profiling input file, addressed by its short key."""
        return self.profile_dir / PROFILE_FILES[key]

    @property
    def dev(self) -> Path:
        return self.profile("dev")

    @property
    def tables(self) -> Path:
        return self.profile("tables")

    # ---- outputs ------------------------------------------------------
    def out(self, name: str) -> Path:
        """Path of one output artefact inside this dataset's result directory."""
        self.out_dir.mkdir(parents=True, exist_ok=True)
        return self.out_dir / name

    def question_topk_columns(self, kc_top_k: int) -> Path:
        return self.out(f"question_keywords_top{kc_top_k}_columns.json")

    # ---- diagnostics --------------------------------------------------
    def missing_inputs(self) -> list[str]:
        """Names of the profiling files that are required but absent."""
        return [f for f in PROFILE_FILES.values() if not (self.profile_dir / f).exists()]

    def describe(self) -> str:
        return (
            f"[paths] dataset={self.dataset}\n"
            f"[paths] profiles={self.profile_dir}\n"
            f"[paths] outputs ={self.out_dir}"
        )


def resolve(dataset: str, profile_dir: str | None = None,
            out_dir: str | None = None, module: str = DEFAULT_MODULE,
            group: str = DEFAULT_GROUP) -> Paths:
    """Resolve the profile and output directories for one dataset.

    Resolution order for each directory: explicit argument, then environment
    variable (PREPWEAVER_PROFILE_DIR / PREPWEAVER_TD_OUT_DIR), then the default
    in-repo layout documented at the top of this file.
    """
    prof = profile_dir or os.environ.get("PREPWEAVER_PROFILE_DIR")
    if prof is None:
        prof = REPO_ROOT / "datasets" / dataset / DEFAULT_PROFILE_SUBDIR

    out = out_dir or os.environ.get("PREPWEAVER_TD_OUT_DIR")
    if out is None:
        out = REPO_ROOT / "results" / module / group / dataset

    return Paths(dataset, Path(prof), Path(out))


def add_arguments(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    """Add the path arguments shared by every stage of this module."""
    parser.add_argument("--dataset", type=str, default="Beaver-Prep",
                        help="Dataset name, e.g. Beaver-Prep. Used to derive "
                             "both the profile and the output directory.")
    parser.add_argument("--profile-dir", type=str, default=None,
                        help="Override the directory holding dev.json and the "
                             "profiling files.")
    parser.add_argument("--out-dir", type=str, default=None,
                        help="Override the directory this stage writes to.")
    return parser


def from_args(args: argparse.Namespace, module: str = DEFAULT_MODULE,
              group: str = DEFAULT_GROUP) -> Paths:
    """Build a Paths object from parsed arguments, and report what was found."""
    p = resolve(args.dataset, args.profile_dir, args.out_dir,
                module=module, group=group)
    print(p.describe())
    missing = p.missing_inputs()
    if missing:
        print(f"[paths] WARNING missing profiling files: {missing}")
    return p
