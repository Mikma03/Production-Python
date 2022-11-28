
####################################
# Function Parameters
#####################################

# Positional and Keyword Arguments

def my_func(a, b, c):
    print(f"a = {a}, b = {b}, c = {c}")

my_func(1,2,3)
## error will occur
my_func(1,2)


def my_func1(a = 1, b=2, c= 3):
    print(f"a = {a}, b = {b}, c = {c}")

my_func1(10, 20, 30)
my_func1(10, 20)
my_func1(10)
my_func1()


def my_func2(a, b=2, c= 3):
    print(f"a = {a}, b = {b}, c = {c}")

my_func2(c=20, b=15, a=10)
my_func2(10, c=10)

# -------------------------------------- #

# Unpacking Iterables

a = 1,2,3
type(a)
b = (1,2,3)
type(b)

c = (1)
type(c)

d = (1,)
type(d)

e = ()
type(e)


a,b,c = [1, 2, 3.145]
(a,b,c) = [1,2,3]

(a,b) = (1,2)

a,b = 3,4

a,b,c = 10, {12,4}, ['a']

a,b = 10,20
print(a, b)

a,b = b,a
print(a, b)


for e in "XYZ":
    print(e)

a,b,c = 'XYZ'

s = "YXS"
s[0]
s[-1]

