class BankAccount:
    def __init__(self,name,balance):
        self.name=name
        self.__balance=balance
    def deposit(self,amount):
        if amount>0:
            self.__balance+=amount
    def withdraw(self,amount):
        if amount<=self.__balance:
            self.__balance-=amount
        else:
            print("Insufficient balance")
    def get_balance(self):
        return self.__balance
account=BankAccount("Ravi", 5000)
account.deposit(2000)
account.withdraw(1000)
print("Account Holder:", account.name)
print("Balance:", account.get_balance())
