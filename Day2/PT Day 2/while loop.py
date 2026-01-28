# username="qwerty"
# password="qwerty123"
# for i in range(3):
#     u = input("Enter username: ")
#     p = input("Enter password: ")
#     if u==username and p==password:
#         print("Login Successful")
#         break
#     else:
#         attempts_left = 2 - i
#         if attempts_left > 0:
#             print(f"Invalid credentials, {attempts_left} attempt(s) left")
#         else:
#             print("Login Failed")


# list=[]
# for i in range(9):
#     item=input("Enter the item to add: ")
#     if item=="done":
#         break
#     else:
#         list.append(item)
# print("Items in the list are:",list)


# def print_data(**kwargs):
#     for key, value in kwargs.items():
#         print(f"{key}: {value}")
# print_data(name="Alice", age=30)


name = input("Enter your name: ")
age = int(input("Enter your age: "))
city = input("Enter your city: ")
profession = input("Enter your profession: ")   
def generate_profile(**kwargs):
    profile = f"Name: {kwargs['name']}\nAge: {kwargs['age']}\nCity: {kwargs['city']}\nProfession: {kwargs['profession']}"
    return profile 
print("\nGenerated Profile:")
print(generate_profile(name=name, age=age, city=city, profession=profession))
