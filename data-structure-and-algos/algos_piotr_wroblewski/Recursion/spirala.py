from tkinter import *
okno=Tk()
okno.title(" Algorytmy w Pythonie - Spirala")
# Metoda geometry("width_size x height_size + x_position + y_position")
# width_size : szerokość
# height_size: wysokość
# x_position: przesuniecie poziome (w prawo)
# y_position: przesuniecie pionowe (w dół)
okno.geometry("550x400+500+60")

# Wartości domyślne
paramAlpha=20
paramLg=180

napisAlpha = Label(okno, text=" alpha=")         # Etykieta ' alpha='
napisAlpha.grid(column=0, row=1, padx=5, pady=5) # Odstęp 'pad' dookoła widgetu pozwala na odsunięcie go od brzegów komórki siatki
editAlpha = Entry(okno, width=6)                # Pole edycyjne 'Alpha'
editAlpha.insert(END, '20')                     # Wstawiamy w pole wartość domyślną "20"

editAlpha.grid(column=1, row=1)                     # Druga kolumna, drugi wiersz

napis2 = Label(okno, text=" lg=")                   # Etykieta 'lg='
napis2.grid(column=0, row=2)
editLg = Entry(okno, width=6)                       # Pole edycyjne 'lg'
editLg.insert(END, '180')                           # Wstawiamy wartość domyślną "180"
editLg.grid(column=1, row=2, padx=5, pady=5)

plotno = Canvas(bg="white", width=300, height=300)  # Pole rysowania (płótno)

def clickedCzysc():
    editAlpha.delete(0, END)           # Czyści zawartość pola editAlpha
    editLg.delete(0, END)              # Czyści zawartość pola editLg
    plotno.delete("all")  # Czyścimy pole rysowania

przyciskCzysc = Button(okno, text=" Czyść ", command=clickedCzysc)
przyciskCzysc.grid(column=1, row=0, padx=5, pady=5)


def rysuj_spirala(paramAlpha, paramLg, x, y):
    if (paramLg > 0 and paramLg > paramAlpha):
        plotno.create_line(x, y, x + paramLg, y)
        plotno.create_line(x + paramLg, y, x + paramLg, y + paramLg)
        plotno.create_line(x + paramLg, y + paramLg, x + paramAlpha, y + paramLg, dash=(3, 3))
        plotno.create_line(x + paramAlpha, y + paramLg, x + paramAlpha, y + paramAlpha)
        rysuj_spirala(paramAlpha, paramLg - 2 * paramAlpha, x + paramAlpha, y + paramAlpha)
    plotno.grid(column=2, row=2, padx=1, pady=1)

def clickedRysuj():
    plotno.delete("all")                # Czyścimy pole rysowania
    paramAlpha=int(editAlpha.get())     # Odczyt wartości Alpha
    paramLg=int(editLg.get())           # Odczyt wartości Lg
    print(paramLg, paramAlpha)
    rysuj_spirala(paramAlpha, paramLg, 5, 5)

przyciskRysuj = Button(okno, text=" Rysuj ", command=clickedRysuj)    # Przycisk 'Rysuj'
przyciskRysuj.grid(column=0, row=0)

okno.mainloop() # Jeśli zamkniesz okno, to przejdziesz poza tą instrukcję