class Dog():
    type = 'canine'
    
    def __init__(self, name, color):
        self.name = name
        self.color = color
    
    def bark(self):
        print(f' My name is {self.name}')
    

fido = Dog('fido', 'red')
fido.bark()

print(Dog.bark(fido))
print(fido.name)
print(Dog.type)
print(Dog('fido', 'red'))   


class Employee:

    raise_amount = 1.04
    num_of_emps = 0

    def __init__(self, first, last, pay):
        self.first = first
        self.last = last
        self.pay = pay

        Employee.num_of_emps += 1

    def fullname(self):
        return '{} {}'.format(self.first, self.last)

    def apply_raise(self):
        self.pay = int(self.pay * self.raise_amount)

    @classmethod
    def set_raise_amt(cls, amount):
        cls.raise_amt = amount 

emp_1 = Employee('Monkey', 'Leo', 50000)
emp_2 = Employee('Rabbit', 'Jenny', 60000)

Employee.set_raise_amt(1.05)

print(emp_1.raise_amt)
print(emp_1.raise_amount)


