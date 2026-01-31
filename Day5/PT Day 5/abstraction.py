# from abc import ABC, abstractmethod
# class Vehicle(ABC):
#     @abstractmethod
#     def start_engine(self):
#         pass
# class Car(Vehicle):
#     def start_engine(self):
#         print("Car engine started") 
# c=Car()
# c.start_engine()

# class A:
#     def display(self):
#         print("This is class A")
# class B():
#     def display(self):
#         print("This is class B")
# class C(A,B):
#     pass

# d=C()
# d.display()



# Abstraction

# class Parent:
#     def __init__(self):
#         self.public_var = "public"
#         self._protected_var = "protected"
#         self.__private_var = "private"  
#     def access_from_same_class(self):
#         print("Inside Parent class:")
#         print("Public variable:", self.public_var)
#         print("Protected variable:", self._protected_var)
#         print("Private variable:", self.__private_var)
# class Child(Parent):
#     def access_from_subclass(self):
#         print("Inside Child class {Subclass}")
#         print("Public variable:", self.public_var)
#         print("Protected variable:", self._protected_var)
#         try:
#             print("Private variable:", self.__private_var)  # This will raise an AttributeError
#         except AttributeError:
#             print("Private Cannot be accessed in subclass{AttributeError}")
# class Stranger:
#     def acccess_from_other_class(self,obj):
#         print("Inside Stranger class {Unrelated}")
#         print("Public variable:", obj.public_var)
#         print("Protected variable:", obj._protected_var)
#         try:    
#             print("Private variable:", obj.__private_var)  # This will raise an AttributeError
#         except AttributeError:
#             print("Private Cannot be accessed in unrelated class{AttributeError}")

# p = Parent()
# c = Child()
# s = Stranger()
# p.access_from_same_class()
# c.access_from_subclass()
# s.acccess_from_other_class(p)



