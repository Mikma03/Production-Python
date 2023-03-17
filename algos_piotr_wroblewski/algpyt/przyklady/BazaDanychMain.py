from MojeTypy import BazaDanych as b
# ---------------------------------------------------------------------------------
# Przykłady użycia bazy danych osobowych
bazad=b.BazaDanych()
bazad.wstawSort("Kowalski", 2850)
bazad.wstawSort("Zarębski", 3100)
bazad.wstawSort("Fuks",     6700)
bazad.wstawSort("Nowak",    4000)
bazad.wstawSort("Konopek",  3350)
bazad.wypiszNieposortowane("Baza nieposortowana")
bazad.wypiszSortZarobk("Baza posortowana według zarobków")
bazad.wypiszSortNazw("Baza posortowana według nazwisk")
