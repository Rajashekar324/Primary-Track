def registration(func):
    def wrapper(email,username, password):
        if len(password) < 8:
            print("Password must be at least 8 characters long.")
        elif "@" not in email or "." not in email:
            print("Invalid email format.")
        else:
            func(email,username, password)
    return wrapper
@registration
def register_user(email,username, password):
    print(f"Registration Successful for user {username} with email {email}  .")
email = input("Enter your email: ")
username = input("Enter your username: ")
password = input("Enter your password: ")
register_user(email,username, password)