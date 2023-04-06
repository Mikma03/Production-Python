# Stałe symboliczne, które użyjemy do oznaczania stanu zajętości pola gry
nic, komputer, czlowiek = 1,2, 3

plus_niesk  =  1000
minus_niesk = -1000
GLEBOKOSC_OK=2
# -------------------------------------------------------------------------------------
class KANDYDACI:    # Pomocnicza struktura zapamiętująca możliwe kandydatury na następny ruch
    def __init__(self):
        self.cpt=-9   # Pole dostępne
        self.tbl = [0] * 9
# -------------------------------------------------------------------------------------
class POLE: # Pomocnicza struktura służąca do czytelnego zwracania przez metodę MiniMax wartości złożonej (dwie wartości)
    def __init__(self):
        self.val=0
        self.gracz=0
# -------------------------------------------------------------------------------------
def Nastepny_Gracz(gracz):
     if gracz==komputer:
         return czlowiek
     else:
         return komputer
# -------------------------------------------------------------------------------------
def NastepnyGracz(gracz, glebokosc):    # Dla którego gracza wykonujemy ewaluację mini-max?
    if (glebokosc % 2) == 0:
        return gracz
    else:
        return Nastepny_Gracz(gracz)
# -------------------------------------------------------------------------------------
def WystarczajaGleboko(p):  # Czy głębokość MiniMax jest OK
    if p==GLEBOKOSC_OK:
        return True
    else:
        return False
# -------------------------------------------------------------------------------------
def WyswietlPlansze(plansza):
    for i in range(9):
        if i==3 or i==6:
            print()
        if plansza[i]==nic:
            print(" *  ", end="")
            continue
        elif plansza[i]==komputer:
            print(" X  ", end="")
            continue
        elif plansza[i]==czlowiek:
            print(" O  ", end="")
            continue
    print("\n")
# -------------------------------------------------------------------------------------
def Zeruj(plansza): # Zerujemy teren gry
    for i in range(9):
        plansza[i]=nic
# -------------------------------------------------------------------------------------
def Generuj(plansza):  # Generuje możliwe kandydatury następnego ruchu
    t = KANDYDACI()
    t.cpt=-1
    for i in range(9):
        if plansza[i]==nic:
            t.cpt =  t.cpt+1
            t.tbl[t.cpt]=i     # Zapamiętanie wolnej pozycji
    return t
# -------------------------------------------------------------------------------------
def KoniecGry(plansza):
  #  Sukces w linii?
    a=((plansza[0]==plansza[1]) and (plansza[1]==plansza[2]) and (plansza[0]!=nic))
    b=((plansza[3]==plansza[4]) and (plansza[4]==plansza[5]) and (plansza[3]!=nic))
    c=((plansza[6]==plansza[7]) and (plansza[7]==plansza[8]) and (plansza[6]!=nic))
  # Sukces w kolumnie?
    d=((plansza[0]==plansza[3]) and (plansza[3]==plansza[6]) and (plansza[0]!=nic))
    e=((plansza[1]==plansza[4]) and (plansza[4]==plansza[7]) and (plansza[1]!=nic))
    f=((plansza[2]==plansza[5]) and (plansza[5]==plansza[8]) and (plansza[2]!=nic))
  # Sukces na przekątnej
    g=((plansza[0]==plansza[4]) and (plansza[4]==plansza[8]) and (plansza[0]!=nic))
    h=((plansza[2]==plansza[4]) and (plansza[4]==plansza[6]) and (plansza[2]!=nic))

  # Robimy to aby wiedzieć kto wygrał:
    if not (a or b or c or d or e or f or g or h):
        return 0
    if a : return 1
    if b : return 3
    if c : return 6
    if d : return 3
    if e : return 4
    if f : return 5
    if g : return 4
    if h : return 4
