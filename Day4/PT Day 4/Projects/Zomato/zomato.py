user_name=input("Enter your name: ")
print("Hello, "+user_name+"! Welcome to Zomato Calculator.")
try:
    items=int(input("How many items do you want to order? "))
    if items==0:
        raise ValueError("You cannot order 0 items.")
    price_per_item=100
    total_amount=items*price_per_item
except ValueError as e:
    print("Error:",e)
except Exception as e:
    print("Unknown Error:",e)
else:
    print("Order successful!")
    print("Total Bill Amount:",total_amount)
finally:
    print("Thank you for using Zomato!")
