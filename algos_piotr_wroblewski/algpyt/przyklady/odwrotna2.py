a=0
b=0

def P2bis():
    global a
    global b
    if a!=0:
        a=a-1
        P2bis()
        a=a+1
        b=b+a
    else:
        b=1

def P2_ITERAT():
    global a
    global b
    k=0
    while (a!=0):
         a=a-1
         k=k+1
    b=1
    while k!=0:
        a=a+1
        b=b+a
        k=k-1

# ---------------------------------------------------------------------
# Tu przetestujemy algorytmy

for i in range (0, 17):
    #global a
    a=i
    P2bis()
    print(b, "  ", end="")

print("\n")

for i in range (0, 17):
    #global a
    a=i
    P2_ITERAT()
    print(b, "  ", end="")

print("\n")
"""
1  2  4  7  11  16  22  29  37  46  56  67  79  92  106  121  137  
1  2  4  7  11  16  22  29  37  46  56  67  79  92  106  121  137  
"""