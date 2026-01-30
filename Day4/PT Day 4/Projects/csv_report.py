import csv
data = [["Name","Marks"],["Alice",85],["Bob",90]]
with open("report.csv","w",newline="") as file:
    writer=csv.writer(file)
    writer.writerows(data)
print("CSV report created")