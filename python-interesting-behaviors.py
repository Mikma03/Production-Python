
#########################################
# Everything is an Object

a = 12
b = 12
print(id(a))  # same as id(b) because of the way Python caches integers
print(id(b))  # same as id(a) because of the way Python caches integers


c = 500
d = 500
print(id(c))  # different from id(d) because of the way Python caches integers
print(id(d))  # different from id(c) because of the way Python caches integers


#########################################
# Floats: Internal Representations

a = 0.1 + 0.1 + 0.1
b = 0.3
# False (not True) because of rounding errors in floating point numbers (IEEE 754)
a == b

format(0.1, '0.25f')  # '0.1000000000000000055511151'


#########################################
# Floats: Internal Representations

(0.125).as_integer_ratio()  # (1, 8)

(0.1).as_integer_ratio()  # (3602879701896397, 36028797018963968)

#########################################
# Operator Precedence

-2 ** 4  # -16 (not 16) because of operator precedence

(-2) ** 4  # 16 (as expected)
