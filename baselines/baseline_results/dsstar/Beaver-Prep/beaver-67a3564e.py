import pandas as pd
import re

# Source tables from the provided `tables` dict
moira = tables['table_1'].copy()            # MOIRA_LIST_DETAIL.pkl
students = tables['table_3'].copy()         # MIT_STUDENT_DIRECTORY.pkl
employees = tables['table_9'].copy()        # EMPLOYEE_DIRECTORY.pkl

# Helper functions to normalize identifiers
def extract_email_like(s: str) -> str | None:
    if not isinstance(s, str):
        return None
    s = s.strip()
    m = re.search(r'([A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,})', s)
    if m:
        return m.group(1).lower()
    token = re.sub(r'[<>()"]', ' ', s).split()
    if token:
        cand = token[-1]
        if re.fullmatch(r'[A-Za-z0-9._\-]+', cand):
            return f"{cand.lower()}@mit.edu"
    return None

def email_to_kerb(email: str | None) -> str | None:
    if not isinstance(email, str):
        return None
    return email.split('@')[0].lower()

# Normalize MOIRA list members to kerberos and email
moira = moira.copy()
moira['member_email_norm'] = moira['moira_list_member'].apply(extract_email_like)
moira['member_kerb'] = moira['member_email_norm'].apply(email_to_kerb)

# Normalize student directory identifiers
students = students.copy()
students['student_email_norm'] = students['EMAIL_ADDRESS'].astype(str).str.strip().str.lower()
students.loc[students['student_email_norm'].isin(['nan', 'none', '']), 'student_email_norm'] = None
students['student_kerb'] = students['student_email_norm'].apply(email_to_kerb)

# Normalize employee directory identifiers
employees = employees.copy()
employees['emp_email_norm'] = employees['EMAIL_ADDRESS'].astype(str).str.strip().str.lower()
employees.loc[employees['emp_email_norm'].isin(['nan', 'none', '']), 'emp_email_norm'] = None
if 'krb_name' in employees.columns:
    employees['krb_name'] = employees['krb_name'].astype(str).str.strip().str.lower()
else:
    employees['krb_name'] = None
employees['emp_kerb_from_email'] = employees['emp_email_norm'].apply(email_to_kerb)
employees['emp_kerb'] = employees['krb_name'].where(employees['krb_name'].notna() & (employees['krb_name'] != 'nan'), employees['emp_kerb_from_email'])

# Identify EECS department members
eecs_patterns = [
    r'\bEECS\b',
    r'\bElectrical\s*Engineering\b',
    r'\bComputer\s*Science\b',
    r'Electrical Engineering and Computer Science',
    r'EECS\s*-\s*Electrical Engineering and Computer Science',
]
eecs_regex = re.compile('|'.join(eecs_patterns), flags=re.IGNORECASE)

students['is_eecs_student'] = (
    students['DEPARTMENT_NAME'].astype(str).str.contains(eecs_regex, na=False) |
    students['DEPARTMENT'].astype(str).str.contains(eecs_regex, na=False)
)
employees['is_eecs_employee'] = employees['DEPARTMENT_NAME'].astype(str).str.contains(eecs_regex, na=False)

# Build lookup sets of kerbs for EECS students and employees
eecs_student_kerbs = set(students.loc[students['is_eecs_student'] & students['student_kerb'].notna(), 'student_kerb'])
eecs_employee_kerbs = set(employees.loc[employees['is_eecs_employee'] & employees['emp_kerb'].notna(), 'emp_kerb'])
eecs_kerbs = eecs_student_kerbs.union(eecs_employee_kerbs)

# Flag MOIRA members who are in EECS
moira['IS_EECS'] = moira['member_kerb'].isin(eecs_kerbs)

# Filter B* lists and count distinct EECS members per list
b_lists = moira.loc[moira['MOIRA_LIST_KEY'].astype(str).str.startswith(('b', 'B'))].copy()

# Only consider rows with a non-null kerberos and flagged as EECS
b_lists_eecs = b_lists.loc[b_lists['IS_EECS'] & b_lists['member_kerb'].notna(), ['MOIRA_LIST_KEY', 'member_kerb']].drop_duplicates()

# Count distinct EECS members per list
eecs_counts = b_lists_eecs.groupby('MOIRA_LIST_KEY', as_index=False).agg(distinct_eecs_members=('member_kerb', 'nunique'))

# Summary metrics
total_b_lists_with_eecs = int(eecs_counts.shape[0])

if not eecs_counts.empty:
    max_row = eecs_counts.sort_values(['distinct_eecs_members', 'MOIRA_LIST_KEY'], ascending=[False, True]).iloc[0]
    max_list_key = max_row['MOIRA_LIST_KEY']
    max_eecs_count = int(max_row['distinct_eecs_members'])
else:
    max_list_key = None
    max_eecs_count = 0

answer_df = pd.DataFrame([{
    'total_b_star_lists_with_at_least_one_eecs_member': total_b_lists_with_eecs,
    'b_star_list_with_max_eecs_members': max_list_key,
    'max_distinct_eecs_member_count': max_eecs_count
}])

# Final result mapping
result = {
    'b_lists_eecs_summary': answer_df
}