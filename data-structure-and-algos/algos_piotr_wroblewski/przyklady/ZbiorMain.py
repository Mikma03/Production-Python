from MojeTypy import ZbiorLitery as z

z1=z.ZbiorLitery()
z2=z.ZbiorLitery()

z1.dodaj('A'), z1.dodaj('K'), z1.dodaj('K'), z1.dodaj('M')
z2.dodaj('B'), z2.dodaj('K'), z2.dodaj('R')
z1.wypisz("z1")
z2.wypisz("z2")
z1.usun('a')
z1.usun('X')
z1.wypisz("z1")
(z1+z2).wypisz("z1+z2")


