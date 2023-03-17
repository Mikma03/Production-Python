def anagramy(zdanie1, zdanie2):
    print("s1=", zdanie2, ", s2=", zdanie1, end=", wynik: ")
    s1 = list(zdanie1) # Zamiana na listę znaków
    s2 = list(zdanie2) # jw.
    s1 = [e for e in s1 if e not in [' '] ] # Usuwamy spacje
    s2 = [e for e in s2 if e not in [' '] ] # jw.
    s1=sorted(s1) # Sortujemy znaki w s1
    s2=sorted(s2) # Sortujemy znaki w s2

    if s1==s2:
        print(", \t --> jest anagramem")
    else:
        print(", \t --> nie jest anagramem")

# --------------------------------------------------------------------------------------------------
# Klasyczny przykład to pytanie Piłata "Co to jest prawda?" i odpowiedź Jezusa "Człowiek, który stoi przed tobą":
anagramy ("quid est veritas","vir est qui adest")
anagramy ("baba","abba")
anagramy ("baba","abbe")