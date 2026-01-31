# class Employee:
#     def __init__(self, name, emp_id, department):
#         self.name = name
#         self.emp_id = emp_id
#         self.department = department
#     def display_details(self, name=None, emp_id=None, department=None):
#         if name is None and emp_id is None and department is None:
#             print(f"Employee Name: {self.name}")
#             print(f"Employee ID: {self.emp_id}")
#             print(f"Department: {self.department}")
#         else:
#             print(f"Employee Name: {name}")
#             print(f"Employee ID: {emp_id}")
#             print(f"Department: {department}")
# class Manager(Employee):
#     def __init__(self, name, emp_id, department, team_size):
#         super().__init__(name, emp_id, department)
#         self.team_size = team_size
#     def display_details(self):
#         print(f"Manager Name: {self.name}")
#         print(f"Manager ID: {self.emp_id}")
#         print(f"Department: {self.department}")
#         print(f"Team Size: {self.team_size}")
# name = input("Enter employee name: ")
# emp_id = input("Enter employee ID: ") 
# department = input("Enter department: ")
# e1 = Employee(name, emp_id, department)
# print("\n=== Method Overloading ===")
# print("With arguments:")
# e1.display_details(name, emp_id, department)
# print("\nWithout arguments:")
# e1.display_details()
# print("\n=== Method Overriding ===")
# team_size = input("Enter team size for manager: ")
# m1 = Manager("Sarah", "M001", "IT", team_size)
# m1.display_details()