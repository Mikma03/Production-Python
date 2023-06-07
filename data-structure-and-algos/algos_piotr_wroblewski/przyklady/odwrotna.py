a=0     # Zmienna globalna
b=0     # Zmienna globalna

def P1(a, b):
    if a==0:
        b=1
    else:
        b=P1(a-1, b)
        b=b+a
    return b

def P2():
    global a # Odwołanie do zmiennej globalnej
    global b # Odwołanie do zmiennej globalnej
    if a==0:
        b=1
    else:
        a=a-1
        P2()
        a=a+1
        b=b+a
# ---------------------------------------------------------------------
# Tu przetestujemy algorytmy

for i in range(17): # Wypiszemy ciąg dla wariantu P1(i, b=0)
    b=P1(i, b)
    print( str(b) + " ", end=" ")
print()
b=0
for i in range(17): # Wypiszemy ciąg dla wariantu P2(i, b=0)
    a=i
    P2()
    print(str(b) + " ", end=" ")
print()

"""
1  2  4  7  11  16  22  29  37  46  56  67  79  92  106  121  137  
1  2  4  7  11  16  22  29  37  46  56  67  79  92  106  121  137  
"""