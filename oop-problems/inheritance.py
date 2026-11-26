from math import isfinite


class Vehicle:
    def drive(self):
        return "Driving a vehicle"


class Car(Vehicle):
    def drive(self):
        return "Driving a car"


class Bicycle(Vehicle):
    def drive(self):
        return "Riding a bicycle"


class Person:
    def __init__(self, name, age, address):
        self.name = name
        self.age = age
        self.address = address

    def introduce(self):
        return f"I'm {self.name}, I'm {self.age}, and I live at {self.address}."


class Student(Person):
    def __init__(self, name, age, address, field_of_study):
        super().__init__(name, age, address)
        self.field_of_study = field_of_study

    def introduce(self):
        return f"{super().introduce()} I study {self.field_of_study}."


class Employee(Person):
    def __init__(self, name, age, address, company):
        super().__init__(name, age, address)
        self.company = company

    def introduce(self):
        return f"{super().introduce()} I work at {self.company}."


class BankAccount:
    def __init__(self, account_number, balance=0):
        if not isfinite(balance) or balance < 0:
            raise ValueError("Opening balance must be finite and nonnegative")
        self.account_number = account_number
        self._balance = balance

    @property
    def balance(self):
        return self._balance

    def deposit(self, amount):
        self._check_amount(amount)
        self._balance += amount

    def withdraw(self, amount):
        self._check_amount(amount)
        if amount > self._balance:
            raise ValueError("Insufficient funds")
        self._balance -= amount

    def transfer(self, destination, amount):
        if not isinstance(destination, BankAccount):
            raise TypeError("Destination must be a bank account")
        self._check_amount(amount)
        if amount > self.balance:
            return False
        destination.deposit(amount)
        self._balance -= amount
        return True

    @staticmethod
    def _check_amount(amount):
        if not isfinite(amount) or amount <= 0:
            raise ValueError("Amount must be finite and positive")


class SavingsAccount(BankAccount):
    def __init__(self, account_number, balance=0, interest_rate=0.02):
        super().__init__(account_number, balance)
        if not isfinite(interest_rate) or interest_rate < 0:
            raise ValueError("Interest rate must be finite and nonnegative")
        self.interest_rate = interest_rate

    def add_interest(self):
        self._balance += self._balance * self.interest_rate

    def check_balance(self):
        return self.balance
