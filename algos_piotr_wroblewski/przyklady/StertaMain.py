from MojeTypy import Sterta as s

doctorsWho={
        37:     "William Hartnell",
        41:     "Patrick Troughton",
        26:     "Jon Pertwee",
        14:     "Tom Baker",
        19:     "Peter Davison",
        99:     "Colin Baker",
        23:     "Sylvester McCoy",
        17:     "Paul McGann",
        12:     "Christopher Eccleston",
        20:     "David Tennant",
        25:     "Matt Smith",
        42:     "Peter Capaldi",
        13:     "Jodie Whittaker"}

n=len(doctorsWho)
print("Lista aktorów grający w serii BBC 'Doctor Who' + umowny ranking preferencji:\n", doctorsWho)
s1=s.Sterta(n)

for key in doctorsWho:
    s1.wstaw(key)

s1.wypisz("Zawartość sterty (priorytety rankingu preferencji):")

print("Rozdanie nagród publiczności na podstawie preferencji:")

for i in range(1, n+1):
    x=s1.obsluz()
    print(f" Nagroda {i:9},    aktor: {doctorsWho[x]:20}   (ranking preferencji {x})")

s1.wypisz("Sterta po obsłudze:")
