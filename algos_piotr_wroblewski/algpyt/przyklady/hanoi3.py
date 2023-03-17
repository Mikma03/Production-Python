a, b, n = 0,0,0
def hanoi():
	global a
	global b
	global n
	if  n!=1:
		n=n-1
		b=3-a-b
		hanoi()
		n=n+1
		b=3-a-b
		print(f" Przesuń dysk nr {n} z {a} na {b}")
		n=n-1
		a=3-a-b
		hanoi()
		n=n+1
		a=3-a-b
	else:
		print(f" Przesuń dysk nr {n} z {a} na {b}")

def hanoiIter():
	global a
	global b
	global n
	M=1
	while True:
		while (n!=1):
			n=n-1
			b=3-a-b
			M=M*2
		print(f" Przesuń dysk nr {n} z {a} na {b}")
		while (M!=1) and (M%2==1):
			M=M//2
			n=n+1
			a=3-a-b
		if M==1:
				break
		M=M+1
		n=n+1
		b=3-a-b
		print(f" Przesuń dysk nr {n} z {a} na {b}")
		n=n-1
		a=3-a-b
		if M==1:
			break


# Tu przetestujemy algorytmy
print("Klasycznie:")
n, a, b = 3, 0, 1
hanoi()
print("Iteracyjnie:")
n, a, b = 3, 0, 1
hanoiIter()

"""
n, a, b = 3, 0, 1:

Przesuń dysk nr 1 z 0 na 1
Przesuń dysk nr 2 z 0 na 2
Przesuń dysk nr 1 z 1 na 2
Przesuń dysk nr 3 z 0 na 1
Przesuń dysk nr 1 z 2 na 0
Przesuń dysk nr 2 z 2 na 1
Przesuń dysk nr 1 z 0 na 1

"""