class Element:
  def __init__(self, pDane = None, pNastepny=None):
    self.dane = pDane
    self.nastepny = pNastepny

class Lista:        # Nowa lista jest pusta (referencja 'None')
  def __init__(self):
    self.glowa = None
    self.ogon = None

l = Lista()     # Tworzymy pustą  listę
q=Element(3)
l.glowa = q     # Wstawiamy nowy element 'q' na koniec listy
l.ogon  = q

r= Element(5)
q.nastepny= r   # Wstawiamy kolejny nowy element na koniec...
l.ogon    = r   # Aktualizujemy odsyłacz do konńca listy

# Procedura poszukiwania elementu:

szukany_element=5

adres_tmp=l.glowa
while adres_tmp!= None:
  if adres_tmp.dane==szukany_element:
      print("Znalazłem poszukiwany element")
      break
  adres_tmp=adres_tmp.nastepny

if adres_tmp == None:
    print("Nie znaleziono poszukiwanego elementu")
