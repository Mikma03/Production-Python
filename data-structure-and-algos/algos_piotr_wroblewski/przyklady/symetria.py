def symetria1 (x):
    if x==0:
        print("-", end=" ")
    else:
        print("<", end=" ")
        symetria1(x-1)
        print(">", end=" ")

def symetria2(x):
    for i in range(x):
        print("<", end=" ")
    print("-", end=" ")
    for i in range(x):
        print(">", end=" ")

symetria1(5)
print()
symetria2(5)