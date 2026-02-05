def designation(func):
    def wrapper():
        print("Designation: Developer")
        func()
    return wrapper


def salary(func):
    def wrapper():
        print("Salary: 50000")
        func()
    return wrapper

@designation
@salary
def employee_details():
    print("Employee details printed")
employee_details()