class Employee:
    def __init__(self, emp_id, name, salary, designation):
        self.emp_id = emp_id
        self.name = name
        self.salary = salary
        self.designation = designation

    def display(self):
        print(f"ID: {self.emp_id}")
        print(f"Name: {self.name}")
        print(f"Salary: {self.salary}")
        print(f"Designation: {self.designation}")