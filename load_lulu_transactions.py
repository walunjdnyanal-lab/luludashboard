"""
Lulu UAE Sales Dashboard
------------------------
Streamlit app to visualize Lulu Hypermarket sales data
with demographic insights and advertisement budget.

Usage:
1. Place this file + lulu_transactions.csv + lulu_loyalty.csv + lulu_ad_budget.csv in your repo.
2. Create requirements.txt with:
   streamlit
   pandas
   numpy
   plotly
3. Run locally: streamlit run lulu_dashboard.py
4. Push repo to GitHub and deploy on Streamlit Cloud.
"""

import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------
# Page Config
# -------------------------
st.set_page_config(page_title="Lulu UAE — Sales Dashboard", layout="wide")
st.title("🛒 Lulu UAE — Sales & Demographics Dashboard")

# -------------------------
# Load Data
# -------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("lulu_transactions.csv", parse_dates=["transaction_date"])
    loyalty_df = pd.read_csv("lulu_loyalty.csv")
    ad_budget = pd.read_csv("lulu_ad_budget.csv")
    return df, loyalty_df, ad_budget

df, loyalty_df, ad_budget = load_data()

# -------------------------
# Sidebar Filters
# -------------------------
st.sidebar.header("🔎 Filters")

# Date filter
min_date, max_date = df["transaction_date"].min(), df["transaction_date"].max()
date_range = st.sidebar.date_input("Transaction date range", (min_date, max_date))

# Demographic filters
gender_filter = st.sidebar.multiselect("Gender", df["gender"].unique(), default=list(df["gender"].unique()))
nationality_filter = st.sidebar.multiselect("Nationality", df["nationality"].unique(), default=list(df["nationality"].unique()))
location_filter = st.sidebar.multiselect("Location", df["location"].unique(), default=list(df["location"].unique()))
loyalty_filter = st.sidebar.multiselect("Loyalty Tier", df["loyalty_tier"].unique(), default=list(df["loyalty_tier"].unique()))

# Age filter
age_min, age_max = int(df["age"].min()), int(df["age"].max())
age_range = st.sidebar.slider("Age Range", age_min, age_max, (age_min, age_max))

# Product category filter
category_filter = st.sidebar.multiselect("Product Category", df["product_category"].unique(), default=list(df["product_category"].unique()))

# -------------------------
# Apply Filters
# -------------------------
filtered = df[
    (df["transaction_date"] >= pd.to_datetime(date_range[0])) &
    (df["transaction_date"] <= pd.to_datetime(date_range[1])) &
    (df["gender"].isin(gender_filter)) &
    (df["nationality"].isin(nationality_filter)) &
    (df["location"].isin(location_filter)) &
    (df["loyalty_tier"].isin(loyalty_filter)) &
    (df["age"].between(age_range[0], age_range[1])) &
    (df["product_category"].isin(category_filter))
]

# -------------------------
# KPIs
# -------------------------
col1, col2, col3, col4 = st.columns(4)
col1.metric("💰 Total Sales (AED)", f"{filtered['sales_amount'].sum():,.2f}")
col2.metric("🧾 Transactions", f"{filtered.shape[0]}")
col3.metric("👥 Unique Customers", f"{filtered['customer_id'].nunique()}")
avg_sales = filtered["sales_amount"].mean() if not filtered.empty else 0
col4.metric("📊 Avg. Transaction (AED)", f"{avg_sales:,.2f}")

st.markdown("---")

# -------------------------
# Charts
# -------------------------
left, right = st.columns((2,1))

# Left: Sales by demographics
with left:
    st.subheader("Sales by Product Category")
    cat_sales = filtered.groupby("product_category")["sales_amount"].sum().reset_index()
    fig_cat = px.bar(cat_sales, x="product_category", y="sales_amount", title="Sales by Product Category", text_auto=True)
    st.plotly_chart(fig_cat, use_container_width=True)

    st.subheader("Sales by Age Group")
    bins = [15, 24, 34, 44, 54, 64, 100]
    labels = ["16-24","25-34","35-44","45-54","55-64","65+"]
    filtered["age_group"] = pd.cut(filtered["age"], bins=bins, labels=labels)
    age_sales = filtered.groupby("age_group")["sales_amount"].sum().reset_index()
    fig_age = px.bar(age_sales, x="age_group", y="sales_amount", title="Sales by Age Group", text_auto=True)
    st.plotly_chart(fig_age, use_container_width=True)

# Right: Demographics and ads
with right:
    st.subheader("Sales by Nationality")
    nat_sales = filtered.groupby("nationality")["sales_amount"].sum().reset_index()
    fig_nat = px.pie(nat_sales, names="nationality", values="sales_amount", title="Sales by Nationality")
    st.plotly_chart(fig_nat, use_container_width=True)

    st.subheader("Sales by Loyalty Tier")
    loyalty_sales = filtered.groupby("loyalty_tier")["sales_amount"].sum().reset_index()
    fig_loyalty = px.bar(loyalty_sales, x="loyalty_tier", y="sales_amount", title="Sales by Loyalty Tier", text_auto=True)
    st.plotly_chart(fig_loyalty, use_container_width=True)

    st.subheader("Advertisement Budget Allocation")
    fig_ad = px.pie(ad_budget, names="ad_category", values="budget_AED", title="Ad Budget (AED)")
    st.plotly_chart(fig_ad, use_container_width=True)

st.markdown("---")

# -------------------------
# Data Table + Download
# -------------------------
st.subheader("Filtered Transactions")
st.dataframe(filtered.sort_values("transaction_date", ascending=False))

csv = filtered.to_csv(index=False).encode("utf-8")
st.download_button("⬇️ Download CSV", csv, "filtered_transactions.csv", "text/csv")

st.caption("Data source: Lulu Hypermarket synthetic dataset (CSV). Replace with real data for production use.")
