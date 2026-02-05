from employee import employee
e1 = employee.Employee(101, "Alice", 50000, "Developer")
e2 = employee.Employee(102, "Bob", 60000, "Tester")
e3 = employee.Employee(103, "John", 75000, "HR")
employees = [e1, e2, e3]
search_name = input("Enter employee name: ")
found = False
for emp in employees:
    if emp.name.lower() == search_name.lower():
        print("\n Employee Found")
        emp.display()
        found = True
        break
if not found:
    print("\n Employee not found")