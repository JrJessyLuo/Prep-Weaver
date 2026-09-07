import pandas as pd

# Source tables from provided 'tables' dict
df_reserve = tables['table_1']  # LIBRARY_RESERVE_MATRL_DETAIL.pkl
df_instr = tables['table_7']    # LIBRARY_COURSE_INSTRUCTOR.pkl

# Reproduce the same logic as the reference code
cols_instr_keep = ["LIBRARY_COURSE_INSTRUCTOR_KEY", "COURSE_NAME", "INSTRUCTOR_NAME", "DEPARTMENT"]
df_joined = df_reserve.merge(df_instr[cols_instr_keep], on="LIBRARY_COURSE_INSTRUCTOR_KEY", how="left")

agg_df = (
    df_joined.groupby("DEPARTMENT", dropna=False)
    .agg(
        unique_courses_by_subject_id=("SUBJECT_ID", "nunique"),
        unique_courses_by_course_name=("COURSE_NAME", "nunique"),
        unique_reserved_materials=("LIBRARY_RESERVE_CATALOG_KEY", "nunique"),
        unique_instructors=("INSTRUCTOR_NAME", "nunique"),
        rows=("LIBRARY_COURSE_INSTRUCTOR_KEY", "size")
    )
    .reset_index()
    .sort_values(["unique_courses_by_subject_id", "unique_reserved_materials"], ascending=[False, False])
)

# Prepare final answer per question: department name, unique courses offered, unique reserved materials, unique instructors
final_df = agg_df.loc[:, [
    "DEPARTMENT",
    "unique_courses_by_subject_id",
    "unique_reserved_materials",
    "unique_instructors"
]].rename(columns={
    "DEPARTMENT": "department",
    "unique_courses_by_subject_id": "unique_courses_offered",
    "unique_reserved_materials": "unique_reserved_materials",
    "unique_instructors": "unique_instructors"
}).sort_values("unique_courses_offered", ascending=False)

# Assign to result dict as required
result = {
    "department_summary": final_df
}