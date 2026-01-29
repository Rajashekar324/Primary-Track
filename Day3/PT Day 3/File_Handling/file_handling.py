# 1. Writing to a file using write mode ('w').
# 2. Reading from a file using read mode ('r').
# 3. Appending to a file using append mode ('a').


# file=open("notes.txt","w")
# file.write("Welcome to file handling in python\n")
# file.write("This is a simple file\n")
# file.close()

# file=open("notes.txt","r")
# content=file.read()
# print(content)
# file.close()

# file=open("notes.txt","a")
# file.write("This line is appended.\n")
# file.close()

# with open("notes.txt","r") as file:
# content=file.read()
# print(content)

# feedback = input("Enter your feedback: ")
# with open("feedback.txt","a") as file:
#     file.write(feedback + "\n")
# print("Thank you for your feedback!")

# with open("data.txt", "w") as file:
# print(file.readline().strip())
# print(file.readline().strip())
# print(file.readline().strip())

# file=open("data.txt","w")
# file.write("Welcome to file handling in python\n")
# file.write("This is a simple file\n")
# file.close()

with open("data.txt", "r") as file:
    while True:
        line = file.readline()
        if not line:
            break
        print(line.strip())