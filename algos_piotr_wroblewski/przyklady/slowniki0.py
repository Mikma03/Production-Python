# Przykładowe operacje na słownikach Pythona

doctorsWho={
        "Pierwszy": "William Hartnell",
        "2":        "Patrick Troughton",
        "3":        "Jon Pertwee",
        "4":        "Tom Baker",
        "5":        "Peter Davison",
        "6":        "Colin Baker",
        "7":        "Sylvester McCoy",
        "8":        "Paul McGann",
        "9":        "Christopher Eccleston",
         10:       "David Tennant",
        "11":       "Matt Smith",
        "12":       "Peter Capaldi",
        "Trzynasta": "Jodie Whittaker"}

# Iterowanie przez kolekcję danych zapisanych w słowniku

for key in doctorsWho:
    print(f" {key}  -   {doctorsWho[key]}")

print(doctorsWho[10])              # Wypisze: David Tennant
print(doctorsWho["Trzynasta"])     # Wypisze: Jodie Whittaker

#print(doctorsWho["Trzynasty"])     # Zgłosi wyjątek: KeyError

print ("Kowalski" in doctorsWho)    # False

# Kasowanie wpisu

del doctorsWho["Pierwszy"] # Lub: doctorsWho.pop("Pierwszy1")


# Pobieranie wartości na podstawie klucza:

print("Wartość dla klucza numerycznego 10:", doctorsWho.get(10))

print("Aktor grający doktora w Serii 15:", doctorsWho.get(15, "Nie ma takiej serii Doktor Who"))

# Aktualizacja danych

doctorsWho.update( { "15":"Jan Kowalski" } )
print("Dodano wpis dla klucza '15'",doctorsWho["15"])
print("Aktualizacja wartości dla klucza '7'")
doctorsWho.update( {"7":"Sylwek McCoy" } )   # lub: doctorsWho["7"]="Sylwek McCoy"
print("Doktor Who dla serii 7.:",doctorsWho["7"])

print ("Surowa zawartość słownika:")


print(doctorsWho)






