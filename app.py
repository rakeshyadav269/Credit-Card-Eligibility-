import streamlit as st
import pickle
import pandas as pd
import random
import string
from datetime import date

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="ClearPath Bank — Credit Card Eligibility Application",
    page_icon="🏦",
    layout="centered"
)

# ================= LOAD MODEL =================
@st.cache_resource
def load_model():
    with open("RF_model.pkl", "rb") as f:
        return pickle.load(f)

model = load_model()

# ================= RESET =================
def reset_form():
    defaults = {
        "age": 0, "dep": 0, "edu": "-- Select --", "gender": "-- Select --",
        "marital": "-- Select --", "income": "-- Select --", "credit": 0,
        "trans_amt": 0, "util": 0.0, "months": 0, "card": "-- Select --",
        "revolving": 0, "trans_ct": 0, "rel": 0
    }
    for k, v in defaults.items():
        st.session_state[k] = v

if "age" not in st.session_state:
    reset_form()

# ================= REJECTION REASON ENGINE =================
def get_rejection_reasons(row):
    reasons = []

    if row["Total_Trans_Ct"] < 20:
        reasons.append((
            "Insufficient Transaction History",
            "Your account reflects a low number of transactions during the review period. "
            "A consistent pattern of card usage is required to establish repayment behaviour. "
            "We recommend maintaining regular monthly transactions to strengthen future applications."
        ))

    if row["Total_Trans_Amt"] < 2000:
        reasons.append((
            "Below Minimum Transaction Volume",
            "The total transaction amount recorded during the assessment period does not meet "
            "the minimum threshold required by our credit evaluation policy. "
            "Higher transaction volume demonstrates active financial engagement and creditworthiness."
        ))

    if row["Total_Revolving_Bal"] == 0:
        reasons.append((
            "Absence of Revolving Credit History",
            "No revolving balance has been recorded on your account. "
            "Revolving credit history is an important indicator used to assess how responsibly "
            "a customer manages their outstanding credit obligations."
        ))

    if row["Avg_Utilization_Ratio"] > 0.85:
        reasons.append((
            "Elevated Credit Utilisation Ratio",
            f"Your recorded utilisation ratio of {row['Avg_Utilization_Ratio']*100:.0f}% exceeds the "
            "acceptable threshold of 85%. A high utilisation ratio indicates that a significant "
            "portion of your available credit is in use, which is considered a risk factor "
            "under our credit assessment guidelines."
        ))
    elif row["Avg_Utilization_Ratio"] == 0.0:
        reasons.append((
            "No Credit Utilisation Recorded",
            "A utilisation ratio of 0% indicates that your credit facility has not been actively used. "
            "Our assessment requires evidence of responsible and moderate credit usage "
            "to evaluate repayment patterns."
        ))

    if row["Total_Relationship_Count"] <= 2:
        reasons.append((
            "Limited Banking Relationship",
            "The number of active products held with us is below the threshold considered "
            "for credit card eligibility. Customers with a broader banking relationship — "
            "including savings accounts, fixed deposits, or existing loan products — "
            "are assessed more favourably."
        ))

    if row["Income_Category"] in ["Less than $40K", "Unknown"]:
        reasons.append((
            "Income Category Below Eligibility Threshold",
            "The income category provided falls below the minimum income band required "
            "for this credit card product. We advise you to explore card products "
            "that are aligned with your current declared income level."
        ))

    if row["Months_on_book"] < 6:
        reasons.append((
            "Insufficient Account Tenure",
            "Your account has been active for fewer than 6 months. "
            "Our credit policy requires a minimum account tenure to establish a reliable "
            "financial history before a credit card application can be approved."
        ))

    if not reasons:
        reasons.append((
            "Application Did Not Meet Eligibility Criteria",
            "Following a comprehensive assessment of your financial profile — including "
            "transaction history, credit utilisation, income band, and account relationship — "
            "your application does not meet the minimum eligibility requirements at this time. "
            "You are welcome to reapply after a period of 90 days."
        ))

    return reasons[:3]

