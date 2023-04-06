mojNapis="Cześć"         # Jakaś zmienna tekstowa (*)
mojNapis2=mojNapis       # mojNapis2 jest tylko referencją do obiektu "Napis"!

print("mojNapis =",mojNapis)
print("mojNapis2=",mojNapis2)

print ("Wynik porównania 'mojNapis is MojNapis2': ", mojNapis is mojNapis2)
print("adres mojNapis=", id(mojNapis))
print("adres mojNapis2",id(mojNapis2))
print("Drugi znak ciągu mojNapis:", mojNapis[1])
mojNapis2=mojNapis[1]+mojNapis2 # Tworzymy nowy obiekt zawierający ciąg 'zCześć' (**)
print("mojNapis =",mojNapis,  "(czyli: mojNapis)")              # Wypisze: mojNapis  = Cześć
print("mojNapis2=",mojNapis2, "(czyli: mojNapis[1]+mojNapis2)") # Wypisze: mojNapis2 = zCześć

print("Adres starego obiektu mojNapis= ", id(mojNapis))  # "stary" obiekt, utworzony w linii (*)
print("Adres nowego obiektu mojNapis2= ", id(mojNapis2)) # "nowy" obiekt, utworzony w linii (**)
