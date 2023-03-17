
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

# set
s = {1, 2, 3}

# that will be error
s[0]

d1 = {'a': 1, 'b': 2, 'c': 3}

for e in d1:
    print(e)

a,b,c = d
print(d)

for e in d1.values:
    print(e)



# -------------------------------------- #

# Extended Unpacking

l = [1, 2, 3, 4, 5,6]
b = l[1:0]

a, b = l[0], l[1]
a, *b = l


a = 'abcdef'
a, *b = s
a,b,c,d = a[0], a[1], s[2:-1], s[-1]

t = ('a', 'b', 'c')
a, *b = t



l = [lambda: print(x) for x in range(10)]
x=15
l[0]()


x = "bdgbfebsetbsrtbargbtsrthwhteshsertabnaerthaethaehtaehbdgbfebsetbsrtbargbtsrthwhteshsertabnaerthaethaehtaeh"
y = "bdgbfebsetbsrtbargbtsrthwhteshsertabnaerthaethaehtaehbdgbfebsetbsrtbargbtsrthwhteshsertabnaerthaethaehtaeh"

print(id(x))
print(id(y))