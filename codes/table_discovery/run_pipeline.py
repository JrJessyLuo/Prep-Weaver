"""Run the whole table-discovery pipeline for one dataset.

    python -m table_discovery.run_pipeline --dataset Beaver-Prep

Stages, in order:

    0  build_join_graph      offline, no LLM, no embedding
    1  column_retrieval      LLM (keyphrases) + local sentence encoder
    2  table_rerank          pure aggregation, no model
    3  llm_disambiguation    LLM, only for the questions the gate routes
    4  expand_compare        pure graph search, no model

Use --stages to run a subset, e.g. --stages 0 2 4 to skip everything that
calls an LLM, and --limit to bound the number of questions in stage 1.
"""

from __future__ import annotations

import argparse

from common import paths as P


def parse_args():
    parser = argparse.ArgumentParser(description="Run the table-discovery pipeline.")
    P.add_arguments(parser)
    parser.add_argument("--stages", type=int, nargs="+", default=[0, 1, 2, 3, 4],
                        choices=[0, 1, 2, 3, 4],
                        help="Stages to run, in the given order.")
    parser.add_argument("--top-k", type=int, default=100,
                        help="Columns retrieved per keyphrase (stages 1 and 2 must agree).")
    parser.add_argument("--top-table-k", type=int, default=50,
                        help="Candidate tables kept per question in stage 2.")
    parser.add_argument("--limit", type=int, default=0,
                        help="Stage 1 only: process the first N questions (0 = all).")
    parser.add_argument("--embedding-model", type=str, default="WhereIsAI/UAE-Large-V1")
    parser.add_argument("--keyword-llm-model", type=str, default="gpt-4.1",
                        help="LLM for stage 1 keyphrase extraction.")
    parser.add_argument("--prune-llm-model", type=str, default="gpt-5.2",
                        help="LLM for stage 3 distractor pruning.")
    parser.add_argument("--graph-name", type=str, default="g_domain")
    return parser.parse_args()


def main():
    a = parse_args()
    paths = P.from_args(a)

    if 0 in a.stages:
        print("\n########## stage 0: join graph ##########")
        from .build_join_graph import build_join_graph
        build_join_graph(paths)

    if 1 in a.stages:
        print("\n########## stage 1: keyphrase -> column retrieval ##########")
        from .column_retrieval import build_keyword_column_similarity
        build_keyword_column_similarity(
            paths,
            embedding_model_name=a.embedding_model,
            llm_model=a.keyword_llm_model,
            top_k=a.top_k,
            limit=a.limit,
        )

    if 2 in a.stages:
        print("\n########## stage 2: table ranking ##########")
        from .table_rerank import rank_tables_for_questions
        rank_tables_for_questions(
            question_topk_columns_path=str(paths.question_topk_columns(a.top_k)),
            table_schema_path=str(paths.tables),
            out_dir=str(paths.out_dir),
            top_col_k=a.top_k,
            top_table_k=a.top_table_k,
        )

    if 3 in a.stages:
        print("\n########## stage 3: gated LLM disambiguation ##########")
        from .llm_disambiguation import run_disambiguation
        run_disambiguation(paths, kc_top_k=a.top_k, llm_model=a.prune_llm_model)

    if 4 in a.stages:
        print("\n########## stages 4-5: expansion + voting ##########")
        from .expand_compare import select_tables
        select_tables(paths, graph_name=a.graph_name)

    print(f"\nDone. All artefacts are under: {paths.out_dir}")


if __name__ == "__main__":
    main()
