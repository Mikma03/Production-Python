from typing import List

my_list = [3, 5, 8, 4, 8]

for i in range(len(my_list)):
    print(my_list[i])

for i in my_list:
    print(i)

my_dict = {"a": 1, "b": 2}

for i in my_dict:
    print(i)

for i, j in my_dict.items():
    print(i, j)


class MyClass:
    def __init__(self, number):
        self.number_ = number

    def print_my_num(self):
        print(self.number_)


instance_of_my_class = MyClass(5)
instance_of_my_class.print_my_num()

# what means "is"?
a = 5
b = 5
print(a is b)

# difference beetween is and ==
# is checks if two variables point to the same object
# == checks if the objects referred to by the variables are equal

# example
a = [1, 2, 3]
b = a
print(a is b)

b = a[:]
print(a is b)


# positional only arguments in function

def my_func(a, b, /, c, d, *, e, f):
    print(a, b, c, d, e, f)


my_func(1, 2, 3, d=4, e=5, f=6)

