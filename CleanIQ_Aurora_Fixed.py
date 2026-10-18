import streamlit as st

import pandas as pd
import re
import hashlib
import plotly.express as px

from io import BytesIO

# ============================================================

# CleanIQ - AI-Powered Data Quality & Cleaning Assistant

# ============================================================

st.set_page_config(

    page_title="CleanIQ",

    page_icon="🧹",

    layout="wide"

)

# ============================================================
# Aurora Analytics design system (presentation only; cleaning logic below is preserved)
# ============================================================
st.markdown("""
<style>
:root { --ciq-ink:#17233d; --ciq-muted:#68758e; --ciq-line:#e6eaf3; --ciq-violet:#7568e8; --ciq-teal:#27b6ad; }
.stApp { background: radial-gradient(ellipse at 10% 0%, rgba(117,104,232,.09), transparent 36%), radial-gradient(ellipse at 90% 0%, rgba(39,182,173,.08), transparent 30%), #f6f8fc; color:var(--ciq-ink); }
[data-testid="stHeader"] { background:rgba(246,248,252,.88); }
.block-container { max-width: 1500px; padding-top: 2.25rem; padding-bottom: 3rem; }
[data-testid="stSidebar"] { background:linear-gradient(180deg,#f0efff 0%,#f8faff 54%,#effaf9 100%); border-right:1px solid #e2e6f2; }
[data-testid="stSidebar"] .block-container { padding-top:1.4rem; }
[data-testid="stMetric"] { background:rgba(255,255,255,.94); border:1px solid var(--ciq-line); padding:16px 18px; border-radius:16px; box-shadow:0 5px 20px rgba(30,45,80,.045); }
[data-testid="stMetricLabel"] { color:var(--ciq-muted); font-weight:600; }
[data-testid="stMetricValue"] { color:var(--ciq-ink); font-weight:750; }
[data-testid="stVerticalBlockBorderWrapper"] { border-radius:16px; }
.stButton > button, .stDownloadButton > button { border-radius:10px; border:1px solid #d8dff0; font-weight:650; transition:all .15s ease; }
.stButton > button[kind="primary"] { background:linear-gradient(110deg,#7568e8,#5d8de8); border:0; color:white; }
.stButton > button:hover, .stDownloadButton > button:hover { border-color:#8b83eb; color:#5549c8; }
[data-testid="stDataFrame"], [data-testid="stTable"] { border:1px solid var(--ciq-line); border-radius:12px; overflow:hidden; }
[data-testid="stTabs"] button { font-weight:650; }
h1,h2,h3 { color:var(--ciq-ink); letter-spacing:-.025em; }
hr { border-color:var(--ciq-line); }
.ciq-hero { padding:26px 30px; margin-bottom:18px; border:1px solid rgba(218,223,244,.95); border-radius:22px; background:linear-gradient(115deg,rgba(255,255,255,.98),rgba(246,246,255,.96) 54%,rgba(237,252,250,.96)); box-shadow:0 12px 36px rgba(38,51,88,.065); position:relative; overflow:hidden; }
.ciq-hero:after { content:''; position:absolute; width:190px; height:190px; right:-45px; top:-75px; border-radius:50%; background:linear-gradient(135deg,rgba(117,104,232,.18),rgba(39,182,173,.16)); }
.ciq-eyebrow { color:#6c63d8; text-transform:uppercase; font-size:11px; font-weight:800; letter-spacing:.16em; }
.ciq-title { color:#17233d; font-size:34px; line-height:1.2; font-weight:800; letter-spacing:-.04em; margin:7px 0 8px; }
.ciq-subtitle { color:#68758e; font-size:15px; max-width:800px; margin:0; }
.ciq-pill { display:inline-block; padding:6px 10px; margin-top:14px; border:1px solid #dcdafa; border-radius:999px; color:#5e55c7; background:#f4f2ff; font-size:12px; font-weight:700; }
.ciq-nav-label { color:#6e7890; font-size:10px; font-weight:800; letter-spacing:.15em; text-transform:uppercase; margin:15px 0 7px; }
.ciq-brand { font-size:20px; font-weight:850; letter-spacing:-.04em; color:#202c49; }
.ciq-brand span { color:#7568e8; }
.ciq-nav a { display:block; padding:8px 10px; margin:3px 0; color:#45516d; text-decoration:none; border-radius:9px; font-size:13px; font-weight:650; }
.ciq-nav a:hover { background:rgba(117,104,232,.10); color:#594fd0; }
.ciq-note { font-size:12px; color:#758099; line-height:1.55; padding:12px; border-radius:12px; background:rgba(255,255,255,.65); border:1px solid #e4e8f2; }
@media (max-width: 800px) { .ciq-title {font-size:27px;} .ciq-hero {padding:20px;} }
</style>
<div class="ciq-hero">
  <div class="ciq-eyebrow">DATA QUALITY WORKSPACE</div>
  <div class="ciq-title">CleanIQ <span style="color:#7568e8">✦</span></div>
  <p class="ciq-subtitle">AI-powered data quality and cleaning assistant. Profile your data, review suggested fixes, approve changes, and validate every result.</p>
  <span class="ciq-pill">✦ Aurora Analytics · Human-in-the-loop</span>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown('<div class="ciq-brand">✦ Clean<span>IQ</span></div>', unsafe_allow_html=True)
    st.caption("A clearer view of your data")
    st.markdown('<div class="ciq-nav-label">WORKSPACE</div><div class="ciq-nav">'
                '<a href="#upload-dataset">↥ &nbsp; Upload dataset</a>'
                '<a href="#dataset-preview">▤ &nbsp; Data preview</a>'
                '<a href="#dataset-profile">◫ &nbsp; Dataset profile</a>'
                '<a href="#quality-issues">⚑ &nbsp; Quality issues</a>'
                '<a href="#cleaning-recommendations">✧ &nbsp; Recommendations</a>'
                '<a href="#cleaning-proposal">⌁ &nbsp; Cleaning proposal</a>'
                '<a href="#human-approval">✓ &nbsp; Human approval</a>'
                '<a href="#audit-log">≡ &nbsp; Audit log</a>'
                '<a href="#validation">◉ &nbsp; Validation</a>'
                '<a href="#downloads">↓ &nbsp; Downloads</a></div>', unsafe_allow_html=True)
    st.markdown('<div class="ciq-nav-label">PRINCIPLE</div><div class="ciq-note">Changes stay under your control. CleanIQ proposes; you decide. Missing values and records are never silently invented or deleted.</div>', unsafe_allow_html=True)

st.info("🛡️ Human control is enabled: review proposed changes before applying them. Missing values and records are not automatically invented or deleted.")

# ============================================================

# Helper Functions

# ============================================================

def get_id_columns(dataframe):

    """Detect likely ID/business-key columns."""

    return [

        col for col in dataframe.columns

        if (

            col.lower().endswith("_id")

            or col.lower().endswith(" id")

            or col.lower() == "id"

            or col.lower().endswith("id")

        )

    ]

def parse_date_safely(value):
    """Parse common date formats without flipping year-first dates."""
    if pd.isna(value):
        return pd.NaT
    # Keep actual date/datetime values as dates.
    if isinstance(value, (pd.Timestamp,)):
        return value
    text = str(value).strip()
    if not text:
        return pd.NaT

    # ISO/year-first values must be parsed year-first, never day-first.
    if re.fullmatch(r"\d{4}[-/]\d{1,2}[-/]\d{1,2}", text):
        normalized = text.replace("/", "-")
        return pd.to_datetime(normalized, format="%Y-%m-%d", errors="coerce")

    # Common day-first formats used in the sample data.
    for fmt in ("%d/%m/%Y", "%d-%m-%Y", "%d/%m/%y", "%d-%m-%y"):
        parsed = pd.to_datetime(text, format=fmt, errors="coerce")
        if pd.notna(parsed):
            return parsed

    # Conservative fallback for other day-first date strings.
    return pd.to_datetime(text, dayfirst=True, errors="coerce")


def get_date_columns(dataframe):

    """Detect likely date columns from column names."""

    date_keywords = ["date", "time", "timestamp"]

    return [

        col for col in dataframe.columns

        if any(keyword in col.lower() for keyword in date_keywords)

    ]

def count_nonstandard_date_columns(dataframe, date_columns):
    """Count date columns with invalid or non-ISO text values.

    Correctly standardized YYYY-MM-DD strings are accepted; object dtype alone
    is not treated as a data-quality issue.
    """
    issue_count = 0
    for col in date_columns:
        has_issue = False
        for value in dataframe[col].dropna():
            if isinstance(value, str):
                text = value.strip()
                if not text:
                    continue
                parsed = parse_date_safely(text)
                if pd.isna(parsed) or text != parsed.strftime("%Y-%m-%d"):
                    has_issue = True
                    break
        if has_issue:
            issue_count += 1
    return issue_count


def count_whitespace_issues(dataframe, text_columns):

    count = 0

    for col in text_columns:

        count += dataframe[col].apply(

            lambda value: isinstance(value, str) and value != value.strip()

        ).sum()

    return int(count)

def calculate_quality_score(dataframe):

    """Transparent rule-based quality score."""

    total_missing = int(dataframe.isnull().sum().sum())

    total_duplicates = int(dataframe.duplicated().sum())

    id_columns = get_id_columns(dataframe)

    date_columns = get_date_columns(dataframe)

    total_duplicate_ids = 0

    for col in id_columns:

        # Missing IDs are missing values, not repeated business keys.
        non_missing_ids = dataframe[col].dropna()
        total_duplicate_ids += int(non_missing_ids.duplicated().sum())

    nonstandard_date_columns = count_nonstandard_date_columns(
        dataframe, date_columns
    )

    text_columns = dataframe.select_dtypes(

        include=["object", "string"]

    ).columns

    whitespace_issues = count_whitespace_issues(

        dataframe,

        text_columns

    )

    score = 100

    missing_penalty = min(total_missing * 1, 30)

    duplicate_id_penalty = min(total_duplicate_ids * 5, 20)

    duplicate_row_penalty = min(total_duplicates * 3, 15)

    date_penalty = min(nonstandard_date_columns * 5, 15)

    whitespace_penalty = min(whitespace_issues * 1, 10)

    score -= missing_penalty

    score -= duplicate_id_penalty

    score -= duplicate_row_penalty

    score -= date_penalty

    score -= whitespace_penalty

    return max(score, 0)

def to_excel(dataframe):

    """Create an Excel file in memory for download."""

    output = BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:

        dataframe.to_excel(

            writer,

            index=False,

            sheet_name="Cleaned_Data"

        )

    return output.getvalue()

# ============================================================

def safe_dataframe_for_display(dataframe):
    """Make mixed Python types in object columns safe for display only."""
    display_df = dataframe.copy()
    for column in display_df.columns:
        if display_df[column].dtype == "object":
            types_present = {type(value) for value in display_df[column].dropna()}
            if len(types_present) > 1:
                display_df[column] = display_df[column].map(
                    lambda value: str(value) if pd.notna(value) else pd.NA
                ).astype("string")
    return display_df


# File Upload

# ============================================================

st.markdown('<div id="upload-dataset"></div>', unsafe_allow_html=True)

uploaded_file = st.file_uploader(

    "Choose your dataset",

    type=["csv", "xlsx"]

)

# ============================================================

# Process Uploaded File

# ============================================================

if uploaded_file is not None:

    # Tie approval state to the exact uploaded file so decisions from an older
    # dataset can never leak into a different upload.
    dataset_fingerprint = hashlib.sha256(
        uploaded_file.getvalue()
    ).hexdigest()[:16]

    try:

        if uploaded_file.name.lower().endswith(".csv"):

            df = pd.read_csv(uploaded_file)

        elif uploaded_file.name.lower().endswith(".xlsx"):

            df = pd.read_excel(uploaded_file)

        else:

            st.error("Unsupported file type.")

            st.stop()

    except Exception as error:

        st.error(f"Could not read the file: {error}")

        st.stop()

    st.success("File uploaded successfully!")

    # ========================================================

    # Dataset Preview

    # ========================================================

    st.markdown('<div id="dataset-preview"></div>', unsafe_allow_html=True)

    st.subheader("📊 Dataset Preview")

    st.dataframe(
        safe_dataframe_for_display(df),
        width="stretch"
    )

    # ========================================================

    # Dataset Profile

    # ========================================================

    st.markdown('<div id="dataset-profile"></div>', unsafe_allow_html=True)

    st.subheader("🔍 Dataset Profile")

    total_rows = df.shape[0]

    total_columns = df.shape[1]

    total_missing = int(df.isnull().sum().sum())

    total_duplicates = int(df.duplicated().sum())

    id_columns = get_id_columns(df)

    date_columns = get_date_columns(df)

    total_duplicate_ids = 0

    for col in id_columns:

        total_duplicate_ids += int(df[col].dropna().duplicated().sum())

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Rows", total_rows)

    col2.metric("Columns", total_columns)

    col3.metric("Missing Values", total_missing)

    col4.metric("Duplicate Rows", total_duplicates)

    if id_columns:

        st.write(

            "Detected ID / business-key columns:",

            ", ".join(id_columns)

        )

        if total_duplicate_ids > 0:

            st.warning(

                f"Duplicate values detected across ID columns: "

                f"{total_duplicate_ids}"

            )

    # ========================================================

    # Column Quality Analysis

    # ========================================================

    st.subheader("📋 Column Quality Analysis")

    column_analysis = pd.DataFrame({

        "Column": df.columns,

        "Data Type": df.dtypes.astype(str).values,

        "Missing": df.isnull().sum().values,

        "Missing %": (

            df.isnull().sum().values / len(df) * 100

        ).round(2),

        "Unique Values": df.nunique().values

    })

    st.dataframe(

        column_analysis,

        width="stretch"

    )

    # Quick visual overview: only show columns that actually have missing values.
    missing_chart_data = column_analysis.loc[
        column_analysis["Missing"] > 0, ["Column", "Missing"]
    ].set_index("Column")
    if not missing_chart_data.empty:
        st.markdown("#### 📊 Missing Values by Column")
        missing_plot = missing_chart_data.reset_index()
        missing_plot.columns = ["Column", "Missing"]
        missing_fig = px.bar(missing_plot, x="Missing", y="Column", orientation="h",
                             color_discrete_sequence=["#7568E8"])
        missing_fig.update_layout(template="plotly_white", height=max(320, 30 * len(missing_plot)),
                                  margin=dict(l=10, r=20, t=15, b=10), font=dict(color="#17233D"),
                                  paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        missing_fig.update_traces(marker_line_width=0)
        st.plotly_chart(missing_fig, use_container_width=True)

    # Additional dashboard visual: compare major quality issue categories.
    issue_counts = {
        "Missing cells": int(df.isnull().sum().sum()),
        "Exact duplicate rows": int(df.duplicated().sum()),
        "Duplicate ID values": int(total_duplicate_ids),
        "Whitespace issues": int(count_whitespace_issues(
            df, df.select_dtypes(include=["object", "string"]).columns
        )),
        "Non-standard date columns": count_nonstandard_date_columns(
            df, date_columns
        ),
    }
    issue_chart_data = pd.DataFrame({
        "Issue type": list(issue_counts.keys()),
        "Count": list(issue_counts.values()),
    }).set_index("Issue type")
    st.markdown("#### 🧭 Data Quality Issues by Type")
    issue_plot = issue_chart_data.reset_index()
    issue_plot.columns = ["Issue type", "Count"]
    issue_palette = {"Missing cells": "#7568E8", "Exact duplicate rows": "#263B63",
                     "Duplicate ID values": "#27B6AD", "Whitespace issues": "#5D8DE8",
                     "Non-standard date columns": "#9A91F0"}
    issue_fig = px.bar(issue_plot, x="Count", y="Issue type", orientation="h",
                       color="Issue type", color_discrete_map=issue_palette,
                       category_orders={"Issue type": list(issue_counts.keys())[::-1]})
    issue_fig.update_layout(template="plotly_white", height=330, showlegend=False,
                            margin=dict(l=10, r=20, t=15, b=10), font=dict(color="#17233D"),
                            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    issue_fig.update_traces(marker_line_width=0)
    st.plotly_chart(issue_fig, use_container_width=True)

    # ========================================================

    # Data Quality Issues

    # ========================================================

    st.markdown('<div id="quality-issues"></div>', unsafe_allow_html=True)

    st.subheader("🚨 Data Quality Issues")

    issues_found = False

    missing_columns = (

        df.columns[df.isnull().any()].tolist()

    )

    if missing_columns:

        issues_found = True

        st.warning(

            f"Missing values found in {len(missing_columns)} "

            f"columns: {', '.join(missing_columns)}"

        )

    for col in id_columns:

        duplicate_count = int(df[col].duplicated().sum())

        if duplicate_count > 0:

            issues_found = True

            st.error(

                f"Duplicate values detected in {col}: "

                f"{duplicate_count} duplicate record(s)."

            )

    for col in date_columns:
        if count_nonstandard_date_columns(df, [col]) > 0:
            issues_found = True
            st.warning(
                f"{col} contains invalid or non-standard date text. "
                "Expected YYYY-MM-DD after standardization."
            )

    text_columns = df.select_dtypes(

        include=["object", "string"]

    ).columns

    whitespace_issues = count_whitespace_issues(

        df,

        text_columns

    )

    if whitespace_issues > 0:

        issues_found = True

        st.warning(

            f"{whitespace_issues} unnecessary whitespace issue(s) "

            f"detected in text fields."

        )

    if not issues_found:

        st.success("No obvious data quality issues detected.")

    # ========================================================

    # Cleaning Recommendations

    # ========================================================

    st.markdown('<div id="cleaning-recommendations"></div>', unsafe_allow_html=True)

    st.subheader("💡 Cleaning Recommendations")

    if missing_columns:

        st.info(

            "Missing values detected. Review each missing field "

            "before filling or removing values."

        )

        for col in missing_columns:

            missing_count = int(df[col].isnull().sum())

            if col == "Total_Sales":

                st.write(

                    f"**{col}:** {missing_count} missing value(s). "

                    "Consider recalculating from Quantity × Unit_Price "

                    "if those fields are available."

                )

            elif col == "Email":

                st.write(

                    f"**{col}:** {missing_count} missing value(s). "

                    "Check the original source rather than inventing "

                    "an email."

                )

            else:

                st.write(

                    f"**{col}:** {missing_count} missing value(s). "

                    "Review the original record before filling or "

                    "removing the value."

                )

    for col in id_columns:

        duplicate_count = int(df[col].duplicated().sum())

        if duplicate_count > 0:

            st.write(

                f"**{col}:** {duplicate_count} duplicate value(s) "

                "detected. Review the affected records before "

                "removing anything."

            )

    for col in date_columns:
        if count_nonstandard_date_columns(df, [col]) > 0:
            st.write(
                f"**{col}:** This column contains invalid or non-standard "
                "date text. CleanIQ can propose standardization after "
                "checking whether the source format is unambiguous."
            )

    if whitespace_issues > 0:

        st.write(

            f"**Text fields:** {whitespace_issues} whitespace issue(s) "

            "can be safely proposed for trimming."

        )

    # ========================================================

    # Data Quality Score

    # ========================================================

    st.subheader("📊 Data Quality Score")

    score = calculate_quality_score(df)

    st.metric(

        "Data Quality Score",

        f"{score}/100"

    )

    st.caption(

        "Score is rule-based and transparent. Missing values, duplicate "

        "business keys, exact duplicate rows, non-standard date values, "

        "and unnecessary whitespace contribute to the score."

    )

    # ========================================================

    # Cleaning Proposal

    # ========================================================

    st.markdown('<div id="cleaning-proposal"></div>', unsafe_allow_html=True)

    st.subheader("🧹 Cleaning Proposal")

    proposed_df = df.copy()

    text_columns = proposed_df.select_dtypes(

        include=["object", "string"]

    ).columns

    proposed_changes = []

    # --------------------------------------------------------

    # Rule 1: Trim unnecessary spaces

    # --------------------------------------------------------

    for index in df.index:

        for col in text_columns:

            before = df.loc[index, col]

            if isinstance(before, str):

                after = before.strip()

                if before != after:

                    proposed_df.loc[index, col] = after

                    proposed_changes.append({

                        "Row": int(df.index.get_loc(index)) + 1,

                        "Column": col,

                        "Before": before,

                        "After": after,

                        "Action": "TRIM_SPACES",

                        "Risk": "LOW",

                        "Reason": "Removed leading/trailing spaces"

                    })

    # --------------------------------------------------------
    # Rule 2: Propose median imputation for missing numeric values.
    # Only suggest a value when the column has observed numeric data.
    # The user must approve every proposed fill; categorical fields remain for review.
    # --------------------------------------------------------

    for col in df.columns:
        # Treat both true nulls and blank/whitespace-only strings as missing.
        text_values = df[col].astype("string").str.strip()
        missing_mask = df[col].isna() | text_values.eq("").fillna(False)
        observed_raw = df.loc[~missing_mask, col]
        numeric_observed = pd.to_numeric(observed_raw, errors="coerce")
        # Infer numeric columns from non-blank values, not from blanks. This is
        # the key fix for Excel columns imported as object/string because of blanks.
        is_numeric_column = (
            pd.api.types.is_numeric_dtype(df[col])
            or (
                not observed_raw.empty
                and numeric_observed.notna().all()
            )
        )
        # Total_Sales is commonly a derived business metric. When its source
        # fields exist, do not independently median-fill it: that can produce
        # values inconsistent with Quantity * Unit_Price. Leave it for review.
        is_derived_sales = (
            str(col).strip().lower() == "total_sales"
            and {"quantity", "unit_price"}.issubset(
                {str(existing).strip().lower() for existing in df.columns}
            )
        )
        if is_numeric_column and missing_mask.any() and not is_derived_sales:
            observed = numeric_observed.dropna()
            if not observed.empty:
                fill_value = float(observed.median())
                if float(fill_value).is_integer():
                    fill_value = int(fill_value)
                for index in df.index[missing_mask]:
                    proposed_changes.append({
                        "Row": int(df.index.get_loc(index)) + 1,
                        "Column": col,
                        "Before": "<MISSING>",
                        "After": fill_value,
                        "Action": "IMPUTE_MEDIAN",
                        "Risk": "MEDIUM",
                        "Reason": f"Median-based numeric fill suggestion ({fill_value}); review suitability before approval"
                    })

    # --------------------------------------------------------
    # Rule 2b: Normalize capitalization for common categorical fields.
    # These are suggestions requiring the same human approval as other changes.
    # --------------------------------------------------------
    case_columns = {
        "city": str.title,
        "category": str.title,
        "status": str.title,
    }
    for col in df.columns:
        normalizer = case_columns.get(str(col).strip().lower())
        if normalizer is None:
            continue
        for index, before in df[col].items():
            if not isinstance(before, str) or not before.strip():
                continue
            # Keep this operation independent from TRIM_SPACES: changing case
            # must not silently remove spaces if the trim proposal is rejected.
            after = normalizer(before)
            if before != after:
                proposed_changes.append({
                    "Row": int(df.index.get_loc(index)) + 1,
                    "Column": col,
                    "Before": before,
                    "After": after,
                    "Action": "STANDARDIZE_CASE",
                    "Risk": "LOW",
                    "Reason": "Suggested consistent capitalization for a recognized categorical field"
                })

    # --------------------------------------------------------

    # Rule 3: Standardize parseable date columns

    # --------------------------------------------------------

    for col in date_columns:

        non_null_values = df[col].dropna()

        if len(non_null_values) == 0:

            continue

        try:
            parsed_dates = non_null_values.map(parse_date_safely)
            invalid_count = int(parsed_dates.isna().sum())

            # Only propose standardization if every non-empty value can be
            # interpreted safely. Never guess when a value is ambiguous/unparseable.
            if invalid_count == 0:
                for index in non_null_values.index:
                    before = df.loc[index, col]
                    parsed_value = parse_date_safely(before)

                    if pd.notna(parsed_value):
                        after = parsed_value.strftime("%Y-%m-%d")
                        if str(before).strip() != after:
                            proposed_df.loc[index, col] = after
                            proposed_changes.append({
                                "Row": int(df.index.get_loc(index)) + 1,
                                "Column": col,
                                "Before": before,
                                "After": after,
                                "Action": "STANDARDIZE_DATE",
                                "Risk": "MEDIUM",
                                "Reason": "Converted parseable date to YYYY-MM-DD while preserving year-first dates"
                            })
        except Exception:
            st.info(
                f"Date standardization was not proposed for {col} "
                "because the values could not be safely interpreted."
            )

    # ========================================================

    # Preview Cleaning Button

    # ========================================================

    if "preview_cleaning" not in st.session_state:

        st.session_state.preview_cleaning = False

    if st.button("🔍 Preview Cleaning"):

        st.session_state.preview_cleaning = True

    # ========================================================

    # Show Proposed Changes

    # ======# Individual Human Approval==================================================

    if st.session_state.preview_cleaning:

        st.subheader("📊 Before vs After")

        if proposed_changes:

            changes_df = pd.DataFrame(proposed_changes)

            st.success(

                f"CleanIQ found {len(changes_df)} proposed change(s)."

            )
            imputation_count = int(changes_df["Action"].eq("IMPUTE_MEDIAN").sum())
            case_count = int(changes_df["Action"].eq("STANDARDIZE_CASE").sum())
            summary_col1, summary_col2, summary_col3 = st.columns(3)
            summary_col1.metric("Median fill suggestions", imputation_count)
            summary_col2.metric("Capitalization suggestions", case_count)
            summary_col3.metric("Total proposals", len(changes_df))
            if imputation_count == 0 and int(df.isna().sum().sum()) > 0:
                st.info("No median fills were proposed. Check whether missing values are in numeric columns with at least one valid numeric value; text fields are intentionally left for review.")

            st.dataframe(

                changes_df,

                width="stretch"

            )

            # =================================================

            # =================================================

            st.markdown('<div id="human-approval"></div>', unsafe_allow_html=True)

            st.subheader("✅ Human Approval")

            st.info(

                "Use bulk actions to decide on many changes at once. "

                "You can still override any decision individually below."

            )

            approval_key = f"cleaniq_decisions_{dataset_fingerprint}"

            if approval_key not in st.session_state:

                st.session_state[approval_key] = {}

            # Give every proposed change a stable decision key.

            for change_index in changes_df.index:

                if change_index not in st.session_state[approval_key]:

                    st.session_state[approval_key][change_index] = "Pending"

            # -------------------------------------------------

            # Bulk decision controls

            # -------------------------------------------------

            st.markdown("#### ⚡ Bulk decisions")

            st.caption(

                "Approve low-risk whitespace changes together. Medium-risk "

                "date changes can also be approved in bulk, but first verify "

                "that the source date format is unambiguous."

            )

            bulk_col1, bulk_col2, bulk_col3, bulk_col4 = st.columns(4)

            def apply_bulk_decision(change_indices, decision_value):

                for idx in change_indices:

                    st.session_state[approval_key][idx] = decision_value

                    widget_key = f"decision_{dataset_fingerprint}_{idx}"

                    # Set widget state before that selectbox is created on this run.

                    if widget_key in st.session_state:

                        st.session_state[widget_key] = decision_value

            low_risk_indices = changes_df.index[changes_df["Risk"].eq("LOW")].tolist()

            medium_risk_indices = changes_df.index[changes_df["Risk"].eq("MEDIUM")].tolist()

            pending_indices = [

                idx for idx in changes_df.index

                if st.session_state[approval_key].get(idx, "Pending") == "Pending"

            ]

            with bulk_col1:

                if st.button("Approve all LOW risk", width="stretch"):

                    apply_bulk_decision(low_risk_indices, "Approve")

                    st.rerun()

            with bulk_col2:

                if st.button("Approve all MEDIUM risk", width="stretch"):

                    apply_bulk_decision(medium_risk_indices, "Approve")

                    st.rerun()

            with bulk_col3:

                if st.button("Reject all pending", width="stretch"):

                    apply_bulk_decision(pending_indices, "Reject")

                    st.rerun()

            with bulk_col4:

                if st.button("Reset all", width="stretch"):

                    apply_bulk_decision(changes_df.index.tolist(), "Pending")

                    st.rerun()

            # -------------------------------------------------

            # Individual decision controls

            # -------------------------------------------------

            for change_index, change in changes_df.iterrows():

                st.markdown(

                    f"**Change {change_index + 1}: "

                    f"{change['Action']} — {change['Column']} "

                    f"(Risk: {change['Risk']})**"

                )

                # repr() makes invisible whitespace visible (e.g. 'mumbai ').
                st.write(
                    f"Row {change['Row']}: "
                    f"{change['Before']!r} → {change['After']!r}"
                )

                decision = st.selectbox(

                    "Decision",

                    ["Pending", "Approve", "Reject", "Review"],

                    index=[

                        "Pending",

                        "Approve",

                        "Reject",

                        "Review"

                    ].index(

                        st.session_state[approval_key][change_index]

                    ),

                    key=f"decision_{dataset_fingerprint}_{change_index}"

                )

                st.session_state[approval_key][change_index] = decision

                st.divider()

            # -------------------------------------------------

            # Build audit table from decisions

            # -------------------------------------------------

            changes_df["Decision"] = changes_df.index.map(

                st.session_state[approval_key]

            )

            st.subheader("📋 Decision Summary")

            st.dataframe(

                changes_df,

                width="stretch"

            )

            approved_changes = changes_df[

                changes_df["Decision"] == "Approve"

            ]

            rejected_changes = changes_df[

                changes_df["Decision"] == "Reject"

            ]

            review_changes = changes_df[

                changes_df["Decision"] == "Review"

            ]

            pending_changes = changes_df[

                changes_df["Decision"] == "Pending"

            ]

            st.write(

                f"Approved: **{len(approved_changes)}** | "

                f"Rejected: **{len(rejected_changes)}** | "

                f"Review: **{len(review_changes)}** | "

                f"Pending: **{len(pending_changes)}**"

            )

            # -------------------------------------------------

            # Apply only approved changes

            # -------------------------------------------------

            st.caption("Apply uses the original uploaded dataset as the baseline and applies every change currently marked Approve. Keep earlier approvals marked Approve if you want them included alongside later decisions.")
            if st.button("🚀 Apply Approved Changes"):

                if len(approved_changes) == 0:

                    st.warning(

                        "No changes are approved yet. "

                        "Approve at least one change before applying."

                    )

                elif len(pending_changes) > 0:

                    st.warning(

                        "Some changes are still pending. "

                        "Please decide on every proposed change first."

                    )

                else:

                    approved_df = df.copy()
                    # Track the proposals whose operations actually execute.
                    # This is separate from whether the final cell differs from
                    # its original value (another proposal may target the same cell).
                    applied_change_indices = set()
                    operation_results = {}

                    for change_index in approved_changes.index:

                        change = changes_df.loc[change_index]

                        row_number = int(change["Row"]) - 1

                        column = change["Column"]

                        action = change["Action"]

                        if action == "TRIM_SPACES":

                            approved_df.loc[

                                approved_df.index[row_number],

                                column

                            ] = str(

                                approved_df.loc[

                                    approved_df.index[row_number],

                                    column

                                ]

                            ).strip()

                        elif action == "STANDARDIZE_CASE":

                            approved_df.loc[
                                approved_df.index[row_number],
                                column
                            ] = str(approved_df.loc[approved_df.index[row_number], column]).title()

                        elif action == "STANDARDIZE_DATE":

                            approved_df.loc[

                                approved_df.index[row_number],

                                column

                            ] = change["After"]

                        elif action == "IMPUTE_MEDIAN":

                            # Convert numeric-looking text columns before filling,
                            # so the approved result is numeric in the exported file.
                            approved_df[column] = pd.to_numeric(
                                approved_df[column].replace(r"^\s*$", pd.NA, regex=True),
                                errors="coerce"
                            )
                            approved_df.loc[
                                approved_df.index[row_number],
                                column
                            ] = change["After"]

                        # Record the value immediately after this operation. This
                        # differs from the final cell value when multiple approved
                        # operations target the same cell.
                        operation_results[change_index] = repr(
                            approved_df.iloc[row_number][column]
                        )
                        applied_change_indices.add(change_index)

                    st.success(

                        f"{len(approved_changes)} approved change(s) applied."

                    )

                    # ------------------------------------------------

                    # Audit Log

                    # ------------------------------------------------

                    st.markdown('<div id="audit-log"></div>', unsafe_allow_html=True)

                    st.subheader("📋 Audit Log")

                    # Audit the user's decision separately from the actual result.
                    audit_log = changes_df.copy()
                    # Streamlit/PyArrow can fail when Before/After contain mixed
                    # values (for example strings plus numeric median proposals).
                    # Convert these display columns to consistent text for rendering.
                    audit_log["Before"] = audit_log["Before"].map(repr)
                    audit_log["After"] = audit_log["After"].map(repr)
                    audit_log["Original Value (visible)"] = audit_log["Before"]
                    audit_log["Proposed Value (visible)"] = audit_log["After"]
                    audit_log["Operation Result (visible)"] = audit_log.index.map(
                        lambda idx: operation_results.get(idx, "Not applied")
                    )
                    audit_log["Final Value (visible)"] = audit_log.apply(
                        lambda item: repr(approved_df.iloc[int(item["Row"]) - 1][item["Column"]]),
                        axis=1,
                    )
                    # Applied records whether this specific approved operation
                    # executed, not whether the cell's final value differs from
                    # its original value. This avoids misleading flags when
                    # multiple proposals target the same cell.
                    audit_log["Applied"] = audit_log.index.isin(
                        applied_change_indices
                    )

                    st.dataframe(audit_log, width="stretch")

                    # ------------------------------------------------

                    # Cleaning Summary

                    # ------------------------------------------------

                    st.subheader("📊 Cleaning Summary")

                    action_summary = (

                        approved_changes["Action"]

                        .value_counts()

                        .rename_axis("Action")

                        .reset_index(name="Changes")

                    )

                    st.dataframe(

                        action_summary,

                        width="stretch"

                    )

                    st.write(

                        f"Total changes approved: "

                        f"{len(approved_changes)}"

                    )

                    # ------------------------------------------------

                    # Cleaned Dataset

                    # ------------------------------------------------

                    st.subheader("🧹 Cleaned Dataset")

                    st.dataframe(
                         safe_dataframe_for_display(approved_df),
                         width="stretch"
                     )

                    # ------------------------------------------------

                    # Before vs After Validation

                    # ------------------------------------------------

                    st.markdown('<div id="validation"></div>', unsafe_allow_html=True)

                    st.subheader("📈 Before vs After Validation")

                    before_score = calculate_quality_score(df)

                    after_score = calculate_quality_score(approved_df)

                    before_missing = int(

                        df.isnull().sum().sum()

                    )

                    after_missing = int(

                        approved_df.isnull().sum().sum()

                    )

                    before_duplicates = int(

                        df.duplicated().sum()

                    )

                    after_duplicates = int(

                        approved_df.duplicated().sum()

                    )

                    before_whitespace = count_whitespace_issues(

                        df,

                        text_columns

                    )

                    after_text_columns = approved_df.select_dtypes(

                        include=["object", "string"]

                    ).columns

                    after_whitespace = count_whitespace_issues(

                        approved_df,

                        after_text_columns

                    )

                    validation_data = pd.DataFrame({

                        "Metric": [

                            "Data Quality Score",

                            "Missing Values",

                            "Exact Duplicate Rows",

                            "Whitespace Issues"

                        ],

                        "Before Cleaning": [

                            before_score,

                            before_missing,

                            before_duplicates,

                            before_whitespace

                        ],

                        "After Cleaning": [

                            after_score,

                            after_missing,

                            after_duplicates,

                            after_whitespace

                        ]

                    })

                    st.dataframe(

                        validation_data,

                        width="stretch"

                    )

                    # Keep score and issue-count charts separate because they use
                    # different scales and should not share one axis.
                    st.markdown("#### 📉 Quality Score Improvement")
                    score_plot = pd.DataFrame({
                    "Stage": ["Before cleaning", "After cleaning"],
                    "Quality score": [before_score, after_score],
                    })
                    score_fig = px.bar(score_plot, x="Stage", y="Quality score", color="Stage",
                    color_discrete_map={"Before cleaning": "#263B63", "After cleaning": "#27B6AD"},
                    range_y=[0, 100])
                    score_fig.update_layout(template="plotly_white", height=320, showlegend=False,
                    margin=dict(l=10, r=20, t=15, b=10), font=dict(color="#17233D"),
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
                    score_fig.update_traces(marker_line_width=0, texttemplate="%{y}", textposition="outside")
                    st.plotly_chart(score_fig, use_container_width=True)

                    st.markdown("#### 🔎 Issue Counts Before vs After")
                    issue_comparison = pd.DataFrame({
                    "Issue": ["Missing cells", "Exact duplicate rows", "Whitespace issues"] * 2,
                    "Count": [before_missing, before_duplicates, before_whitespace,
                    after_missing, after_duplicates, after_whitespace],
                    "Stage": ["Before cleaning"] * 3 + ["After cleaning"] * 3,
                    })
                    comparison_fig = px.bar(issue_comparison, x="Count", y="Issue", color="Stage",
                    barmode="group", orientation="h",
                    color_discrete_map={"Before cleaning": "#263B63", "After cleaning": "#27B6AD"},
                    category_orders={"Issue": ["Missing cells", "Exact duplicate rows", "Whitespace issues"]})
                    comparison_fig.update_layout(template="plotly_white", height=330,
                    margin=dict(l=10, r=20, t=15, b=10), font=dict(color="#17233D"),
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
                    comparison_fig.update_traces(marker_line_width=0)
                    st.plotly_chart(comparison_fig, use_container_width=True)

                    # Flag arithmetic inconsistencies without silently changing sales.
                    normalized_columns = {str(col).strip().lower(): col for col in approved_df.columns}
                    if all(key in normalized_columns for key in ["quantity", "unit_price", "total_sales"]):
                        quantity_col = normalized_columns["quantity"]
                        price_col = normalized_columns["unit_price"]
                        sales_col = normalized_columns["total_sales"]
                        q = pd.to_numeric(approved_df[quantity_col], errors="coerce")
                        price = pd.to_numeric(approved_df[price_col], errors="coerce")
                        sales = pd.to_numeric(approved_df[sales_col], errors="coerce")
                        expected_sales = q * price
                        mismatch_mask = q.notna() & price.notna() & sales.notna() & ((sales - expected_sales).abs() > 0.01)
                        mismatch_count = int(mismatch_mask.sum())
                        if mismatch_count:
                            st.warning(
                                f"Business-rule check: {mismatch_count} row(s) have Total_Sales different from Quantity × Unit_Price. "
                                "Review these against the source; CleanIQ has not changed these values automatically."
                            )
                            st.dataframe(approved_df.loc[mismatch_mask, [quantity_col, price_col, sales_col]], width="stretch")

                    score_change = after_score - before_score

                    if score_change > 0:

                        st.success(

                            f"Validation complete. Quality score improved "

                            f"by {score_change} point(s)."

                        )

                    elif score_change == 0:

                        st.info(

                            "Validation complete. The approved cleaning "

                            "did not change the overall quality score."

                        )

                    else:

                        st.warning(

                            "Validation complete, but the quality score "

                            "decreased. Review the approved changes."

                        )

                    # ------------------------------------------------

                    # AI Analysis Context

                    # ------------------------------------------------

                    st.subheader("🤖 AI Analysis Context")

                    missing_details = []

                    for col in missing_columns:

                        missing_count = int(df[col].isnull().sum())

                        missing_details.append({

                            "Column": col,

                            "Missing Values": missing_count,

                            "Missing %": round(

                                missing_count / len(df) * 100,

                                2

                            )

                        })

                    duplicate_details = []

                    for col in id_columns:

                        duplicate_count = int(

                            df[col].duplicated().sum()

                        )

                        if duplicate_count > 0:

                            duplicate_details.append({

                                "Column": col,

                                "Duplicate Values": duplicate_count

                            })

                    approved_action_counts = (

                        approved_changes["Action"]

                        .value_counts()

                        .to_dict()

                    )

                    # Report both original and remaining issues explicitly. Recommendations
                    # must be based on the cleaned dataset, not stale before-cleaning counts.
                    after_duplicate_ids = 0
                    for id_col in id_columns:
                        after_duplicate_ids += int(
                            approved_df[id_col].dropna().duplicated().sum()
                        )
                    before_nonstandard_dates = count_nonstandard_date_columns(df, date_columns)
                    after_nonstandard_dates = count_nonstandard_date_columns(approved_df, date_columns)

                    ai_context = {

                        "dataset": {

                            "rows": int(total_rows),

                            "columns": int(total_columns)

                        },

                        "quality": {

                            "before_score": int(before_score),

                            "after_score": int(after_score),

                            "score_change": int(score_change)

                        },

                        "issues_before_cleaning": {
                            "missing_values": int(before_missing),
                            "exact_duplicate_rows": int(before_duplicates),
                            "duplicate_business_keys": int(total_duplicate_ids),
                            "whitespace_issues": int(before_whitespace),
                            "nonstandard_date_columns": int(before_nonstandard_dates)
                        },

                        "issues_after_cleaning": {
                            "missing_values": int(after_missing),
                            "exact_duplicate_rows": int(after_duplicates),
                            "duplicate_business_keys": int(after_duplicate_ids),
                            "whitespace_issues": int(after_whitespace),
                            "nonstandard_date_columns": int(after_nonstandard_dates)
                        },

                        "missing_details": missing_details,

                        "duplicate_details": duplicate_details,

                        "approved_actions": approved_action_counts,

                        "approved_changes": int(len(approved_changes)),

                        "rejected_changes": int(len(rejected_changes)),

                        "review_changes": int(len(review_changes))

                    }

                    # ------------------------------------------------

                    # Free rule-based demo recommendations (no API call)

                    # ------------------------------------------------

                    st.subheader("🤖 CleanIQ Demo AI Recommendations")

                    demo_recommendations = []

                    st.caption("The recommendations below describe issues that remain after cleaning. Before-cleaning counts are shown separately in the validation summary.")

                    if after_missing > 0:

                        demo_recommendations.append(

                            f"Review the {after_missing} missing value(s) still present against the original source before filling or removing data."

                        )

                    if after_duplicate_ids > 0:

                        demo_recommendations.append(

                            f"Investigate {after_duplicate_ids} repeated value(s) still present in ID/business-key columns before changing records."

                        )

                    if after_whitespace > 0:

                        demo_recommendations.append(

                            f"Check the {after_whitespace} leading/trailing whitespace issue(s) that remain in text fields."

                        )

                    if after_nonstandard_dates > 0:

                        demo_recommendations.append(

                            "Confirm the source date convention before standardizing dates. Values such as 05/01/2026 can mean different dates depending on the source format."

                        )

                    if not demo_recommendations:

                        demo_recommendations.append(

                            "No remaining issues were detected by these checks. Review business rules for additional quality risks."

                        )

                    for recommendation in demo_recommendations:

                        st.write(f"• {recommendation}")

                    st.caption(

                        "Demo mode: these recommendations come from predefined "

                        "Python rules. No paid API or live AI model is used."

                    )

                    st.write(

                        "CleanIQ has prepared a structured summary from "

                        "verified data-quality findings. The future AI "

                        "layer will use this context for explanations "

                        "and recommendations rather than directly "

                        "modifying the dataset."

                    )

                    with st.expander("🔎 View Verified AI Context"):

                        st.json(ai_context)

                    # ------------------------------------------------

                    # AI Prompt Preview

                    # ------------------------------------------------

                    ai_prompt = f"""

You are the data-quality assistant inside CleanIQ.

Analyze the following verified dataset-quality findings.

Dataset:

- Rows: {total_rows}

- Columns: {total_columns}

Quality:

- Before score: {before_score}/100

- After score: {after_score}/100

- Score change: {score_change}

Issues before cleaning:

- Missing values: {before_missing}
- Exact duplicate rows: {before_duplicates}
- Duplicate business-key values: {total_duplicate_ids}
- Whitespace issues: {before_whitespace}
- Non-standard date columns: {before_nonstandard_dates}

Issues after cleaning:

- Missing values: {after_missing}
- Exact duplicate rows: {after_duplicates}
- Duplicate business-key values: {after_duplicate_ids}
- Whitespace issues: {after_whitespace}
- Non-standard date columns: {after_nonstandard_dates}

Missing-value details:

{missing_details}

Duplicate-key details:

{duplicate_details}

Approved cleaning actions:

{approved_action_counts}

Approved changes: {len(approved_changes)}

Rejected changes: {len(rejected_changes)}

Changes requiring review: {len(review_changes)}

Explain:

1. The most important remaining data-quality risks.

2. Why those issues matter from a business/data perspective.

3. What should be reviewed next.

4. Which actions should NOT be automated without human approval.

Do not invent missing values, records, business facts, or cleaning results.

Do not modify the dataset.

"""

                    with st.expander("🧠 View AI Prompt Preview"):

                        st.code(

                            ai_prompt.strip(),

                            language="text"

                        )

                    st.info(

                        "AI integration is intentionally separated from the "

                        "cleaning engine. The AI will explain verified facts "

                        "and recommend next actions; human approval remains "

                        "required for data changes."

                    )

                    # ------------------------------------------------

                    # Downloads

                    # ------------------------------------------------

                    st.markdown('<div id="downloads"></div>', unsafe_allow_html=True)

                    st.subheader("📥 Downloads")

                    csv_data = approved_df.to_csv(

                        index=False

                    ).encode("utf-8")

                    st.download_button(

                        label="Download Approved CSV",

                        data=csv_data,

                        file_name="CleanIQ_Cleaned_Dataset.csv",

                        mime="text/csv"

                    )

                    excel_data = to_excel(approved_df)

                    st.download_button(

                        label="Download Approved Excel",

                        data=excel_data,

                        file_name="CleanIQ_Cleaned_Dataset.xlsx",

                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

                    )

                    audit_csv = audit_log.to_csv(

                        index=False

                    ).encode("utf-8")

                    st.download_button(

                        label="Download Audit Log",

                        data=audit_csv,

                        file_name="CleanIQ_Audit_Log.csv",

                        mime="text/csv"

                    )

            else:

                st.info(

                    "Make a decision for every proposed change, "

                    "then click 'Apply Approved Changes'."

                )

        else:

            st.success(

                "No safe automatic cleaning changes were detected."

            )

            st.info(

                "Missing values and duplicate records are not "

                "automatically changed by CleanIQ."

            )
