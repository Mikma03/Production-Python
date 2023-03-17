x="Hejka"
tab = [2,3, 'Hejka']
print (x in tab)    # Wypisze True, gdyż napis "Hejka" znajduje się w tablicy 'tab'

A = 20
B = 20
if A > B:           # Uwaga: poniżej, po dwukropku musisz zastosować wcięcie!
    print("A jest większe od B")
elif A == B:        # Jeśli poprzednio testowany warunek nie okazał się prawdziwy, spróbuj kolejnego
    print("A jest równe B")
else:               # Jeśli poprzednie warunki nie zostały spełnione, to:
    print("Skończyły mi się pomysły...")

jezyki = ["C++", "Python", "Java"]

for x in jezyki:
   if x == "Python":
        print("Znalazłem Pythona!")
   else:
        print(f"Znalazłem język {x}")


