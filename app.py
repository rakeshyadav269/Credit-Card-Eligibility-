import streamlit as st
import pickle
import numpy as np

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Credit Card Eligibility Prediction",
    page_icon="💳",
    layout="centered"
)
# ================= THEME SELECTOR (TOP RIGHT) =================
col_theme_1, col_theme_2, col_theme_3 = st.columns([8, 1, 1])

with col_theme_3:
    theme = st.selectbox(
        "Theme",
        ["Banking", "FinTech", "Dark"],
        label_visibility="collapsed"
    )

# ================= LOAD MODEL =================
with open("DT_model.pkl", "rb") as f:
    model = pickle.load(f)

# ================= CSS =================
st.markdown("""
<style>

/* Background */
.stApp {
    background-image: url("https://png.pngtree.com/thumb_back/fh260/background/20220227/pngtree-black-girl-shopping-online-with-credit-card-and-laptop-photo-image_44473314.jpg");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}

/* Title */
.page-title {
    background: rgba(255,255,255,0.9);
    padding: 18px;
    border-radius: 14px;
    font-size: 36px;
    font-weight: 800;
    text-align: center;
    color: #1b4332;
    margin-bottom: 25px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.25);
}

/* Section titles */
.section-title {
    font-size: 22px;
    font-weight: 700;
    color: #1b4332;
    margin-top: 20px;
}

/* Required star */
.required {
    color: red;
    font-weight: 900;
}

/* Warning */
.warning-box {
    background:#fff3cd;
    color:#856404;
    padding:14px;
    border-radius:10px;
    font-weight:700;
    text-align:center;
}

/* Success */
.success-box {
    background:#d4edda;
    color:#155724;
    padding:16px;
    border-radius:12px;
    font-size:20px;
    font-weight:800;
    text-align:center;
}

/* Error */
.error-box {
    background:#f8d7da;
    color:#721c24;
    padding:16px;
    border-radius:12px;
    font-size:20px;
    font-weight:800;
    text-align:center;
}

            /* Field label highlight */
.field-label {
    display: block;
    background: rgba(255, 255, 255, 0.92);
    color: #1b4332;
    padding: 6px 12px;
    border-radius: 8px;
    font-size: 15px;
    font-weight: 800;
    margin-bottom: 6px;
    box-shadow: 0px 2px 6px rgba(0,0,0,0.25);
}

/* Required star */
.required {
    color: red;
    font-weight: 900;
}
/* Section heading highlight */
.section-header {
    background: rgba(255, 255, 255, 0.95);
    color: #1b4332;
    padding: 10px 16px;
    border-radius: 10px;
    font-size: 22px;
    font-weight: 800;
    margin: 20px 0 12px 0;
    box-shadow: 0px 3px 8px rgba(0,0,0,0.25);
    text-align: center;
}

/* Remove extra space between label and input */
.field-label {
    margin-bottom: 2px !important;
    padding-bottom: 4px !important;
}
/* Reduce space between label and input */
.field-label {
    margin-bottom: 2px !important;
    padding-bottom: 2px !important;
}

/* Reduce space below input boxes */
div[data-testid="stNumberInput"],
div[data-testid="stSelectbox"] {
    margin-bottom: 6px !important;
}

/* Reduce space between rows inside columns */
div[data-testid="column"] > div {
    gap: 6px !important;
}


</style>
""", unsafe_allow_html=True)
# ================= THEME STYLING =================
if theme == "Banking":
    theme_css = """
    .page-title { color:#1b4332; }
    .field-label { border-left:5px solid #2d6a4f; }
    input, select { border:2px solid #95d5b2 !important; }
    """

elif theme == "FinTech":
    theme_css = """
    .page-title { color:#3c096c; }
    .field-label { border-left:5px solid #7b2cbf; }
    input, select { border:2px solid #c77dff !important; }
    """

else:  # Dark
    theme_css = """
    .stApp { background-color:#0f172a; }
    .page-title { color:#f8fafc; background:rgba(0,0,0,0.7); }
    .field-label { background:#1e293b; color:white; }
    input, select {
        background:#020617 !important;
        color:white !important;
        border:2px solid #475569 !important;
    }
    """

st.markdown(f"<style>{theme_css}</style>", unsafe_allow_html=True)

# ================= TITLE =================
st.markdown(
    "<div class='page-title'>💳 Credit Card Eligibility Prediction App</div>",
    unsafe_allow_html=True
)

# ================= CUSTOMER DETAILS =================
st.markdown("<div class='section-header'>👤 Customer Details</div>", unsafe_allow_html=True)


