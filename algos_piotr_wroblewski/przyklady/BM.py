K= 26*2 + 2*2 + 1    # Znaki ASCII + polskie litery + odstęp
shift=[None]*K       # Zmienna globalna
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
def init_shifts(w):
    global shift
    M=len(w)
    for i in range(K):
        shift[i]=M
    for i in range(M):
        shift[ indeks(w[i]) ] = M-i-1
# ------------------------------------------------
def bm(w, t):
    global shift
    init_shifts(w)
    N = len(t)
    M = len(w)
    i, j  = M - 1, M - 1
    while j>=0:
        while t[i]!=w[j]:
            x=shift[ indeks(t[i]) ]
            if M-j>x:
                i=i+M-j
            else:
                i=i+x
            if i>=N:
                return -1
            j=M-1
        i=i-1
        j=j-1
    return i+1

# ------------------------------------------------
# Testujemy:

t="Z pamiętnika młodej lekarki"
#  012345678901234567890123456789
print(t)
print("012345678901234567890123456789")
print(f"Wynik/pozycja poszukiwań słowa 'lek'={bm('lek', t)}")               # Wynik: 20
print(f"Wynik/pozycja poszukiwań słowa 'pa'={bm('pa', t)}")                 # Wynik: 2
print(f"Wynik/pozycja poszukiwań słowa 'parapet'=, {bm('parapet', t)}")     # Wynik: -1
print(f"Wynik/pozycja poszukiwań słowa 'młodej'={bm('młodej', t)}")         # Wynik: 13
print(f"Wynik/pozycja poszukiwań słowa 'koperta'= {bm('koperta', t)}")      # Wynik: -1
