"""
Load Lulu Transactions CSV
--------------------------
This script loads the pre-generated `lulu_transactions.csv` file
and performs some preprocessing so it’s ready for dashboards or analysis.
"""

import pandas as pd

def load_transactions(file_path: str = "lulu_transactions.csv") -> pd.DataFrame:
    """
    Load the Lulu transactions dataset.

    Args:
        file_path (str): Path to the CSV file (default: 'lulu_transactions.csv').

    Returns:
        pd.DataFrame: Processed dataframe with parsed dates.
    """
    # Load CSV
    df = pd.read_csv(file_path, parse_dates=["transaction_date"])

    # Ensure correct data types
    df["transaction_id"] = df["transaction_id"].astype(str)
    df["customer_id"] = df["customer_id"].astype(str)
    df["product_category"] = df["product_category"].astype("category")
    df["gender"] = df["gender"].astype("category")
    df["nationality"] = df["nationality"].astype("category")
    df["location"] = df["location"].astype("category")
    df["loyalty_tier"] = df["loyalty_tier"].astype("category")

    # Sort by date
    df = df.sort_values("transaction_date").reset_index(drop=True)

    return df


if __name__ == "__main__":
    df = load_transactions("lulu_transactions.csv")
    print("✅ Lulu transactions loaded successfully!")
    print(df.head(10))   # Preview first 10 rows
