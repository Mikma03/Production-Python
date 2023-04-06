def koduj(napis, N):
    res = ""
    for i in range( len(napis) ):
        c = napis[i]      # Kodujemy znak po znaku
        if (c.isupper()): # Duża litera
            res = res + chr( (ord(c) + N - ord('A')) % 26 + ord ('A') )
        else: # Mała litera
            res = res + chr( (ord(c) + N - ord('a')) % 26 + ord('a') )
    return res

def dekoduj(napis, N):
    res = ""
    for i in range( len(napis) ):
        c = napis[i]      # Kodujemy znak po znaku
        if (c.isupper()): # Duża litera
            res = res + chr( (ord(c) - N - ord('A')) % 26 + ord ('A') )
        else: # Mała litera
            res = res + chr( (ord(c) - N - ord('a')) % 26 + ord('a') )
    return res

oryginal    = "WARINUKRAINE"
zakodowany  =  koduj(oryginal, 4)
odkodowany = dekoduj(zakodowany, 4)
print(oryginal)
print(zakodowany)
print(odkodowany)

tajnykod='GLAEPEYOVEMRMI'
print("Próba złamania kodu:", tajnykod)
for i in range(26):
    zgadujemy=dekoduj(tajnykod, i)
    print(zgadujemy)