# -------------------------------------------------------------------------------------
def SprawdzCzyKoniecGry(plansza, gracz):
    if KoniecGry(plansza):
        WyswietlPlansze(plansza)
        print("\n  ** KONIEC GRY ** ")
        if gracz==czlowiek:
            print(":) WYGRAŁEŚ, GRATULACJE!")
        else:
            print(":-( WYGRAŁ KOMPUTER...")
        input("Naciśnij dowolny klawisz...")
        return True
    nastepni=Generuj(plansza)
    if nastepni.cpt==-1:
        WyswietlPlansze(plansza)
        print("\n  ** KONIEC GRY ** ")
        print("Remis!")
        input("Naciśnij dowolny klawisz...")
        return True
    return False
# -------------------------------------------------------------------------------------
def LiniaPusta(Line, plansza):
    return ((plansza[(Line-1)*3]==nic) and (plansza[(Line-1)*3+1]==nic) and (plansza[(Line-1)*3+2]==nic))
#  ____________________________________________________________________
def KolumnaPusta(Col, plansza):
    return ((plansza[Col-1]==nic) and (plansza[(Col-1)+3]==nic) and (plansza[(Col-1)+6]==nic))
# ____________________________________________________________________
def LiniaPelna(Line, plansza):
    return not((plansza[(Line-1)*3]==nic) or (plansza[(Line-1)*3+1]==nic) or (plansza[(Line-1)*3+2]==nic))
#  ____________________________________________________________________
def KolumnaPelna(Col, plansza):
    return not ((plansza[Col-1]==nic) or (plansza[(Col-1)+3]==nic) or (plansza[(Col-1)+6]==nic))
#  ____________________________________________________________________
def Przekatna1_Pusta(plansza):
    return ((plansza[0]==nic) and (plansza[4]==nic) and (plansza[8]==nic))
# ____________________________________________________________________
def Przekatna1_Pelna(plansza):
    return not((plansza[0]==nic) or (plansza[4]==nic) or (plansza[8]==nic))
# ____________________________________________________________________
def Przekatna2_Pusta(plansza):
    return ((plansza[2]==nic) and (plansza[4]==nic) and (plansza[6]==nic))
# ____________________________________________________________________
def Przekatna2_Pelna (plansza):
    return not ((plansza[2]==nic) or (plansza[4]==nic) or (plansza[6]==nic))
# -------------------------------------------------------------------------------------
def Ewaluacja(plansza, gracz):
    val=0
    result=KoniecGry(plansza)
    if result!=0:
        if (plansza[result]==Nastepny_Gracz(gracz)):
            return minus_niesk  # Pozycja wygrywająca dla przeciwnika
        else:
            return  plus_niesk   # Pozycja wygrywająca dla nas

    for Line in range(1,4):
        if not (LiniaPusta(Line,plansza) or LiniaPelna(Line,plansza)):
            if ((plansza[(Line-1)*3]==Nastepny_Gracz(gracz)) or (plansza[(Line-1)*3+1]==Nastepny_Gracz(gracz)) or (plansza[(Line-1)*3+2]==Nastepny_Gracz(gracz))):
                val=val-1
            if ((plansza[(Line-1)*3]==gracz) or (plansza[(Line-1)*3+1]==gracz) or (plansza[(Line-1)*3+2]==gracz)):
                val=val+1
    for Col in range (1, 4):
        if not (KolumnaPusta(Col, plansza) or KolumnaPelna(Col,plansza)):
            if ((plansza[Col-1]==Nastepny_Gracz(gracz)) or (plansza[(Col-1)+3]==Nastepny_Gracz(gracz)) or (plansza[(Col-1)+6]==Nastepny_Gracz(gracz))):
                val=val-1
            if ((plansza[Col-1]==gracz) or (plansza[(Col-1)+3]==gracz) or (plansza[(Col-1)+6]==gracz)):
                val=val+1
    if (not(Przekatna1_Pusta(plansza) or Przekatna1_Pelna(plansza))):
        if ((plansza[0]==Nastepny_Gracz(gracz)) or (plansza[4]==Nastepny_Gracz(gracz)) or (plansza[8]==Nastepny_Gracz(gracz))):
           val=val-1
        if ((plansza[0]==gracz) or (plansza[4]==gracz) or (plansza[8]==gracz)):
            val=val+1
    if (not(Przekatna2_Pusta(plansza) or Przekatna2_Pelna(plansza))) :
        if ((plansza[2]==Nastepny_Gracz(gracz)) or (plansza[4]==Nastepny_Gracz(gracz)) or (plansza[6]==Nastepny_Gracz(gracz))):
            val=val-1
        if ((plansza[2]==gracz) or (plansza[4]==gracz) or (plansza[6]==gracz)):
            val=val+1
    return val
