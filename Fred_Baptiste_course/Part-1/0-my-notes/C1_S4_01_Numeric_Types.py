
####################################
# Numeric Types
#####################################

# Integers: Data Types

print(type(100))

from decimal import Decimal
from signal import raise_signal
import sys

sys.getsizeof(0)


import time

def cacl(a: int) -> int:
    for i in range(100000):
        a *2

start = time.perf_counter()
cacl(10)
stop = time.perf_counter()

print(stop - start)

# -------------------------------------- #

# Integers: Operations

type(20/2)

import math

math.floor(3.99)

math.floor(-3.9999)

math.floor(-3.0000000000000001)

# -------------------------------------- #

# Integers: Constructors and Bases

a = int(Decimal("10.9"))

b = int("A", base=11)

int("12345")


int("101", 2)

bin(10)

oct(10)

hex(10)

def from_base10(n, b):
    if b < 2:
        raise ValueError('Base b must be >= 2')
    if n < 0:
        raise ValueError('Number n must be >= 0')
    if n == 0:
        return [0]
    digits = []
    while n > 0:
        n, m = divmod(n, b)
        digits.insert(0, m)
    return digits

# -------------------------------------- #

# Rational Numbers

from fractions import Fraction

help(Fraction)

# -------------------------------------- #

# Floats: Internal Representations


a = 0.1 + 0.1 + 0.1
b = 0.3 
a == b

format(0.1, '0.25f')

# -------------------------------------- #

# Floats: Equality Testing

import math

x = 1000.0000001
y = 1000.0000002
math.isclose(x, y)


t = 0.0000001
z = 0.0000002
math.isclose(t, z)

# -------------------------------------- #

# Floats: Coercing to Integers

import math

help(math.floor)
math.floor(10.4)
math.floor(-10.4)

help(math.ceil)
math.ceil(10.4)
math.ceil(-10.4)

help(math.trunc)
math.trunc(10.3), math.trunc(10.5), math.trunc(10.9)
int(10.4), int(10.5), int(10.9)
math.floor(10.4), math.floor(10.5), math.floor(10.9)

math.floor(-10.4), math.floor(-10.5), math.floor(-10.9)
math.trunc(-10.3), math.trunc(-10.5), math.trunc(-10.9)

math.ceil(10.4), math.ceil(10.5), math.ceil(10.9)
math.ceil(-10.4), math.ceil(-10.5), math.ceil(-10.9)

# -------------------------------------- #

# Floats: Rounding

help(round)

a = round(0.9)
a, type(a)

a = round(1.9, 0)
a, type(a)

round(1.8888, 3)
round(1.8888, 2)
round(1.8888, 1)
round(1.8888, 0)

round(888.88, 1)
round(888.88, 0)

round(888.88, -1)
round(888.88, -2)
round(888.88, -3)
round(888.88, -4)

# -------------------------------------- #

## Ties

round(1.35, 1)
round(1.25, 1)

round(-1.35, 1)
round(-1.25, 1)

def _round_(x):
    from math import copysign
    return int(x + 0.5 * copyright(1, x))

round(2.5), _round_(2.5)

# -------------------------------------- #

# Decimals

import decimal
from decimal import Decimal

decimal.getcontext()
decimal.getcontext().rounding
decimal.getcontext().prec

decimal.localcontext()
type(decimal.localcontext())
type(decimal.getcontext())

with decimal.localcontext() as ctx:
    ctx.prec = 6
    ctx.rounding = decimal.ROUND_HALF_UP
    print(ctx)
    print(decimal.getcontext())
    print(id(ctx) == id(decimal.getcontext()))


from decimal import Decimal
Decimal(-10.1)

t = (0, (3,1,4,5), -4)
Decimal(t)

Decimal((0, (3,1,4,5), -4))

format(0.1, '.25f')

Decimal(0.1) == Decimal('0.1')
Decimal(10) == Decimal('10')

decimal.getcontext().prec

# -------------------------------------- #

# Decimals: Math Operations

import decimal
from decimal import Decimal

x = 10
y = 3

