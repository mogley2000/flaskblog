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
        self.email = first + '.' + last + '@email.com'

        Employee.num_of_emps += 1

    def fullname(self):
        return '{} {}'.format(self.first, self.last)

    def apply_raise(self):
        self.pay = int(self.pay * self.raise_amount)

    @classmethod
    def set_raise_amt(cls, amount):
        cls.raise_amt = amount 


class Developer(Employee):
    raise_amount = 1.10

    def __init__(self, first, last, pay, prog_lang):
        super().__init__(first, last, pay)
        self.prog_lang = prog_lang


emp_1 = Employee('Monkey', 'Leo', 50000)
emp_2 = Employee('Rabbit', 'Jenny', 60000)

Employee.set_raise_amt(1.05)

dev_1 = Developer('Foo', 'Bar', 50000, 'Python')
dev_2 = Developer('Test', 'Employee', 60000, 'Java')

print(dev_1.email)
print(dev_1.prog_lang)

class Manager(Employee):
    def __init__(self, first, last, pay, employees=None):
        super().__init__(first, last, pay)
        if employees is None:
            self.employees = []
        else:
            self.employees = employees 

    def add_emp(self, emp):
        if emp not in self.employees:
            self.employees.append(emp)
    
    def add_emp(self, emp):
        if emp in self.employees:
            self.employees.remove(emp)
    
    def print_emps(self):
        for emp in self.employees:
            print('-->', emp.fullname())

mgr_1 = Manager('Sue', 'Smith', 90000, [dev_1])
print(mgr_1.email)
mgr_1.print_emps()
