import pandas as pd
data = {
    "Transaction_id": [1, 2, 3, 4],
    "Type": ["deposit", "withdrawal", "deposit", "withdrawal"],
    "Amount": [1000, 20000, 300, 3330]
}
df = pd.DataFrame(data)
total_deposit = df[df["Type"] == "deposit"]["Amount"].sum()
total_withdrawal = df[df["Type"] == "withdrawal"]["Amount"].sum()
final_balance = total_deposit - total_withdrawal
high_value = df[df["Amount"] > 5000]
print("Total Deposit:", total_deposit)
print("Total Withdrawal:", total_withdrawal)
print("Final Balance:", final_balance)
print("\nHigh Value Transactions:")
print(high_value)