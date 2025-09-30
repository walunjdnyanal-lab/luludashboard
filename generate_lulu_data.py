import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_synthetic_data(n_rows: int = 100, seed: int = 42):
    np.random.seed(seed)

    # Pools
    genders = ["Male", "Female", "Other"]
    nationalities = ["UAE", "India", "Philippines", "Egypt", "Pakistan", "UK", "Saudi Arabia", "Other"]
    locations = ["Abu Dhabi", "Dubai", "Sharjah", "Ajman", "Ras Al Khaimah"]
    product_categories = ["Clothing", "Grocery", "Electronics", "Home & Living", "Pharmacy"]
    loyalty_tiers = ["None", "Silver", "Gold", "Platinum"]

    # Dates in last 180 days
    end = datetime.today()
    start = end - timedelta(days=180)
    dates = [start + timedelta(days=int(x)) for x in np.random.randint(0, (end - start).days + 1, size=n_rows)]

    # Customers
    unique_customers = int(max(10, n_rows * 0.6))
    customer_ids = [f"C{1000 + i}" for i in range(unique_customers)]
    customers = np.random.choice(customer_ids, size=n_rows)

    # Map customer demographics
    cust_demo = {}
    for cid in customer_ids:
        cust_demo[cid] = {
            "age": int(np.random.normal(35, 12)),
            "gender": np.random.choice(genders, p=[0.48, 0.5, 0.02]),
            "nationality": np.random.choice(nationalities),
            "location": np.random.choice(locations),
            "loyalty_tier": np.random.choice(loyalty_tiers, p=[0.5, 0.25, 0.18, 0.07])
        }

    # Transactions
    rows = []
    for i in range(n_rows):
        cid = customers[i]
        demo = cust_demo[cid]
        category = np.random.choice(product_categories, p=[0.2, 0.45, 0.15, 0.12, 0.08])

        base_price = {
            "Clothing": np.random.normal(120, 60),
            "Grocery": np.random.normal(35, 20),
            "Electronics": np.random.normal(800, 400),
            "Home & Living": np.random.normal(220, 120),
            "Pharmacy": np.random.normal(40, 25)
        }[category]

        quantity = int(max(1, np.random.poisson(2)))
        total = max(2.0, round(base_price * quantity * np.random.uniform(0.7, 1.4), 2))

        rows.append({
            "transaction_id": f"T{10000 + i}",
            "transaction_date": dates[i].date(),
            "customer_id": cid,
            "age": max(16, demo["age"]),
            "gender": demo["gender"],
            "nationality": demo["nationality"],
            "location": demo["location"],
            "loyalty_tier": demo["loyalty_tier"],
            "product_category": category,
            "quantity": quantity,
            "sales_amount": total
        })

    df = pd.DataFrame(rows)

    # Loyalty program summary
    loyalty_df = df.groupby(["customer_id", "loyalty_tier"]).agg({
        "sales_amount": "sum",
        "transaction_id": "count"
    }).reset_index().rename(columns={"transaction_id": "transactions"})

    # Advertisement budget
    ad_budget = pd.DataFrame({
        "ad_category": ["Clothing", "Grocery", "Electronics"],
        "budget_AED": [200000, 350000, 150000]
    })

    return df, loyalty_df, ad_budget


if __name__ == "__main__":
    df, loyalty_df, ad_budget = generate_synthetic_data(n_rows=100, seed=42)

    # Save to CSV
    df.to_csv("lulu_transactions.csv", index=False)
    loyalty_df.to_csv("lulu_loyalty.csv", index=False)
    ad_budget.to_csv("lulu_ad_budget.csv", index=False)

    print("✅ Synthetic Lulu data generated and saved as CSV files:")
    print("- lulu_transactions.csv")
    print("- lulu_loyalty.csv")
    print("- lulu_ad_budget.csv")
