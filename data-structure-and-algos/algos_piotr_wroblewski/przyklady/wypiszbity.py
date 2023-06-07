def showbits(s): # Funkcja pokazuje reprezentację binarną liczby
    print(f"{s:3}=", end="")        # Wymusza pomijanie znaku końca linii użyciu 'print'
    wagi=[1,2,4,8,16,32,64,128]     # Maska bitu wagi (ograniczmy się do 8)
    for i in range(7, -1, -1):      # Od 7. do 0. (pętla odliczająca wstecz, patrz -1)
        bit = wagi[i] & s           # Operacja bitowa AND
        if (bit !=0 ):
            print("1", end ="")
        else:
            print("0",  end ="")
    print()

showbits(6)
showbits(13)
showbits(245)

