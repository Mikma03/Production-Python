
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


# Integers: Operations

type(20/2)

import math

math.floor(3.99)

math.floor(-3.9999)

math.floor(-3.0000000000000001)


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


# Rational Numbers

from fractions import Fraction

help(Fraction)


# Floats: Internal Representations


a = 0.1 + 0.1 + 0.1
b = 0.3 
a == b

format(0.1, '0.25f')


# Floats: Equality Testing

