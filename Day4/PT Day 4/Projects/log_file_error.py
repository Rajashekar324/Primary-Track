with open("logs.log", "r") as log, open("errors.txt", "w") as out:
    for line in log:
        if "ERROR" in line:
            out.write(line)
print("Errors extracted")