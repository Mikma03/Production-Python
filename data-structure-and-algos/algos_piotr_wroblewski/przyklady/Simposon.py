N=4 # Liczba punktów = 2N+1
def simpson(f, a, b):
   # Funkcja zwraca całkę funkcji f(x) w przedziale [a,b],  której wartości sa podane tabelarycznie w 2N+1 punktach
   s=0
   h=(b-a)/(2.0*N)
   for i in range(0, 2*N, 2): # Od 0 do 2*N-1, skok co 2 punktu
      s=s+h*(f[i]+4*f[i+1]+f[i+2])/3.0
   return s
 # Testujemy:
f=[41, 29, 19, 11, 5, 1, -1, -1, 1]  # Tablica ma rozmiar 2*N+1 = 9
print("Wartość całki =", simpson(f,-5,3) ) # 82.66666666666667

