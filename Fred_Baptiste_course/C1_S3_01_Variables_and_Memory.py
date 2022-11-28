
####################################
# Variables and Memory
#####################################

# Memory References

my_var = 10

print(my_var)
print(id(my_var))
print(hex(id(my_var)))

other_var = my_var

# -------------------------------------- #

# Reference Counting

import sys
from weakref import ref

a = [1, 2, 3]

print(id(a))
sys.getrefcount(a)


import ctypes

def ref_count(address: int):
    return ctypes.c_long.from_address(address).value

ref_count(2621733745024)

b = a
id(b)

b = None
id(b)

ref_count(id(a))

a_id = id(a)
a = None
ref_count(a_id)

# -------------------------------------- #

# Garbage Collection

import ctypes
import gc

def ref_count(address: int):
    return ctypes.c_long.from_address(address).value

def object_by_id(object_id):
    for obj in gc.get_objects():
        if id(obj) == object_id:
            return "Object exists"
    return "Not found"

# -------------------------------------- #

# Variable Re-Assignment

my_var = 10
my_var = my_var + 5


a = 10
b = 10
hex(id(a))
hex(id(b))

# -------------------------------------- #

# Object Mutability

a = [1, 2]
b = [3, 4]

t = (a, b)

a.append(3)
b.append(5)

# -------------------------------------- #

# Function Arguments and Mutability

def process(s):
    print('Initial s # = {0}'.format(id(s)))
    s = s + ' world'
    print('Final s # = {0}'.format(id(s)))

my_var = 'hello'
print('my_var # = {0}'.format(id(my_var)))

# -------------------------------------- #

# Everything is an Object

a = 12
b = 12 

print(id(a))
print(id(b))

c = 500
d = 500

print(id(c))
print(id(d))