col1, col2 = st.columns(2)

with col1:
    st.markdown("<div class='field-label'>Customer Age <span class='required'>*</span></div>", unsafe_allow_html=True)
    Customer_Age = st.number_input("", 18, 100, 30)

    st.markdown("<div class='field-label'>Dependent Count</div>", unsafe_allow_html=True)
    Dependent_count = st.selectbox("", [0,1,2,3,4,5])

    st.markdown("<div class='field-label'>Education Level</div>", unsafe_allow_html=True)
    Education_Level = st.selectbox(
        "", ["High School","Graduate","Uneducated","College","Post-Graduate","Doctorate","Unknown"]
    )

with col2:
    st.markdown("<div class='field-label'>Gender <span class='required'>*</span></div>", unsafe_allow_html=True)
    Gender = st.selectbox("", ["M","F"])

    st.markdown("<div class='field-label'>Marital Status</div>", unsafe_allow_html=True)
    Marital_Status = st.selectbox("", ["Single","Married","Divorced"])

    st.markdown("<div class='field-label'>Income Category <span class='required'>*</span></div>", unsafe_allow_html=True)
    Income_Category = st.selectbox(
        "", ["Less than $40K","$40K - $60K","$60K - $80K","$80K - $120K","$120K +","Unknown"]
    )


# ================= FINANCIAL DETAILS =================
st.markdown("<div class='section-header'>💳 Financial & Account Details</div>", unsafe_allow_html=True)


col3, col4 = st.columns(2)

with col3:
    st.markdown("<div class='field-label'>Credit Limit <span class='required'>*</span></div>", unsafe_allow_html=True)
    Credit_Limit = st.number_input("", 1000, 50000, 10000)

    st.markdown("<div class='field-label'>Total Transaction Amount <span class='required'>*</span></div>", unsafe_allow_html=True)
    Total_Transaction_Amount = st.number_input("", 0, 20000, 0)

    st.markdown("<div class='field-label'>Avg Utilization Ratio <span class='required'>*</span></div>", unsafe_allow_html=True)
    Avg_Utilization_Ratio = st.number_input("", 0.0, 1.0, 0.0, format="%.2f")

    st.markdown("<div class='field-label'>Months on Book <span class='required'>*</span></div>", unsafe_allow_html=True)
    Months_on_book = st.number_input("", 0, 60, 12)


with col4:
    st.markdown("<div class='field-label'>Card Category <span class='required'>*</span></div>", unsafe_allow_html=True)
    Card_Category = st.selectbox("", ["Blue","Silver","Gold","Platinum"])

    st.markdown("<div class='field-label'>Total Revolving Balance</div>", unsafe_allow_html=True)
    Total_Revolving_Balance = st.number_input("", 0, 5000, 0)

    st.markdown("<div class='field-label'>Total Transaction Count <span class='required'>*</span></div>", unsafe_allow_html=True)
    Total_Transaction_Count = st.number_input("", 0, 200, 0)

    st.markdown("<div class='field-label'>Total Relationship Count <span class='required'>*</span></div>", unsafe_allow_html=True)
    Total_Relationship_Count = st.selectbox("", [1,2,3,4,5,6])


    



# ================= VALIDATION =================
is_valid = all([
    Customer_Age > 0,
    Credit_Limit > 0,
    Total_Transaction_Amount > 0,
    Total_Transaction_Count > 0,
    Avg_Utilization_Ratio >= 0
])

# ================= PREDICTION =================
if st.button("Predict Eligibility"):

    if not is_valid:
        st.markdown(
            "<div class='warning-box'>⚠ Please enter all mandatory details before checking eligibility.</div>",
            unsafe_allow_html=True
        )

        if st.button("🔄 Reset Form"):
            st.session_state.clear()
            st.experimental_rerun()

    else:
        input_data = np.array([[
        Customer_Age,
        Gender,
        Dependent_count,
        Education_Level,
        Marital_Status,
        Income_Category,
        Card_Category,
        Months_on_book,
        Total_Relationship_Count,
        0,
        0,
        Credit_Limit,
        Total_Revolving_Balance,
        Total_Transaction_Amount,
        Total_Transaction_Count,
        Avg_Utilization_Ratio
    ]])


        result = model.predict(input_data)[0]

        if result == 1:
            st.markdown(
                "<div class='success-box'>✅ CUSTOMER IS ELIGIBLE FOR CREDIT CARD</div>",
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                "<div class='error-box'>❌ CUSTOMER IS NOT ELIGIBLE FOR CREDIT CARD</div>",
                unsafe_allow_html=True
            )
