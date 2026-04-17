import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# 1. Page Configuration
st.set_page_config(page_title="Telecom Churn Dashboard", layout="wide")

st.title("📊 Telecom Customer Analytics Dashboard")
st.markdown("""
Welcome to the **Telecom Churn Intelligence System**
- 📊 Overview Dashboard & 📈 Deep EDA Analysis  
- 🤖 ML Churn Prediction  
""")

st.sidebar.success("Select a page above ⬆️")

# 2. Data Loading & Cleaning
@st.cache_data
def load_data():
    df = pd.read_csv("df_merg")
    # Standardize column names to lowercase with underscores to match your code logic
    df.columns = [c.lower().replace(" ", "_") for c in df.columns]
    
    # Fill missing categories so charts render correctly
    df["churn_category"] = df["churn_category"].fillna("None")
    df["churn_reason"] = df["churn_reason"].fillna("None")
    df["internet_type"] = df["internet_type"].fillna("None")
    df["offer"] = df["offer"].fillna("No Offer")
    return df

df = load_data()

# 3. Sidebar Filters
st.sidebar.header("🎛 Filters")
city = st.sidebar.multiselect("City", df["city"].unique())
contract = st.sidebar.multiselect("contract", df["contract"].unique())

# 4. Filtering Logic
filtered_df = df.copy()
if city:
    filtered_df = filtered_df[filtered_df["city"].isin(city)]
if contract:
    filtered_df = filtered_df[filtered_df["contract"].isin(contract)]


# 5. Data Preprocessing (Tenure Groups)
filtered_df["tenure_group"] = pd.cut(
    filtered_df["tenure_in_months"],
    bins=[-1, 12, 36, 72],
    labels=["New", "Mid", "Loyal"]
)

# 6. Key Performance Indicators (KPIs)
st.subheader("📌 Executive Summary")
c1, c2, c3, c4, c5 = st.columns(5)

total_cust = len(filtered_df)
churn_df = filtered_df[filtered_df["customer_status"] == "Churned"]
churn_r = (len(churn_df) / total_cust * 100) if total_cust > 0 else 0
arpu = filtered_df["monthly_charge"].mean()
rev_at_risk = churn_df["total_revenue"].sum()

c1.metric("Total Customers", f"{total_cust:,}")
c2.metric("Churn Rate", f"{churn_r:.1f}%", delta=f"{(churn_r - 26):.1f}% vs Bench", delta_color="inverse")
c3.metric("ARPU", f"${arpu:.2f}", help="Average Revenue Per User")
c4.metric("Revenue at Risk", f"${rev_at_risk/1e3:.1f}k")
c5.metric("Avg Tenure", f"{filtered_df['tenure_in_months'].mean():.1f} Mo")

st.divider()

# 7. CHURN REASON ANALYSIS
st.subheader("❓ Why are they leaving?")
if not churn_df.empty:
    fig_reason = px.pie(
        churn_df, 
        names="churn_category", 
        hole=0.4,
        title="Churn Reasons (Top Categories)",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    st.plotly_chart(fig_reason, use_container_width=True)
    
    st.markdown("### 💡 Key Insights: The Competitor & Value Gap")
    ci1, ci2 = st.columns(2)
    with ci1:
        st.info(f"""
        **1. The Competitor Dominance (45%)**
        Almost half of all churned customers are being 'poached'. This suggests our 
        retention offers are not strong enough to stop switching.
        """)
    with ci2:
        st.warning(f"""
        **2. The Experience & Support Gap (34%)**
        'Dissatisfaction' and 'Attitude' account for over 1/3 of churn. This is an 
        internal service quality issue.
        """)
    st.success(f"""
    **🎯 Strategic Recommendation:** We have a **'Price-Value Paradox.'** High-paying customers 
    (ARPU: ${arpu:.2f}) are leaving for competitors. 
    **Action:** Target high-ARPU users in their first 6 months with loyalty lock-in offers.
    """)
else:
    st.write("No churned data available for selected filters.")

# 8. COMPETITOR DEEP DIVE
st.subheader("🎯 Deep Dive: The Competitor Threat")
competitor_churn = filtered_df[filtered_df["churn_category"] == "Competitor"]

if not competitor_churn.empty:
    reason_counts = competitor_churn["churn_reason"].value_counts().reset_index()
    reason_counts.columns = ["churn_reason", "count"]
    fig_comp = px.bar(
        reason_counts, y="churn_reason", x="count", orientation='h',
        text="count", color="count", color_continuous_scale="Reds"
    )
    fig_comp.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig_comp, use_container_width=True)