print(x//y, x%y)
print(divmod(x, y), )
print(x==y *(x//y) + x%y)


x = -10
y = 3

print(x//y, x%y)
print(divmod(x, y), )
print(x==y *(x//y) + x%y)


help(Decimal)

a = Decimal('1.5')
print(a.ln())
print(a.exp())
print(a.sqrt())

import math
math.sqrt(a)

x = 2
x_dec = Decimal(2)
root_float = math.sqrt(x)
root_mixed = math.sqrt(x_dec)
root_dec = x_dec.sqrt()


print(format(root_float, '1.27f'))
print(format(root_mixed, '1.27f'))
print(root_dec * root_dec)

# -------------------------------------- #

# Decimals: Performance Considerations

from decimal import Decimal
import sys

a = 3.14678
b = Decimal('3.14678')

sys.getsizeof(a)
sys.getsizeof(b)

import time

def run_float(n=1):
    for i in range(n):
        a = 3.14678


def run_decimal(n=1):
    for i in range(n):
        a = Decimal('3.14678')

start = time.perf_counter()
run_float(n)
end = time.perf_counter()
print('float:', end-start)

start = time.perf_counter()
run_decimal(n)
end = time.perf_counter()
print('float:', end-start)


###
def run_float(n=1):
    a = 3.14678
    for i in range(n):
        a + a

def run_decimal(n=1):
    a = Decimal('3.14678')
    for i in range(n):
        a + a

start = time.perf_counter()
run_float(n)
end = time.perf_counter()
print('float:', end-start)

start = time.perf_counter()
run_decimal(n)
end = time.perf_counter()
print('float:', end-start)


###
import math
import time
from decimal import Decimal
import sys

n = 500000

def run_float(n=1):
    a = 3.14678
    for i in range(n):
        math.sqrt(a)


def run_decimal(n=1):
    a = Decimal('3.14678')
    for i in range(n):
        a.sqrt()

start = time.perf_counter()
run_float(n)
end = time.perf_counter()
print('float:', end-start)

start = time.perf_counter()
run_decimal(n)
end = time.perf_counter()
print('float:', end-start)

# -------------------------------------- #

# Booleans

issubclass(bool, int)
int(True)
int(False)

id(True)
id(0)

True is 1
True == 1

True > False
(1 == 2) == False
(1 == 2) == True

True + True + True 
(True + True + True ) % 2

bool(x)
bool(-1)
bool(1)

help(bool)
issubclass(bool, int)

type(True), id(True), int(True)
type(False), id(False), int(False)

(3 < 4) == True
(3 < 4) is True

(1 == 3) == False

int(True), int(False)
1 + True

True > False

-True

True and False
True or False

bool(0)
bool(1)

bool(False)
bool(True)

# -------------------------------------- #

# Booleans: Truth Values

bool(None)
bool(-1)

help(int)

bool(0)
0 != 0

(100).__bool__()
(0).__bool__()

a = []
bool(a)
a.__len__()
bool(a.__len__())

b = ""
c = ()
bool(b)
bool(c)

a = {}
b = set()

bool(a), bool(b)

bool(None)

a = [1, 2, 3]
if a is not None and len(a) > 0:
    print(a[1])
else:
    print(a[2])


if bool(a):
    print(a[1])
else:
    print(a[2])

# -------------------------------------- #

# Booleans: Precedence and Short-Circuiting

not, and, or

## Operators

< >,  <=, >=, ==, !=, in, is

not
and
or


True or True and False
True or (True and False)
(True or True) and False

a = 10
b = 2

if a/b >2:
    print('a is at leat twice b')

if b > 0 and a/b >2:
    print('a is at leat twice b')

import string
help(string)

# -------------------------------------- #

# Booleans: Boolean Operators

'a' or [1,2]
'' or [1,2]


s1 = None
s2 = ''
s3 = 'abc'


s1 = s1 or 'n/a'
s2 = s2 or 'n/a'
s3 = s3 or 'n/a'
print(s1, s2, s3)


[] or [0]
None or [0]


print(None and 100)
[] and [0]


a = 2
b = 4
if b == 0:
    print(0)
else:
    print(a/b)

print(b and a/b)


s1 = None
s2 = ''
s3 = 'abc'

print((s1 and s1[0] or 'n/a'))
print((s2 and s1[0] or 'n/a'))
print((s3 and s1[0] or 'n/a'))


help(bool)
not True
not False

not bool('abc')
not 'abc'
type(not 'abc')

not None


# -------------------------------------- #

# Comparison Operators

0.1 is (3+4j)
3 is 3
[1,2] is [1,2]

'a' in 'this is a test'
3 in [1,2,3]
3 not in [1,2,3]

'key1' in {'key1': 1}
1 in {'key1': 1}

3 < 5

from decimal import Decimal
from fractions import Fraction

4 < Decimal('10.5')
Fraction(2,3) < Decimal('0.5')

True == Fraction(2, 3)
True < Fraction(3, 2)

1 < 2 and 2 < 3


import string

'A' > 'a'


