import pandas as pd
df = pd.read_csv("product_data.csv")
df["Total_Sales"] = df["Price"] * df["Quantity"]
df["Tax"] = df["Total_Sales"] * 0.10
print(df)
df.to_csv("bank_transactions.csv", index=False)