# ================= CSS =================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Source+Serif+4:wght@400;600;700&family=IBM+Plex+Sans:wght@300;400;500;600&display=swap');

:root {
    --navy:    #1A2B4A;
    --navy2:   #243557;
    --gold:    #B8922A;
    --gold2:   #D4A840;
    --cream:   #F5F2ED;
    --white:   #FFFFFF;
    --text:    #1C2B3A;
    --muted:   #6B7C93;
    --border:  #C8D0DC;
    --light:   #EDF0F5;
    --green:   #1A5C38;
    --red:     #8B1A1A;
    --input:   #FFFFFF;
    --shadow:  0 2px 16px rgba(26,43,74,0.10);
}

html, body {
    background: var(--cream) !important;
    font-family: 'IBM Plex Sans', sans-serif !important;
    color: var(--text) !important;
}

/* ===== CENTER FIX ===== */
[data-testid="stAppViewContainer"] > .main {
    display: flex;
    justify-content: center;
}

[data-testid="stAppViewContainer"] > .main > .block-container {
    max-width: 860px;
    width: 100%;
    margin-left: auto;
    margin-right: auto;
}

[data-testid="stHeader"] { background: transparent !important; }
#MainMenu, footer, header { visibility: hidden; }

/* ── TOP NAV BAR ── */
.topbar {
    background: var(--navy);
    margin: -1rem -1rem 0;
    padding: 0 40px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: 64px;
    border-bottom: 3px solid var(--gold);
}
.bank-name {
    font-family: 'Source Serif 4', serif;
    font-size: 22px;
    font-weight: 700;
    color: var(--white);
    letter-spacing: 0.3px;
}
.bank-name span { color: var(--gold2); }
.nav-links {
    display: flex;
    gap: 28px;
}
.nav-link {
    font-size: 12px;
    color: rgba(255,255,255,0.55);
    letter-spacing: 0.5px;
    font-weight: 500;
}
.nav-right {
    font-size: 11px;
    color: rgba(255,255,255,0.4);
    letter-spacing: 0.5px;
}

/* ── PAGE BANNER ── */
.page-banner {
    background: linear-gradient(100deg, var(--navy) 0%, var(--navy2) 100%);
    padding: 36px 40px 32px;
    margin: 0 -1rem 28px;
    border-bottom: 1px solid rgba(184,146,42,0.3);
    position: relative;
    overflow: hidden;
}
.page-banner::after {
    content: '';
    position: absolute;
    right: -30px; top: -30px;
    width: 180px; height: 180px;
    border: 40px solid rgba(184,146,42,0.07);
    border-radius: 50%;
}
.page-banner::before {
    content: '';
    position: absolute;
    right: 80px; bottom: -50px;
    width: 120px; height: 120px;
    border: 30px solid rgba(255,255,255,0.04);
    border-radius: 50%;
}
.banner-eyebrow {
    font-size: 11px;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--gold2);
    font-weight: 600;
    margin-bottom: 10px;
}
.banner-title {
    font-family: 'Source Serif 4', serif;
    font-size: 30px;
    font-weight: 700;
    color: var(--white);
    margin-bottom: 8px;
    line-height: 1.25;
}
.banner-sub {
    font-size: 14px;
    color: rgba(255,255,255,0.55);
    line-height: 1.65;
    max-width: 480px;
}
.banner-ref {
    margin-top: 20px;
    display: flex;
    gap: 24px;
}
.bref-item {
    font-size: 11px;
    color: rgba(255,255,255,0.35);
    letter-spacing: 0.5px;
}
.bref-item span { color: rgba(255,255,255,0.65); font-weight: 600; }

