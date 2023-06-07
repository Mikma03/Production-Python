def hanoi(n, a, b):
    if n==1:
        print(f"Przesuń dysk nr {n} z {a} na {b}")
    else:
        hanoi(n-1,a,3-a-b)
        print(f"Przesuń dysk nr {n} z {a} na {b}")
        hanoi(n-1,3-a-b,b)

print("Testujemy dla 3 krążków")
hanoi(3, 0, 1)
