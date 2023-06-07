def hanoi2(n, a, b):
    while n!=1:
        hanoi2(n-1,a,3-a-b)
        print(f"Przesuń dysk nr {n} z {a} na {b}")
        n=n-1
        a=3-a-b
    print(f"Przesuń dysk nr {n} z {a} na {b}")


# Testujemy
print("Testujemy dla 4 krążków")
hanoi2(4, 0, 1)
