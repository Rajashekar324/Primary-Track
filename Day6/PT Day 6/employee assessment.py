users = {"admin": "123"}  # username: password
employees = []  # List of employees
def need_register(func):
    def wrapper(user, pwd):
        if user not in users:
            print(f"User '{user}' not found. Creating account...")
            users[user] = pwd
        return func(user, pwd)
    return wrapper
def need_login(func):
    def wrapper(user, pwd):
        if users.get(user) != pwd:
            print("Wrong password!")
            return
        return func(user, pwd)
    return wrapper
@need_register
@need_login
def employee_system(username, password):
    print(f"\n Access granted! Welcome {username}")
    while True:
        print("\n--- Menu ---")
        print("1. Add Employee")
        print("2. Show Employees")
        print("3. Logout")
        choice = input("Choose: ")
        if choice == '1':
            name = input("Employee name: ")
            salary = input("Salary: $")
            employees.append({"name": name, "salary": salary})
            print(f"Added {name}")
        elif choice == '2':
            print("\n--- Employees ---")
            for emp in employees:
                print(f"Name: {emp['name']} | Salary: ${emp['salary']}")
        elif choice == '3':
            print("Goodbye!")
            break
        else:
            print("Invalid choice")
print("=== EMPLOYEE SYSTEM ===")
user = input("Username: ")
pwd = input("Password: ")
employee_system(user, pwd)