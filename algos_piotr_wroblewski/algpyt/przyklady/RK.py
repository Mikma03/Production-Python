p=33554393 			# Duża liczba pierwsza
MAX = 64		    # Liczba znaków alfabetu
# ------------------------------------------------------
def indeks(c):      # Konwersja znaku 'c' na indeksy w tablicy
  if c==' ':        # Uwaga: brak rzetelnej ochrony przed błędami!
      return 0      # (sprawdzam tylko kilka prostych warunków)
  elif c=='ę':
    return 53
  elif c =='Ę':
      return 54
  elif c == 'ł':
      return 55
  elif c == 'Ł':
      return 56
  # itd. itd. (miejsce na kolejne polskie znaki)
  elif (c >= 'a') and (c <= 'z'):
        return ord(c) - ord('a') +1     #   Od 1 do 25
  elif (c >= 'A') and (c <= 'Z'):
      return ord(c) - ord('A') + 27     #   Od 27 do 52
  else:
      print("Błędny znak!")
      return -1
# ------------------------------------------------
def rk(w, t):
    Hw = 0  # Funkcja H dla wzorca
    Ht = 0  # Funkcja H dla tekstu
    M=len(w)
    N=len(t)

    bM_1 = 1
    for i in range(1, M): # Wyliczymy wartość pow(MAX, M-1) % p
        bM_1= (MAX*bM_1) % p

    for i in range(M):
        Hw = (Hw * MAX + indeks( w[i]) ) % p  # Inicjacja funkcji H dla wzorca
        Ht = (Ht * MAX + indeks( t[i]) ) % p  # Inicjacja funkcji H dla tekstu
    i=0
    while Hw != Ht:     # Przesuwanie sie w tekscie
        if i+M >= N:
            return -1 # Porazka poszukiwan
        else:
            Ht = (Ht+MAX * p - indeks(t[i]   ) * bM_1) % p # (*)
            Ht = (Ht * MAX   + indeks(t[i+M])) % p
        i=i+1
    return i
# ------------------------------------------------
# Testujemy:

t="Z pamiętnika młodej lekarki"
#  012345678901234567890123456789
print(t)
print("012345678901234567890123456789")
print(f"Wynik/pozycja poszukiwań słowa 'lek'={rk('młodej', t)}")            # Wynik: 20
print(f"Wynik/pozycja poszukiwań słowa 'pa'={rk('pa', t)}")                 # Wynik: 2
print(f"Wynik/pozycja poszukiwań słowa 'parapet'=, {rk('parapet', t)}")     # Wynik: -1
print(f"Wynik/pozycja poszukiwań słowa 'młodej'={rk('młodej', t)}")         # Wynik: 13
print(f"Wynik/pozycja poszukiwań słowa 'koperta'= {rk('koperta', t)}")      # Wynik: -1
