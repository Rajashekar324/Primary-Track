from abc import ABC, abstractmethod
class Person:
    def __init__(self,name,age):
        self.name=name
        self.age=age

class Customer(Person):
    def __init__(self,name,age,customer_id):
        super().__init__(name,age)
        self.customer_id=customer_id

class Employee(Person):
    def __init__(self,name,age,emp_id,role):
        super().__init__(name,age)
        self.emp_id=emp_id
        self.role=role

class Account(ABC):
    def __init__(self,account_no,customer):
        self.account_no=account_no
        self.customer=customer
        self.__balance=0

    def deposit(self,amount):
        self.__balance+=amount
        print("Deposited:",amount)
    def get_balance(self):
        return self.__balance
    @abstractmethod
    def withdraw(self, amount):
        pass
class SavingsAccount(Account):
    def withdraw(self,amount):
        if amount<=self.get_balance():
            self._Account__balance-=amount
            print("Withdrawn from Savings:",amount)
        else:
            print("Insufficient balance")
class CurrentAccount(Account):
    def withdraw(self,amount):
        self._Account__balance-=amount
        print("Withdrawn from Current:",amount)
emp = Employee("Raj",35,"E101","Manager")
print("Employee:",emp.name,emp.role)
cust = Customer("Ravi",25,"C201")
print("Customer:",cust.name,cust.customer_id)
savings=SavingsAccount("SA1001",cust)
current=CurrentAccount("CA2001",cust)
savings.deposit(5000)
savings.withdraw(2000)
print("Savings Balance:",savings.get_balance())
current.deposit(3000)
current.withdraw(4000)
print("Current Balance:",current.get_balance())
