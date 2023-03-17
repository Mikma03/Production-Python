def zawiera(wyraz, zdanie):
    print(f"Szukam '{wyraz}' w '{zdanie}'")
    n = len(wyraz)
    if n> len(zdanie):
        print("Poszukiwane słowo jest dłuższe niż zdanie...")
        return False
    wyraz_lst = list(wyraz) # Zamiana na listę znaków
    zdanie_lst = list(zdanie) # jw.

    print(len(zdanie_lst), "  ", zdanie_lst)  # Usuwamy znaki zawarte w  wyraz_lst ze zdania
    for e in wyraz_lst:
        try:
            zdanie_lst.remove(e)
        except ValueError:
            pass  # Nic nie robimy, gdy elementu nie ma

    print(len(zdanie_lst), "  ", zdanie_lst)
    print(len(wyraz_lst), "  ", wyraz_lst)

    return len(zdanie) - n == len(zdanie_lst)

# --------------------------------------------------------------------------------------------------
print ( zawiera("Bramka","Bronek alergicznie nie znosił makaronu z kaszą") )
print ( zawiera("Kia","Salon samochodów Renault i Nissan") )