# only_errors = []

# def extract_errors_simple():
#     with open("applications.log", 'r') as file:
#         for line in file:
#             if "Errno" in line:
#                 words = line.split()
#                 if len(words) > 0:
#                     only_errors.append(line)

# errors = extract_errors_simple()

# for error in only_errors:
#     print(error)


# import re

# username = input("Enter your username: ")
# password = input("Enter your password: ")

# def check_password_strength(username, password):
#     if len(password) < 8:
#         return "Weak"
    
#     has_upper = re.search(r"[A-Z]", password)
#     has_lower = re.search(r"[a-z]", password)
#     has_digit = re.search(r"\d", password)
#     has_special = re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)
    
#     if username.lower() in password.lower():
#         return "Weak (Password should not contain username)"
    
#     if has_upper and has_lower and has_digit and has_special:
#         return "Strong"
#     elif (has_upper or has_lower) and has_digit:
#         return "Moderate"
#     else:
#         return "Weak"

# strength = check_password_strength(username,password)
# print(f"Password strength: {strength}")
