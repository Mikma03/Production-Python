from matplotlib import pyplot as plt
kategorie = ['Samoloty', 'Czołgi', 'Wozy bojowe', 'Helikoptery']
wyniki = [99, 509, 1556, 123]
statystyki = plt.bar(kategorie, wyniki, color='k')
plt.title("Straty wojenne agresora - 1. kwartał 2022")
plt.xlabel("Kategorie")
plt.ylabel("Wyniki")
plt.show()
