def add_designation(designation):
    def decorator(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            print(f"Designation: {designation}")
            return result
        return wrapper
    return decorator
def add_salary(salary):
    def decorator(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            print(f"Salary: ${salary:,}")
            print("-" * 30)
            return result
        return wrapper
    return decorator
@add_salary(75000)
@add_designation("Manager")
def employee1_details(name, emp_id, department):
    print(f"\nEmployee Name: {name}")
    print(f"Employee ID: {emp_id}")
    print(f"Department: {department}")
@add_salary(60000)
@add_designation("Senior Developer")
def employee2_details(name, emp_id, department):
    print(f"\nEmployee Name: {name}")
    print(f"Employee ID: {emp_id}")
    print(f"Department: {department}")
@add_salary(30000)
@add_designation("Intern")
def employee3_details(name, emp_id, department):
    print(f"\nEmployee Name: {name}")
    print(f"Employee ID: {emp_id}")
    print(f"Department: {department}")
print("=" * 40)
print("EMPLOYEE DETAILS")
print("=" * 40)
employee1_details("John Doe","EMP001","IT")
employee2_details("Jane Smith","EMP002","Engineering")
employee3_details("Bob Johnson","EMP003","Marketing")