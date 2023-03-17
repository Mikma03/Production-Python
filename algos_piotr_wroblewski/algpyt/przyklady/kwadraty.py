from tkinter import *
okno=Tk()
okno.title(" Algorytmy w Pythonie - Kwadraty")
okno.geometry("600x450+500+60")
paramN, paramLg, parX, parY= 6, 250, 15, 15 # # Wartości domyślne

napisN = Label(okno, text=" N=")             # Etykieta 'N='
napisN.grid(column=0, row=1, padx=5, pady=5) # Odstęp 'pad' dookoła widgetu pozwala na odsunięcie go od brzegów komórki siatki
editN = Entry(okno, width=6)                 # Pole edycyjne 'Alpha'
editN.insert(END, '6')                       # Wstawiamy w pole wartość domyślną "6"
editN.grid(column=1, row=1)                  # Druga kolumna, drugi wiersz

napis2 = Label(okno, text=" lg=")            # Etykieta 'lg='
napis2.grid(column=0, row=2)
editLg = Entry(okno, width=6)                # Pole edycyjne 'lg'
editLg.insert(END, '240')                    # Wstawiamy wartość domyślną "240"
editLg.grid(column=1, row=2, padx=5, pady=5)

napis3 = Label(okno, text=" x=")             # Etykieta 'x='
napis3.grid(column=3, row=1)
editX = Entry(okno, width=6)                 # Pole edycyjne 'y'
editX.insert(END, '15')                      # Wstawiamy wartość domyślną "15"
editX.grid(column=4, row=1, padx=5, pady=5)

napis4 = Label(okno, text=" y=")                   # Etykieta 'y='
napis4.grid(column=3, row=2)
editY = Entry(okno, width=6)                       # Pole edycyjne 'y'
editY.insert(END, '15')                           # Wstawiamy wartość domyślną "15"
editY.grid(column=4, row=2, padx=5, pady=5)
plotno = Canvas(bg="white", width=300, height=300)  # Pole rysowania (płótno)

def clickedCzysc():
    editN.delete(0, END)           # Czyści zawartość pola editAlpha
    editLg.delete(0, END)          # Czyści zawartość pola editLg
    editX.delete(0, END)           # Czyści zawartość pola editX
    editY.delete(0, END)  # Czyści zawartość pola editY
    plotno.delete("all")  # Czyścimy pole rysowania

przyciskCzysc = Button(okno, text=" Czyść ", command=clickedCzysc)
przyciskCzysc.grid(column=1, row=0, padx=5, pady=5)

def rysuj_kwadraty(paramN, paramLg, x, y):
    if (paramN > 0):
        plotno.create_line(x, y, x + paramLg, y)
        plotno.create_line(x + paramLg, y, x + paramLg, y + paramLg)
        plotno.create_line(x + paramLg, y + paramLg, x, y + paramLg)
        plotno.create_line(x, y + paramLg, x, y + paramLg / 2)
        plotno.create_line(x, y + paramLg / 2, x + paramLg / 2, y + paramLg)
        plotno.create_line(x + paramLg / 2, y + paramLg, x + paramLg, y + paramLg / 2)
        plotno.create_line(x + paramLg, y + paramLg / 2, x + paramLg / 2, y)
        plotno.create_line(x + paramLg / 2, y, x + paramLg / 4, y + paramLg / 4)
        rysuj_kwadraty(paramN - 1, paramLg / 2, x + paramLg / 4, y + paramLg / 4)
        plotno.create_line(x + paramLg / 4, y + paramLg / 4, x, y + paramLg / 2)
        plotno.create_line(x, y + paramLg / 2, x, y)

    plotno.grid(column=5, row=3, padx=1, pady=1)

def clickedRysuj():
    plotno.delete("all")        # Czyścimy pole rysowania
    paramN=int(editN.get())     # Odczyt wartości N
    paramLg=int(editLg.get())   # Odczyt wartości Lg
    parX = int(editX.get())     # Odczyt wartości X
    parY = int(editY.get())     # Odczyt wartości Y

    print(paramLg, paramN, parX, parY)
    rysuj_kwadraty(paramN, paramLg, parX, parY)
przyciskRysuj = Button(okno, text=" Rysuj ", command=clickedRysuj)    # Przycisk 'Rysuj'
przyciskRysuj.grid(column=0, row=0)

okno.mainloop() # Jeśli zamkniesz okno, to przejdziesz poza tą instrukcję