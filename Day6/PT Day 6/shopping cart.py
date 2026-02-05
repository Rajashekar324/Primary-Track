items={"apple":1,"milk":2,"bread":1.5}
cart=[]
def show_cart(func):
    def wrapper():
        func()
        print("\n--- Your Cart ---")
        cart_iter = iter(cart)
        total=0
        try:
            while True:
                item=next(cart_iter)
                price=items[item]
                print(f"{item}:${price}")
                total+=price
        except StopIteration:
            pass  
        print(f"Total:${total}")
    return wrapper
def welcome(func):
    def wrapper():
        print("=== WELCOME ===")
        name=input("Enter name: ")
        print(f"Hi {name}!")
        return func()
    return wrapper
@welcome
@show_cart
def shop():
    print("\nItems: apple($1), milk($2), bread($1.5)")
    while True:
        choice=input("Add item (or 'done'): ").lower()
        if choice=='done':
            break
        if choice in items:
            cart.append(choice)
            print(f"Added {choice}")
        else:
            print("Not available")
shop()