from MojeTypy import Sterta as s
tab=[40, 2, 1, 6, 18, 29, 29, 32, 23, 34, 91, 45, 6]
print(tab)                        # [40, 2, 1, 6, 18, 29, 29, 32, 23, 34, 91, 45, 6]
sterta=s.Sterta( len(tab))
for element in tab:
    sterta.wstaw(element)
for i in range(len(tab)-1, -1, -1):
    tab[i]= sterta.obsluz()       # Pobierany największy element zapisujemy na końcu
print(tab)                        # [1, 2, 6, 6, 18, 23, 29, 29, 32, 34, 40, 45, 91]