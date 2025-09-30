import pandas as pd

# Assume df is your transactional dataset with at least:
# customer_id, transaction_date, sales_amount

# 1. Prepare recency, frequency, monetary
df['transaction_date'] = pd.to_datetime(df['transaction_date'])
snapshot_date = df['transaction_date'].max() + pd.Timedelta(days=1)

cust = df.groupby('customer_id').agg({
    'transaction_date': lambda x: (snapshot_date - x.max()).days,
    'transaction_id': 'count',
    'sales_amount': 'sum'
}).reset_index()

cust.rename(columns={
    'transaction_date': 'recency',
    'transaction_id': 'frequency',
    'sales_amount': 'monetary'
}, inplace=True)

# 2. Create R, F, M scores (1–5 bins using qcut)
cust['r_score'] = pd.qcut(cust['recency'], 5, labels=[5,4,3,2,1])  # lower recency = better
cust['f_score'] = pd.qcut(cust['frequency'].rank(method='first'), 5, labels=[1,2,3,4,5])
cust['m_score'] = pd.qcut(cust['monetary'], 5, labels=[1,2,3,4,5])

# 3. Combine into RFM segment
cust['RFM_Segment'] = cust['r_score'].astype(str) + cust['f_score'].astype(str) + cust['m_score'].astype(str)
cust['RFM_Score'] = cust[['r_score','f_score','m_score']].astype(int).sum(axis=1)

# 4. Example segmentation rule
cust['Segment'] = pd.cut(cust['RFM_Score'],
                         bins=[0,5,9,12,15],
                         labels=['Low Value','Mid Value','High Value','Champions'])

print(cust.head())