# -------------------------------------------------------------------------------------
def WykonajRuch(gracz, plansza, ruch):
    plansza[ruch]=gracz
# -------------------------------------------------------------------------------------
def MiniMax(plansza, glebokosc, gracz):
    res = POLE()
    if WystarczajaGleboko(glebokosc):   # Węzeł uznawany za położony dostatecznie głęboko
        res.val=Ewaluacja(plansza, gracz)
        res.gracz=-1
        return res
    nastepni=Generuj(plansza)
    if (nastepni.cpt==-1): # Węzeł terminalny
        res.val = Ewaluacja(plansza, gracz)
        res.gracz = -1
        return res
    lepszy=minus_niesk
    gracz_1=int()
    plansza1 = [nic] *9
    for i in range(9):
        for k in range(9):
            plansza1[k]=plansza[k]
        plansza1[nastepni.tbl[i]]=NastepnyGracz(gracz,glebokosc)
        r = MiniMax(plansza1, glebokosc+1, gracz)
        if (-r.val > lepszy):
            lepszy = -r.val
            gracz_1=nastepni.tbl[i]
    res.val=lepszy
    res.gracz=gracz_1
    return res

# -------------------------------------------------------------------------------------
def Zajete(plansza, ruch):  # Pole wolne?
    if (ruch==-1):
        return True
    if (plansza[ruch] != nic):
        return False
    else:
        return True
# -------------------------------------------------------------------------------------
def WybierzRuch(gracz, plansza):   # Wybór ruchu zależy od tego, kto gra
    ruch=int()
    if (gracz==czlowiek):  # Gra człowiek, musimy pobrać poprawny wybór (pole nie może być zajęte)
            # Gracz kontra komputer
        while True:
            try:
                ruch = int(input("\n Twój wybór(0... 8): "))
                if ruch not in range(0, 9):
                    print("Błędny wybór!")
                    continue
                else:
                    break
            except ValueError:
                print(f"Ups, {ruch} nie jest poprawny... Próbuj dalej.")
            if Zajete(plansza, ruch):
                continue
    else: # Gra komputer
        wybor=MiniMax(plansza, 0, gracz)
        ruch=wybor.gracz
        print("\nMój ruch: ", ruch)
    return ruch
# -------------------------------------------------------------------------------------

def Graj(plansza, gracz):
    koniec = False
    gracz1=gracz
    while not koniec:
        WyswietlPlansze(plansza)
        ruch=WybierzRuch(gracz1, plansza)
        if (ruch!=-1):
            WykonajRuch(gracz1, plansza, ruch)
        koniec = SprawdzCzyKoniecGry(plansza, gracz1)
        gracz1=Nastepny_Gracz(gracz1)
# -------------------------------------------------------------------------------------
# Testujemy
plansza= [0] * 9
print("Kodowanie pól planszy:")
print(" 0 1 2\n 3 4 5\n 6 7 8\n")
print("Zaczynamy:")
Zeruj(plansza)
#gracz=komputer
gracz=czlowiek  # Lub gracz=komputer — ten zapis wskazuje, kto zaczyna grę
Graj(plansza, gracz)
input("Naciśnij dowolny klawisz...")