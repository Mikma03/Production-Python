

#########################################
# C1_S3
# Everything is an Object

a = 12
b = 12 
print(id(a))
print(id(b))


c = 500
d = 500
print(id(c))
print(id(d))


#########################################
# C1_S4
# Floats: Internal Representations

a = 0.1 + 0.1 + 0.1
b = 0.3 
a == b


format(0.1, '0.25f')