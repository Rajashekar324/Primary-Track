# Bill Calculator
name=input("Enter person name: ")
name=name.strip()
phone=input("Enter phone number: ")
phone=phone.strip()
masked_phone=phone[:-5]+"*****"
count=input("Enter number of bills: ")
count=count.strip()
count=int(count)
total_bill=0
bill_details = []
for i in range(count):
    print(f"\nBill {i + 1}")
    place=input("Enter place spent: ")
    place=place.strip()
    amount=input("Enter bill amount: ")
    amount=amount.strip()
    amount=float(amount)
    total_bill+=amount
    bill_details.append((place, amount))
print("\n--- Person Billing Details ---")
print(f"Name     : {name}")
print(f"Phone No : {masked_phone}")
print("\n--- Bill Breakdown ---")
for place, amount in bill_details:
    print(f"{place} : ₹{amount:.2f}")
print(f"\nTotal Bill : ₹{total_bill:.2f}")
