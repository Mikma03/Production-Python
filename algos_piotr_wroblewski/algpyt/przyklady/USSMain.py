from MojeTypy import USS as u

p=u.USS()       # Tworzymy nowy słownik i wpisujemy kilka haseł
for s in ["alf", "alfabet", "alfabetycznie", "anagram", "anonim", "Bal", "ASTRonoMIa", "Ankara", "Balon", "Cena"]:
    p.zapisz(s)
p.pisz_slownik() # Wypisujemy słownik
# Szukamy kilku haseł
for s in ["anagram", "anagramy", "gra", "alf", "ALF", "dom", "cwaniak", "bal"]:
    p.szukaj(s)