# --- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
# Funkcje pomocnicze

def do_indeksu(c):  # Konwersja znaku 'c' na wartość 0... 25 dla liter z zakresu A... Z, 26 dla spacji i 27 dla znaku '-' (minus)
  if ((c >= 'A') and (c <= 'Z') or (c >= 'a') and (c <= 'z')):
     return ord(c.upper()) -ord('A')	# Zamiana na dużą literę realizowana przez metodę upper(), kod 'A' to 65
  elif c==' ':
     return 26
  elif c=='-':
    return 27
  else:
    return 99  # Błąd zakresu (znak spoza alfabetu)

def z_indeksu(n):  # Konwersja indeksu z zakresu 0… 27 na odpowiedni znak alfabetu
  if (n >= 0) and (n <= ord('Z') - ord('A')):
      return chr(n + ord('A'))
  elif n==26:
      return ' '
  elif n==27:
      return '-'
  else:
    return '@'  # Umowny kod błędu (nierozpoznany znak)
# --- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
ROZM = 29  # Rozmiar alfabetu

class USS:
    def __init__(self):
        self.t=[None for x in range(ROZM)]  # W tablicy będziemy zapisywali referencje do obiektów USS

    def zapisz(self, slowo):
        #  Zmienna pomocnicza pozwoli nawigować po drzewie wskazywanym przez referencję do własnego obiektu (self)
        p=self
        print("Dodaję słowo:[" + slowo + "]. ")
        for i in range (1, len(slowo)+1):
           pos=do_indeksu(slowo[i-1])
           if (p.t[pos] != None):
               p=p.t[pos]
           else:
              q=USS()
              p.t[pos]=q
              for k in range(ROZM):
                  q.t[k]=None
              p=q
        p.t[ROZM-1]=p  	# Pętla jako koniec słowa

    def pisz_slownik(self):
        for i in range(ROZM):
           if (self.t[i] != None):
               if ( (self.t[i]).t[ROZM-1] == self.t[i]):
                   print(z_indeksu(i))  # Gdy koniec słowa to pisz znak końca linii
               else:
                   print(z_indeksu(i), end=" ")
                   print("---", end=" ") # Aby ładniej wyglądało na konsoli tekstowej...
                   (self.t[i]).pisz_slownik() # Wypisz rekurencyjnie resztę

    def szukaj(self, slowo):    # Wyszukuje słowo w drzewie (słowniku)
        Szukam=True
        i=0
        p=self  # Zmienna pomocnicza pozwoli nawigować po drzewie wskazywanym przez referencję do własnego obiektu (self)
        print("Szukane słowo:[" + slowo + "]: ", end=" ")

        while Szukam==True and i< len(slowo):
            if (p.t[ do_indeksu(slowo[i]) ]==None):
                Szukam=False    # Brak odgałęzienia, słowa nie ma!
            else:
                p=p.t[do_indeksu(slowo[i])] # Szukamy dalej
                i=i+1

        if ( (i==len(slowo) ) and (p.t[ROZM-1]==p) and Szukam==True):
            print("Słowo znalezione!")
        else:
            print("Słowo nie zostało znalezione w słowniku")

# Proba bezpośredniego wywołania modułu
if __name__ == "__main__":
	print("To jest moduł biblioteczny, aby przetestować wywołaj plik:", "USSMain.py!")
