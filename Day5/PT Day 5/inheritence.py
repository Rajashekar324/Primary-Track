# Simple Inheritence
# class Employee:
#     def __init__(self,name,emp_id,department):
#         self.name=name
#         self.emp_id=emp_id
#         self.department=department
#     def display_details(self):
#         print(f"Employee Name: {self.name}")
#         print(f"Employee ID: {self.emp_id}")
#         print(f"Department: {self.department}")
# name=input("Enter employee name: ")
# emp_id=input("Enter employee ID: ")
# department=input("Enter department: ")
# e1=Employee(name, emp_id, department)
# e1.display_details()


# Multilevel Inheritance

# class Person:
#     def __init__(self, name):
#         self.name=name
# class Employee(Person):
#     def __init__(self,name,emp_id,department):
#         super().__init__(name)
#         self.emp_id=emp_id
#         self.department=department
# class Manager(Employee):
#     def __init__(self,name,emp_id,department,salary):
#         super().__init__(name,emp_id,department)
#         self.salary=salary
#     def display_details(self):
#         print(f"Employee Name: {self.name}")
#         print(f"Employee ID: {self.emp_id}")
#         print(f"Department: {self.department}")
#         print(f"Salary: {self.salary}")
# name=input("Enter employee name: ")
# emp_id=input("Enter employee ID: ")
# department=input("Enter department: ")
# salary=input("Enter salary: ")
# m1=Manager(name,emp_id,department,salary)
# m1.display_details()


# Hierarchical Inheritance

# class Person:
#     def __init__(self,name):
#         self.name=name
# class Employee(Person):
#     def __init__(self,name,emp_id,department):
#         super().__init__(name)
#         self.emp_id=emp_id
#         self.department=department
#     def display_employee(self):
#         print("Employee Name:", self.name)
#         print("Employee ID:", self.emp_id)
#         print("Department:", self.department)
# class Student(Person):
#     def __init__(self,name,roll_no,course):
#         super().__init__(name)
#         self.roll_no=roll_no
#         self.course=course
#     def display_student(self):
#         print("Student Name:",self.name)
#         print("Roll No:", self.roll_no)
#         print("Course:", self.course)
# name=input("Enter employee name: ")
# emp_id=input("Enter employee ID: ")
# department=input("Enter department: ")
# e1=Employee(name,emp_id,department)
# e1.display_employee()
# print()
# name=input("Enter student name: ")
# roll_no=input("Enter roll number: ")
# course=input("Enter course: ")
# s1=Student(name,roll_no,course)
# s1.display_student()


# Multiple Inheritance

# class Person:
#     def __init__(self,name):
#         self.name=name
# class EmployeeDetails:
#     def __init__(self,emp_id,department):
#         self.emp_id=emp_id
#         self.department=department
# class Employee(Person,EmployeeDetails):
#     def __init__(self,name,emp_id,department):
#         Person.__init__(self,name)
#         EmployeeDetails.__init__(self,emp_id,department)
#     def display_details(self):
#         print("Employee Name:",self.name)
#         print("Employee ID:",self.emp_id)
#         print("Department:",self.department)
# name=input("Enter employee name: ")
# emp_id=input("Enter employee ID: ")
# department=input("Enter department: ")
# e1=Employee(name,emp_id,department)
# e1.display_details()
