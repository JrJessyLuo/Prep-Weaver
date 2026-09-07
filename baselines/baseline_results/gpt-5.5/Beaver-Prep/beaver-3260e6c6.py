import pandas as pd
import numpy as np
import re

target_list = "date-destiny"
target_dept = "Management"
target_list_norm = target_list.strip().lower()
target_dept_norm = target_dept.strip().lower()

def norm_series(s):
    return s.astype(str).str.strip().str.lower()

def col_priority(col):
    c = col.lower()
    p = 0
    if "list" in c:
        p += 5
    if "mail" in c or "email" in c:
        p += 3
    if c in {"name", "list_name", "email_list_name", "mailing_list_name"}:
        p += 4
    return p

# Find the table/column containing the requested email list name
list_candidates = []
for tname, df in tables.items():
    if df.empty:
        continue
    for col in df.columns:
        vals = norm_series(df[col])
        mask = vals.eq(target_list_norm)
        if mask.any():
            list_candidates.append((col_priority(col), tname, col, mask))

answer = None

if list_candidates:
    _, list_table_name, list_col, list_mask = sorted(list_candidates, reverse=True)[0]
    list_df = tables[list_table_name].copy()
    list_rows = list_df[list_mask].copy()

    # If the matching table is already an aggregated/list-by-department table, use it directly
    dept_cols = [
        c for c in list_df.columns
        if ("department" in c.lower() or "dept" in c.lower()) and "code" not in c.lower()
    ]
    count_cols = [
        c for c in list_df.columns
        if ("student" in c.lower() and any(k in c.lower() for k in ["num", "number", "count", "cnt"]))
        or any(k in c.lower() for k in ["student_count", "num_students", "number_of_students"])
    ]
    pct_cols = [
        c for c in list_df.columns
        if any(k in c.lower() for k in ["percent", "percentage", "pct"])
    ]

    if dept_cols and count_cols and pct_cols:
        dept_col = dept_cols[0]
        direct = list_rows[norm_series(list_rows[dept_col]).eq(target_dept_norm)].copy()
        if not direct.empty:
            count_col = count_cols[0]
            pct_col = pct_cols[0]
            pct = direct.iloc[0][pct_col]
            if isinstance(pct, str):
                pct = pct.strip().replace("%", "")
            answer = pd.DataFrame([{
                "list_name": target_list,
                "department_name": direct.iloc[0][dept_col],
                "number_of_students": int(pd.to_numeric(direct.iloc[0][count_col], errors="coerce")),
                "percentage_of_students": round(float(pd.to_numeric(pct, errors="coerce")), 2)
            }])

    if answer is None:
        students = tables["table_2"].copy()
        students["__email_norm"] = students["EMAIL_ADDRESS"].astype(str).str.strip().str.lower()
        students["__local_norm"] = students["__email_norm"].str.split("@").str[0]
        students["__dept_name_norm"] = students["DEPARTMENT_NAME"].astype(str).str.strip().str.lower()
        students["__dept_code_norm"] = students["DEPARTMENT"].astype(str).str.strip().str.lower()

        student_emails = set(students["__email_norm"].dropna())
        student_locals = set(students["__local_norm"].dropna())

        member_rows = list_rows.copy()

        # If list metadata is separate from membership, try to find a linked membership table
        key_cols = [
            c for c in list_rows.columns
            if c != list_col and any(k in c.lower() for k in ["id", "key", "list"])
        ]
        key_vals = set()
        for c in key_cols:
            key_vals.update(
                list_rows[c].dropna().astype(str).str.strip().tolist()
            )
        key_vals.add(target_list)

        linked = []
        for tname, df in tables.items():
            if tname == list_table_name or df.empty:
                continue
            for c in df.columns:
                cl = c.lower()
                if "list" in cl or c in key_cols:
                    m = df[c].astype(str).str.strip().isin(key_vals)
                    if m.any():
                        linked.append((m.sum(), tname, c, m))
        if linked:
            _, mem_table_name, _, mem_mask = sorted(linked, reverse=True)[0]
            member_rows = tables[mem_table_name][mem_mask].copy()

        # Identify member columns
        candidate_member_cols = []
        for c in member_rows.columns:
            cl = c.lower()
            if c == list_col:
                continue
            if "list" in cl and not any(k in cl for k in ["member", "subscriber", "recipient"]):
                continue
            if (
                "email" in cl
                or "member" in cl
                or "subscriber" in cl
                or "recipient" in cl
                or "principal" in cl
                or "kerberos" in cl
                or "krb" in cl
                or "login" in cl
                or "username" in cl
                or cl == "user"
                or "mit_id" in cl
            ):
                candidate_member_cols.append(c)

        # Fallback: columns whose values overlap student emails/local parts
        if not candidate_member_cols:
            for c in member_rows.columns:
                if c == list_col:
                    continue
                vals = set(norm_series(member_rows[c]).dropna())
                if vals & student_emails or vals & student_locals:
                    candidate_member_cols.append(c)

        member_emails = set()
        member_locals = set()
        member_mitids = set()

        for c in candidate_member_cols:
            for val in member_rows[c].dropna():
                if isinstance(val, (list, tuple, set)):
                    pieces = list(val)
                else:
                    text = str(val).strip()
                    pieces = re.split(r"[;,\n\r\t ]+", text) if re.search(r"[@;,\n\r\t ]", text) else [text]

                for piece in pieces:
                    token = str(piece).strip().strip("<>()[]{}'\"").lower()
                    if not token or token == target_list_norm:
                        continue
                    if "@" in token:
                        member_emails.add(token)
                        member_locals.add(token.split("@", 1)[0])
                    elif re.fullmatch(r"\d{6,12}", token):
                        member_mitids.add(int(token))
                    elif re.fullmatch(r"[a-z0-9._%+\-]+", token):
                        member_locals.add(token)

        # Map MIT IDs to emails if needed
        if member_mitids and "table_3" in tables and {"MIT_ID", "EMAIL_ADDRESS"}.issubset(tables["table_3"].columns):
            people = tables["table_3"][["MIT_ID", "EMAIL_ADDRESS"]].dropna().copy()
            people = people[people["MIT_ID"].isin(member_mitids)]
            mapped_emails = people["EMAIL_ADDRESS"].astype(str).str.strip().str.lower()
            member_emails.update(mapped_emails)
            member_locals.update(mapped_emails.str.split("@").str[0])

        matched_students = students[
            students["__email_norm"].isin(member_emails)
            | students["__local_norm"].isin(member_locals)
        ].copy()

        matched_students = matched_students.drop_duplicates(subset=["__email_norm"])

        total_students = len(matched_students)
        management_students = matched_students[
            matched_students["__dept_name_norm"].eq(target_dept_norm)
            | matched_students["__dept_code_norm"].eq("15")
        ]

        num_management = len(management_students)
        pct_management = round((num_management / total_students * 100), 2) if total_students else 0.00

        answer = pd.DataFrame([{
            "list_name": target_list,
            "department_name": target_dept,
            "number_of_students": num_management,
            "percentage_of_students": pct_management
        }])
else:
    answer = pd.DataFrame(columns=[
        "list_name",
        "department_name",
        "number_of_students",
        "percentage_of_students"
    ])

result = {"date_destiny_management_students": answer}
