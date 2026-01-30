import re
password=input("Enter your password: ")
strength_points=0
if len(password) >= 8:
    strength_points += 1
if re.search(r"[A-Z]",password):
    strength_points+=1
if re.search(r"[a-z]",password):
    strength_points+=1
if re.search(r"[0-9]", password):
    strength_points+=1
if re.search(r"[!@#$%^&*(),.?\":{}|<>]",password):
    strength_points+=1
if strength_points<=2:
    print("Weak Password")
elif strength_points==3:
    print("Medium Password")
elif strength_points==4:
    print("Strong Password")
else:
    print("Very Strong Password")
