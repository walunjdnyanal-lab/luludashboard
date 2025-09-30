# lulu_sales_dashboard_app.py
# Streamlit dashboard for AM Sales Manager - Lulu Mall (UAE)
# Features:
# - Accepts transactional CSV upload (or generates synthetic demo data)
# - Shows KPIs, demographic insights, category-wise sales
# - Shows advertisement budget (overall + category-wise)
# - Provides loyalty program simulation and suggested segments
# - Allows export of simulated loyalty members and ad budgets

import streamlit as st
import pandas as pd
import numpy as np
import io
import plotly.express as px
import datetime

st.set_page_config(page_title="Lulu Mall Sales Dashboard (UAE)", layout="wide")

# ------------------------- Helpers -------------------------
@st.cache_data
def generate_demo_data(n=5000, seed=42):
    np.random.seed(seed)
    start = datetime.datetime(2024,1,1)
    end = datetime.datetime(2025,9,29)
    days = (end - start).days
    dates = [start + datetime.timedelta(days=int(np.random.rand()*days)) for _ in range(n)]

    customer_ids = np.random.choice(range(10000,20000), size=n, replace=True)
    ages = np.random.choice(list(range(16,76)), size=n, p=np.concatenate([np.ones(50)/50]))
    genders = np.random.choice(['Male','Female','Other'], size=n, p=[0.48,0.50,0.02])
    emirates = np.random.choice(['Dubai','Abu Dhabi','Sharjah','Ajman','Ras Al Khaimah','Fujairah','Umm Al Quwain'], size=n, p=[0.6,0.15,0.12,0.04,0.04,0.03,0.02])
    categories = np.random.choice(['Clothing','Grocery','Electronics','Home & Living','Beauty','Toys'], size=n, p=[0.22,0.35,0.15,0.12,0.1,0.06])
    amounts = np.round(np.random.exponential(scale=120, size=n) + np.where(categories=='Electronics',200,0) + np.where(categories=='Grocery',20,0),2)
    payment_type = np.random.choice(['Cash','Card','Mobile Pay'], size=n, p=[0.25,0.65,0.10])

    df = pd.DataFrame({
        'transaction_id': [f'TX{100000+i}' for i in range(n)],
        'date': dates,
        'customer_id': customer_ids,
        'age': ages,
        'gender': genders,
        'emirate': emirates,
        'category': categories,
        'amount': amounts,
        'payment_type': payment_type
    })
    df['year_month'] = df['date'].dt.to_period('M').astype(str)
    return df

@st.cache_data
def sample_ad_budget():
    # Example ad budget across categories per quarter (AED)
    budget = pd.DataFrame({
        'category': ['Clothing','Grocery','Electronics','Home & Living','Beauty','Other'],
        'budget_aed': [350000, 500000, 300000, 150000, 100000, 50000]
    })
    budget['pct'] = (budget['budget_aed'] / budget['budget_aed'].sum())*100
    return budget

@st.cache_data
def construct_loyalty(df):
    # Simple RFM-like scoring for loyalty segments
    ref_date = df['date'].max() + pd.Timedelta(days=1)
    cust = df.groupby('customer_id').agg({
        'date': lambda x: (ref_date - x.max()).days,
        'transaction_id': 'count',
        'amount': 'sum'
    }).rename(columns={'date':'recency_days','transaction_id':'frequency','amount':'monetary'})
    # Normalize scores
    cust['r_score'] = pd.qcut(cust['recency_days'], 5, labels=[5,4,3,2,1]).astype(int)
    cust['f_score'] = pd.qcut(cust['frequency'].rank(method='
