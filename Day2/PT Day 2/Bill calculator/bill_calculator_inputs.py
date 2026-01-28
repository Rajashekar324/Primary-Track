name=input("Enter person name: ")
name=name.strip()
phone=input("Enter phone number: ")
phone=phone.strip()
count=input("Enter number of bills: ")
email=input("Enter the Email ID: ")
if "@" not in email:
    print("Invalid email")
count=count.strip()
count=int(count)
bill_details=[]

for i in range(count):
    print(f"\nBill {i + 1}")
    place=input("Enter place spent: ")
    place=place.strip()
    amount=input("Enter bill amount: ")
    amount=amount.strip()
    amount=float(amount)
    bill_details.append((place, amount))
