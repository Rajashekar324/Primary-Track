'''text = "User ID:12345"
id = text.split(":")[1]
print(id)
'''
'''name = "vemula sameera"
parts = name.split()
initials = parts[0][0] + parts[1][0]
print(initials.upper())'''


'''name="   sum  "
print(name.strip())'''

'''msg="the trip was amazing "
print(len(msg.split()))'''

'''marks,attendance=89,90

if(marks>=50 and attendance>=75):
   print("Eligible for writing exam")
else:
   print("Not eligible")'''


'''recharge,gb=200,5
if recharge>250 and gb==5:
    print("Bonus ")
else:
    print("No bonus")'''

'''bill=2000
day="sunday"
member="Gold"
if bill>1000 and (day=="saturday" or day=="sunday") and member=="Gold":
    bill=bill*0.8
    print(bill)
else:
    print(bill)'''

'''psw=123
for i in range(3):
    password=int(input("Enter password:"))
    if password != psw and i!=2:
        print(f"Login failed . This is ur {i+1} attempt.")
    elif i==2:
       print(f"Login failed .This was ur last attempt. Try after sometime")
    else:
        print("login successfull")
        break'''


# l = []

# for i in range(8):
#     a = input("Enter item: ")
#     if a == "done":
#         break
#     else:
#         l.append(a)

# print(l)



# def greet(name):
#     print(f"Hi {name} ! Good morning")
# greet("sam")

# def add_all(*args):
#     sum=0
#     for i in args:
#         sum=sum+i
#     return sum
# print(add_all(1,2,3,3))


# def printdata(**s):
#     for key,value in s.items():
#         print(f"{key}:{value}")
# printdata(name="sam",age=89)

#  PROFILE GENERATOR


# name = input("Enter your name: ")
# age = int(input("Enter your age: "))
# city = input("Enter your city: ")
# profession = input("Enter your profession: ")   
# def generate_profile(**kwargs):
#     profile = f"Name: {kwargs['name']}\nAge: {kwargs['age']}\nCity: {kwargs['city']}\nProfession: {kwargs['profession']}"
#     return profile 
# print("\nGenerated Profile:")
# print(generate_profile(name=name, age=age, city=city, profession=profession))