/* ── PROGRESS STEPS ── */
.steps-row {
    display: flex;
    align-items: center;
    margin-bottom: 28px;
    background: var(--white);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 16px 24px;
    box-shadow: var(--shadow);
}
.step {
    display: flex;
    align-items: center;
    gap: 10px;
    flex: 1;
}
.step-num {
    width: 30px; height: 30px;
    border-radius: 50%;
    background: var(--navy);
    color: var(--white);
    font-size: 13px;
    font-weight: 700;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
}
.step-info {}
.step-name { font-size: 13px; font-weight: 600; color: var(--navy); }
.step-desc { font-size: 11px; color: var(--muted); }
.step-divider { flex: 0.4; height: 1px; background: var(--border); margin: 0 8px; }

/* ── FORM SECTION ── */
.form-section {
    background: var(--white);
    border: 1px solid var(--border);
    border-radius: 12px;
    margin-bottom: 20px;
    overflow: hidden;
    box-shadow: var(--shadow);
}
.form-section-hdr {
    background: var(--navy);
    padding: 14px 24px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.form-section-title {
    font-family: 'Source Serif 4', serif;
    font-size: 15px;
    font-weight: 600;
    color: var(--white);
    letter-spacing: 0.2px;
}
.form-section-step {
    font-size: 11px;
    color: var(--gold2);
    letter-spacing: 1px;
    text-transform: uppercase;
    font-weight: 600;
}
.form-section-body {
    padding: 24px 24px 8px;
}
.gold-line {
    height: 3px;
    background: linear-gradient(90deg, var(--gold) 0%, var(--gold2) 60%, transparent 100%);
}

/* ── FIELD LABELS ── */
.flabel {
    font-size: 11px;
    font-weight: 600;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 0.9px;
    margin-bottom: 5px;
    margin-top: 2px;
}
.req { color: #C0392B; margin-left: 2px; font-weight: 700; }

/* ── INPUTS — fully visible on light bg ── */
.stNumberInput input {
    background: var(--input) !important;
    color: var(--text) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 8px !important;
    font-size: 15px !important;
    font-weight: 500 !important;
    font-family: 'IBM Plex Sans', sans-serif !important;
    padding: 10px 14px !important;
}
.stNumberInput input:focus {
    border-color: var(--navy) !important;
    box-shadow: 0 0 0 3px rgba(26,43,74,0.10) !important;
    outline: none !important;
}
.stNumberInput input::placeholder { color: #B0BCCB !important; }
.stNumberInput button {
    background: var(--light) !important;
    border: 1px solid var(--border) !important;
    color: var(--navy) !important;
    border-radius: 6px !important;
}

/* Selectbox */
.stSelectbox > div > div {
    background: var(--input) !important;
    color: var(--text) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 8px !important;
    font-size: 14px !important;
    font-family: 'IBM Plex Sans', sans-serif !important;
}
.stSelectbox > div > div:hover { border-color: var(--navy) !important; }
[data-baseweb="select"] span { color: var(--text) !important; }

/* Dropdown menu */
[data-baseweb="popover"] ul {
    background: var(--white) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    box-shadow: 0 8px 24px rgba(0,0,0,0.12) !important;
}
[role="option"] {
    color: var(--text) !important;
    background: var(--white) !important;
    font-size: 14px !important;
    font-family: 'IBM Plex Sans', sans-serif !important;
}
[role="option"]:hover, [aria-selected="true"] {
    background: var(--light) !important;
    color: var(--navy) !important;
}

/* ── BUTTONS ── */
.stButton > button {
    border-radius: 8px !important;
    font-family: 'IBM Plex Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    height: 48px !important;
    transition: all 0.2s ease !important;
}
div[data-testid="column"]:first-child .stButton > button {
    background: var(--navy) !important;
    color: var(--white) !important;
    border: none !important;
    box-shadow: 0 3px 12px rgba(26,43,74,0.25) !important;
    letter-spacing: 0.3px !important;
}
div[data-testid="column"]:first-child .stButton > button:hover {
    background: var(--navy2) !important;
    box-shadow: 0 6px 20px rgba(26,43,74,0.35) !important;
    transform: translateY(-1px) !important;
}
div[data-testid="column"]:last-child .stButton > button {
    background: transparent !important;
    color: var(--muted) !important;
    border: 1.5px solid var(--border) !important;
}
div[data-testid="column"]:last-child .stButton > button:hover {
    color: var(--navy) !important;
    border-color: var(--navy) !important;
}

/* ── RESULT — APPROVED ── */
.result-approved {
    background: var(--white);
    border: 1px solid #B7D9C4;
    border-top: 5px solid #2E7D52;
    border-radius: 12px;
    padding: 32px 36px;
    margin-top: 24px;
    box-shadow: 0 4px 20px rgba(46,125,82,0.10);
    animation: fadeUp 0.4s ease;
}
.res-icon-ok { font-size: 40px; margin-bottom: 12px; }
.res-title-ok {
    font-family: 'Source Serif 4', serif;
    font-size: 24px;
    font-weight: 700;
    color: #1A5C38;
    margin-bottom: 10px;
}
.res-body { font-size: 14px; color: #3D4F5C; line-height: 1.75; }
.res-meta {
    margin-top: 20px;
    padding-top: 16px;
    border-top: 1px solid var(--border);
    display: flex;
    gap: 32px;
}
.res-meta-item { font-size: 11px; color: var(--muted); }
.res-meta-item span { display: block; font-size: 13px; color: var(--text); font-weight: 600; margin-top: 2px; }

/* ── RESULT — REJECTED ── */
.result-rejected {
    background: var(--white);
    border: 1px solid #D9B7B7;
    border-top: 5px solid #8B1A1A;
    border-radius: 12px;
    padding: 32px 36px;
    margin-top: 24px;
    box-shadow: 0 4px 20px rgba(139,26,26,0.08);
    animation: fadeUp 0.4s ease;
}
.res-title-no {
    font-family: 'Source Serif 4', serif;
    font-size: 24px;
    font-weight: 700;
    color: var(--red);
    margin-bottom: 10px;
}

/* ── REASON CARDS ── */
.reasons-section { margin-top: 28px; }
.reasons-hdr {
    font-family: 'Source Serif 4', serif;
    font-size: 17px;
    font-weight: 600;
    color: var(--navy);
    margin-bottom: 6px;
}
.reasons-sub {
    font-size: 12px;
    color: var(--muted);
    margin-bottom: 16px;
    line-height: 1.5;
}
.reason-card {
    background: var(--white);
    border: 1px solid #DDD0D0;
    border-left: 4px solid #8B1A1A;
    border-radius: 10px;
    padding: 18px 20px;
    margin-bottom: 12px;
    box-shadow: 0 1px 6px rgba(139,26,26,0.05);
    animation: fadeUp 0.35s ease both;
}
.reason-card:nth-child(2) { animation-delay: 0.08s; }
.reason-card:nth-child(3) { animation-delay: 0.16s; }
.r-num {
    font-size: 10px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #8B1A1A;
    margin-bottom: 5px;
}
.r-title {
    font-size: 14px;
    font-weight: 700;
    color: var(--navy);
    margin-bottom: 6px;
}
.r-body { font-size: 13px; color: var(--muted); line-height: 1.7; }

.advice-card {
    background: #FFFDF5;
    border: 1px solid #E8D49A;
    border-left: 4px solid var(--gold);
    border-radius: 10px;
    padding: 18px 20px;
    margin-top: 6px;
}
.adv-title {
    font-size: 13px;
    font-weight: 700;
    color: var(--gold);
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-bottom: 8px;
}
.adv-body { font-size: 13px; color: #5C4A1A; line-height: 1.75; }

/* ── WARNING ── */
.warn-box {
    background: #FFFBF0;
    border: 1px solid #F0C040;
    border-left: 4px solid #D4A010;
    border-radius: 10px;
    padding: 16px 20px;
    margin-top: 16px;
}
.warn-title { font-size: 12px; font-weight: 700; color: #7A5A00; text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 10px; }
.warn-item { font-size: 13px; color: #7A5A00; margin: 5px 0; }

/* ── FOOTER ── */
.footer {
    background: var(--navy);
    margin: 36px -1rem -1rem;
    padding: 24px 40px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.footer-left { font-size: 11px; color: rgba(255,255,255,0.35); line-height: 1.8; }
.footer-right { font-size: 11px; color: rgba(255,255,255,0.3); text-align: right; line-height: 1.8; }

@keyframes fadeUp {
    from { opacity: 0; transform: translateY(14px); }
    to   { opacity: 1; transform: translateY(0); }
}
</style>
""", unsafe_allow_html=True)



# ================= TOP NAV =================
today = date.today().strftime("%d %b %Y")
st.markdown(f"""
<div class="topbar">
    <div class="bank-name">ClearPath <span>Bank</span></div>
    <div class="nav-links">
        <span class="nav-link">Personal Banking</span>
        <span class="nav-link">Cards & Loans</span>
        <span class="nav-link">Investments</span>
        <span class="nav-link">Support</span>
    </div>
    <div class="nav-right">Online Portal &nbsp;|&nbsp; {today}</div>
</div>
""", unsafe_allow_html=True)

# ================= PAGE BANNER =================
st.markdown(f"""
<div class="page-banner">
    <div class="banner-eyebrow">Cards & Loans › Credit Card Application</div>
    <div class="banner-title">Credit Card Eligibility Check</div>
    <div class="banner-sub">
        Complete the form below with accurate financial information.
        Your eligibility will be assessed instantly based on our internal credit evaluation criteria.
    </div>
    <div class="banner-ref">
        <div class="bref-item">Form Reference &nbsp;<span>CC-ELIG-2025</span></div>
        <div class="bref-item">Assessment Date &nbsp;<span>{today}</span></div>
        <div class="bref-item">Processing Time &nbsp;<span>Instant</span></div>
    </div>
</div>
""", unsafe_allow_html=True)

# ================= STEPS =================
st.markdown("""
<div class="steps-row">
    <div class="step">
        <div class="step-num">1</div>
        <div class="step-info">
            <div class="step-name">Personal Details</div>
            <div class="step-desc">Identity & demographics</div>
        </div>
    </div>
    <div class="step-divider"></div>
    <div class="step">
        <div class="step-num">2</div>
        <div class="step-info">
            <div class="step-name">Financial Details</div>
            <div class="step-desc">Account & transaction data</div>
        </div>
    </div>
    <div class="step-divider"></div>
    <div class="step">
        <div class="step-num">3</div>
        <div class="step-info">
            <div class="step-name">Eligibility Decision</div>
            <div class="step-desc">Instant assessment result</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ================= OPTIONS =================
SELECT       = "-- Select --"
GEN_OPTIONS  = [SELECT, "Female", "Male"]
EDU_OPTIONS  = [SELECT, "College", "Doctorate", "Graduate", "High School", "Post-Graduate", "Uneducated", "Unknown"]
MAR_OPTIONS  = [SELECT, "Divorced", "Married", "Single", "Unknown"]
INC_OPTIONS  = [SELECT, "Less than $40K", "$40K - $60K", "$60K - $80K", "$80K - $120K", "$120K +", "Unknown"]
CARD_OPTIONS = [SELECT, "Blue", "Gold", "Platinum", "Silver"]
REL_OPTIONS  = [0, 1, 2, 3, 4, 5, 6]
gender_raw   = {"Female": "F", "Male": "M"}

# ================= SECTION 1: PERSONAL =================
st.markdown("""
<div class="form-section">
<div class="form-section-hdr">
    <div class="form-section-title">👤 &nbsp;Section A — Personal Information</div>
    <div class="form-section-step">Step 1 of 2</div>
</div>
<div class="gold-line"></div>
<div class="form-section-body">
""", unsafe_allow_html=True)

c1, c2 = st.columns(2)
with c1:
    st.markdown("<div class='flabel'>Customer Age <span class='req'>*</span></div>", unsafe_allow_html=True)
    Customer_Age = st.number_input("__age", min_value=0, max_value=100, step=1, key="age",
                                   label_visibility="collapsed", help="Must be between 18 and 100")
    st.markdown("<div class='flabel'>Education Level</div>", unsafe_allow_html=True)
    Education_Level = st.selectbox("__edu", EDU_OPTIONS, key="edu", label_visibility="collapsed")
    st.markdown("<div class='flabel'>Number of Dependents</div>", unsafe_allow_html=True)
    Dependent_count = st.selectbox("__dep", [0,1,2,3,4,5], key="dep", label_visibility="collapsed")

with c2:
    st.markdown("<div class='flabel'>Gender <span class='req'>*</span></div>", unsafe_allow_html=True)
    Gender_display = st.selectbox("__gen", GEN_OPTIONS, key="gender", label_visibility="collapsed")
    st.markdown("<div class='flabel'>Marital Status</div>", unsafe_allow_html=True)
    Marital_Status = st.selectbox("__mar", MAR_OPTIONS, key="marital", label_visibility="collapsed")
    st.markdown("<div class='flabel'>Annual Income Category <span class='req'>*</span></div>", unsafe_allow_html=True)
    Income_Category = st.selectbox("__inc", INC_OPTIONS, key="income", label_visibility="collapsed")

st.markdown("</div></div>", unsafe_allow_html=True)

# ================= SECTION 2: FINANCIAL =================
st.markdown("""
<div class="form-section">
<div class="form-section-hdr">
    <div class="form-section-title">💳 &nbsp;Section B — Financial & Account Information</div>
    <div class="form-section-step">Step 2 of 2</div>
</div>
<div class="gold-line"></div>
<div class="form-section-body">
""", unsafe_allow_html=True)

c3, c4 = st.columns(2)
with c3:
    st.markdown("<div class='flabel'>Credit Limit ($) <span class='req'>*</span></div>", unsafe_allow_html=True)
    Credit_Limit = st.number_input("__cl", min_value=0, max_value=500000, step=500, key="credit",
                                   label_visibility="collapsed", help="Your existing credit card limit")
    st.markdown("<div class='flabel'>Total Transaction Amount ($) <span class='req'>*</span></div>", unsafe_allow_html=True)
    Total_Trans_Amt = st.number_input("__ta", min_value=0, max_value=200000, step=100, key="trans_amt",
                                      label_visibility="collapsed", help="Total spend in last 12 months")
    st.markdown("<div class='flabel'>Average Utilisation Ratio (0.00–1.00) <span class='req'>*</span></div>", unsafe_allow_html=True)
    Avg_Utilization_Ratio = st.number_input("__ur", min_value=0.0, max_value=1.0, step=0.01,
                                             format="%.2f", key="util", label_visibility="collapsed",
                                             help="E.g. 0.30 means 30% of limit used")
    st.markdown("<div class='flabel'>Months Account Active <span class='req'>*</span></div>", unsafe_allow_html=True)
    Months_on_book = st.number_input("__mob", min_value=0, max_value=60, step=1, key="months",
                                     label_visibility="collapsed", help="Duration of relationship with bank")

with c4:
    st.markdown("<div class='flabel'>Card Category <span class='req'>*</span></div>", unsafe_allow_html=True)
    Card_Category = st.selectbox("__cc", CARD_OPTIONS, key="card", label_visibility="collapsed")
    st.markdown("<div class='flabel'>Total Revolving Balance ($)</div>", unsafe_allow_html=True)
    Total_Revolving_Bal = st.number_input("__rb", min_value=0, max_value=50000, step=100, key="revolving",
                                          label_visibility="collapsed", help="Outstanding revolving credit balance")
    st.markdown("<div class='flabel'>Total Transaction Count <span class='req'>*</span></div>", unsafe_allow_html=True)
    Total_Trans_Ct = st.number_input("__tc", min_value=0, max_value=200, step=1, key="trans_ct",
                                     label_visibility="collapsed", help="Number of transactions in last 12 months")
    st.markdown("<div class='flabel'>Active Bank Products Held <span class='req'>*</span></div>", unsafe_allow_html=True)
    Total_Relationship_Count = st.selectbox("__rc", REL_OPTIONS, key="rel",
        label_visibility="collapsed",
        format_func=lambda x: "-- Select --" if x == 0 else f"{x} product{'s' if x > 1 else ''}")

st.markdown("</div></div>", unsafe_allow_html=True)

# ================= NOTICE =================
st.markdown("""
<div style="background:#EDF0F5; border:1px solid #C8D0DC; border-radius:8px;
            padding:12px 18px; margin-bottom:20px; font-size:12px; color:#6B7C93; line-height:1.65;">
    <strong style="color:#1A2B4A;">ℹ Important Notice:</strong> &nbsp;
    Fields marked with <span style="color:#C0392B; font-weight:700;">*</span> are mandatory.
    All information provided is used solely for eligibility assessment and is handled in
    accordance with our data privacy policy. Providing inaccurate information may result
    in disqualification of the application.
</div>
""", unsafe_allow_html=True)

# ================= BUTTONS =================
b1, b2 = st.columns([4, 1])
with b1:
    predict_clicked = st.button("Submit Application for Assessment", use_container_width=True)
with b2:
    st.button("Clear Form", use_container_width=True, on_click=reset_form)

# ================= PREDICT =================
if predict_clicked:
    missing = []
    if Customer_Age == 0:              missing.append("Customer Age")
    if Gender_display == SELECT:       missing.append("Gender")
    if Income_Category == SELECT:      missing.append("Annual Income Category")
    if Credit_Limit == 0:              missing.append("Credit Limit")
    if Total_Trans_Amt == 0:           missing.append("Total Transaction Amount")
    if Total_Trans_Ct == 0:            missing.append("Total Transaction Count")
    if Card_Category == SELECT:        missing.append("Card Category")
    if Total_Relationship_Count == 0:  missing.append("Active Bank Products Held")
    if Months_on_book == 0:            missing.append("Months Account Active")

    if missing:
        items = "".join(f"<div class='warn-item'>› &nbsp;{f}</div>" for f in missing)
        st.markdown(f"""
        <div class="warn-box">
            <div class="warn-title">⚠ Incomplete Submission — Required Fields Missing</div>
            {items}
        </div>""", unsafe_allow_html=True)

    else:
        Gender = gender_raw.get(Gender_display, "M")
        edu    = Education_Level if Education_Level != SELECT else "Graduate"
        mar    = Marital_Status  if Marital_Status  != SELECT else "Single"

        input_df = pd.DataFrame([{
            'Customer_Age':             int(Customer_Age),
            'Gender':                   Gender,
            'Dependent_count':          int(Dependent_count),
            'Education_Level':          edu,
            'Marital_Status':           mar,
            'Income_Category':          Income_Category,
            'Card_Category':            Card_Category,
            'Months_on_book':           int(Months_on_book),
            'Total_Relationship_Count': int(Total_Relationship_Count),
            'Months_Inactive_12_mon':   0,
            'Contacts_Count_12_mon':    0,
            'Credit_Limit':             float(Credit_Limit),
            'Total_Revolving_Bal':      int(Total_Revolving_Bal),
            'Total_Trans_Amt':          int(Total_Trans_Amt),
            'Total_Trans_Ct':           int(Total_Trans_Ct),
            'Avg_Utilization_Ratio':    float(Avg_Utilization_Ratio)
        }])

        result = model.predict(input_df)[0]
        ref = "CPB-CC-" + "".join(random.choices(string.digits, k=10))

        if result == 1:
            st.markdown(f"""
            <div class="result-approved">
                <div class="res-icon-ok">✅</div>
                <div class="res-title-ok">Application Pre-Approved</div>
                <div class="res-body">
                    We are pleased to inform you that based on the financial information provided,
                    your credit card application has been <strong>pre-approved</strong> subject to
                    final documentation verification.<br><br>
                    A ClearPath Bank representative will contact you within <strong>3–5 business days</strong>
                    to complete the issuance process. Please keep your identity documents ready.
                </div>
                <div class="res-meta">
                    <div class="res-meta-item">Application Reference<span>{ref}</span></div>
                    <div class="res-meta-item">Assessment Date<span>{today}</span></div>
                    <div class="res-meta-item">Status<span style="color:#1A5C38;">Pre-Approved ✓</span></div>
                    <div class="res-meta-item">Next Step<span>Document Verification</span></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        else:
            st.markdown(f"""
            <div class="result-rejected">
                <div class="res-icon-ok">❌</div>
                <div class="res-title-no">Application Unsuccessful</div>
                <div class="res-body">
                    We regret to inform you that following a thorough assessment of your
                    submitted financial profile, your credit card application has <strong>not been approved</strong>
                    at this time.<br><br>
                    The decision has been made in accordance with ClearPath Bank's internal credit evaluation
                    policy. Please refer to the detailed assessment feedback below to understand
                    the specific factors that influenced this decision.
                </div>
                <div class="res-meta">
                    <div class="res-meta-item">Application Reference<span>{ref}</span></div>
                    <div class="res-meta-item">Assessment Date<span>{today}</span></div>
                    <div class="res-meta-item">Status<span style="color:#8B1A1A;">Not Approved ✗</span></div>
                    <div class="res-meta-item">Review Period<span>90 Days</span></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            row = input_df.iloc[0]
            reasons = get_rejection_reasons(row)

            st.markdown("""
            <div class="reasons-section">
                <div class="reasons-hdr">Assessment Feedback — Reasons for Decline</div>
                <div class="reasons-sub">
                    The following factors were identified during your credit assessment.
                    Please review each point carefully before reapplying.
                </div>
            """, unsafe_allow_html=True)

            for i, (title, detail) in enumerate(reasons, 1):
                st.markdown(f"""
                <div class="reason-card">
                    <div class="r-num">Reason {i} of {len(reasons)}</div>
                    <div class="r-title">{title}</div>
                    <div class="r-body">{detail}</div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("""
            <div class="advice-card">
                <div class="adv-title">Recommended Actions Before Reapplying</div>
                <div class="adv-body">
                    <strong>1. Increase transaction activity</strong> — Ensure regular, consistent usage of your existing debit or credit facilities.<br>
                    <strong>2. Manage your utilisation ratio</strong> — Maintain utilisation between 10% and 30% of your available limit.<br>
                    <strong>3. Build revolving credit history</strong> — Sustaining a modest revolving balance and repaying on time improves your credit profile.<br>
                    <strong>4. Strengthen your banking relationship</strong> — Consider adding savings, fixed deposit, or loan products to your portfolio.<br><br>
                    You may submit a fresh application after a minimum period of <strong>90 days</strong>.
                    For personalised guidance, please visit your nearest ClearPath Bank branch
                    or contact us at <strong>1800-CPB-0000</strong> (Toll Free, Mon–Sat, 9 AM – 6 PM).
                </div>
            </div>
            </div>
            """, unsafe_allow_html=True)

# ================= FOOTER =================
st.markdown(f"""
<div class="footer">
    <div class="footer-left">
        © 2025 ClearPath Bank Ltd. All rights reserved.<br>
        Regulated by the Reserve Bank of India. Member of DICGC.<br>
        Credit decisions are subject to internal policy and regulatory guidelines.
    </div>
    <div class="footer-right">
        Privacy Policy &nbsp;|&nbsp; Terms & Conditions<br>
        Grievance Redressal &nbsp;|&nbsp; Fair Practices Code<br>
        Form CC-ELIG-2025 &nbsp;|&nbsp; Version 3.1
    </div>
</div>
""", unsafe_allow_html=True)