else:
    st.write("No competitor churn data found for current filters.")

st.divider()

# 9. GENERAL DISTRIBUTIONS
st.subheader("📊 Operational Analysis")
col_a, col_b = st.columns(2)

with col_a:
    st.write("**Churn Distribution**")
    fig1 = px.histogram(filtered_df, x="customer_status", color="customer_status")
    st.plotly_chart(fig1, use_container_width=True)

with col_b:
    st.write("**Tenure vs Status**")
    fig2 = px.box(filtered_df, x="customer_status", y="tenure_in_months", color="customer_status")
    st.plotly_chart(fig2, use_container_width=True)

# 10. HIGH COST BARRIER (The "Money" Visual)
st.subheader("💰 The High-Cost Barrier: Tenure vs. Monthly Charges")

fig_barrier = px.scatter(
    filtered_df, x="tenure_in_months", y="monthly_charge",
    color="customer_status", marginal_x="box", marginal_y="box",
    hover_data=["contract", "internet_type"],
    color_discrete_map={'Churned': '#e74c3c', 'Stayed': '#2ecc71', 'Joined': '#3498db'},
    opacity=0.6
)
fig_barrier.add_vrect(x0=0, x1=12, fillcolor="red", opacity=0.1, layer="below", line_width=0)
st.plotly_chart(fig_barrier, use_container_width=True)

st.info("""
**Finding:** Churned customers often have higher monthly charges but lower Tenure. 
* **The Danger Zone (Red Shaded):** The top-left corner represents customers paying high fees who haven't been with the company long. These are your highest churn risks.
""")

# 11. SERVICE USAGE SEGMENTATION
st.divider()
st.subheader("🛠 Service Usage vs. Retention")
services = ['internet_type', 'contract', 'tenure_group']
selected_svc = st.segmented_control("Select Dimension to Compare:", services, default='internet_type')

fig_svc = px.histogram(
    filtered_df, x=selected_svc, color="customer_status",
    barmode="group", text_auto='.2s',
    color_discrete_map={'Churned': '#e74c3c', 'Stayed': '#2ecc71'}
)
st.plotly_chart(fig_svc, use_container_width=True)

# Update your load_data to include population if needed
@st.cache_data
def load_data():
    df = pd.read_csv("df_merg")
    df.columns = [c.lower().replace(" ", "_") for c in df.columns]
    
    # Fill NAs for columns that only exist for certain subsets
    df["churn_category"] = df["churn_category"].fillna("None")
    df["churn_reason"] = df["churn_reason"].fillna("None")
    df["offer"] = df["offer"].fillna("No Offer")
    df["internet_type"] = df["internet_type"].fillna("None")
    return df

# --- New Insight: Referral Power ---
st.divider()
st.subheader("🤝 The Referral Impact on Retention")

# Create a 'Referrer' flag
filtered_df['is_referrer'] = filtered_df['number_of_referrals'] > 0

fig_ref = px.histogram(
    filtered_df, 
    x="is_referrer", 
    color="customer_status",
    barmode="group",
    text_auto=True,
    labels={"is_referrer": "Has Referred Friends/Family?", "customer_status": "Status"},
    color_discrete_map={'Churned': '#e74c3c', 'Stayed': '#2ecc71', 'Joined': '#3498db'}
)

st.plotly_chart(fig_ref, use_container_width=True)


col1, col2 = st.columns(2)

with col1:
    st.info("""
    **The Data Speaks:**  Customers who **DO NOT** refer (False) have a churn volume nearly **double** that of those who do.
    * Specifically, **1,245** non-referrers churned compared to only **624** referrers.
    """)

with col2:
    st.success("""
    **The Business Logic:**
    Referrals create a "social lock-in." When a customer refers a friend, they become an ambassador for the brand, which makes them much more likely to stay themselves to maintain that shared connection.
    """)

st.markdown("""
> **🚀 Actionable Strategy:** > We should launch a **'Refer-a-Friend' program** specifically targeting customers in the **'Mid' tenure group** (12-36 months). 
> This won't just bring in new 'Joined' customers (which is currently low at 81-373)—it will directly cut our churn in half by turning passive users into active advocates.
""")