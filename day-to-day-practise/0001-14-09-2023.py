from typing import List

my_list = [1,2,3,4]
my_list2 = [1,2,3,4,5]

def my_func(l: List, l2: List) -> List:
    my_tuple = l, l2
    return my_tuple

my_func(l=my_list, l2=my_list2)

class MyClass:
    def __init__(self, argument):
        self.z = argument

    def only_print(self):
        print(self.z)

create_instance = MyClass("str")

create_instance.only_print()

my_dict = {
    'a': 5,
    'b': 6
}

for z in my_dict.values():
    print(z)


my_list = [1,2,3,4,5,6,7,8,9,10]
my_list2 = [1,2,3,4,5,6,7,8,9,10]

if len(my_list) > 9 and len(my_list) is len(my_list2):
    print('list printed')
else:
    print('do notthing')


