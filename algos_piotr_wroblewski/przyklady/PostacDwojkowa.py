def post_dw(n):
    if(n!=0):
        post_dw(n//2)
        print(n % 2, end="")    # Reszta z dzielenia przez 2

print("66=", bin(66), ", wynik naszej funkcji:", end="")
post_dw(66)         # Wynik: 66= 0b1000010 , wynik naszej funkcji:1000010
print("\n179=", bin(179), ", wynik naszej funkcji:", end="")
post_dw(179)        # Wynik: 179= 0b10110011 , wynik naszej funkcji:10110011
print("\n4345=", bin(4345), ", wynik naszej funkcji:", end="")
post_dw(4345)       # Wynik:4345= 0b1000011111001 , wynik naszej funkcji:1000011111001

# Wersja z parametrem dodatkowym:
def post_dw_dod(x, res=0, pos=0):
    if(x>0):
        post_dw_dod( x//2, res + ((x%2) * pow(10, pos)),  pos+1)
    else:
        print(res, end="")
print("\n---------------")
print("\n4345=", bin(4345), ", wynik naszej funkcji:", end="")
post_dw_dod(4345)      # Wynik:4345= 0b1000011111001 , wynik naszej funkcji:1000011111001