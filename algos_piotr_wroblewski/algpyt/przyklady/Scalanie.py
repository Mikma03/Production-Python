def scalaj(T1, T2): # # Scalanie posortowanych tablic T1 i T2 do T3
	N=len(T1)
	M=len(T2)
	T3=[None] * (N+M)     # Pusta (na razie) tablica
	i, j, k =  0, 0, 0    # Wskaźniki pozycyjne potrzebne do nawigowania po T2 i T2
	while i < N and j < M: # Progresywnie przesuwamy się wzdłuż tablicy T1 lub T2 kopiując większy element do T3
		if T1[i] < T2[j]:
			T3[k] = T1[i]
			k, i = k + 1, i + 1
		else:
			T3[k] = T2[j]
			k, j = k + 1, j + 1
	while i < N: # Przekopiujmy pozostałości T1
		T3[k] = T1[i]
		k, i = k + 1, i + 1
	while j < M:
		T3[k]=T2[j]
		k, j  = k + 1, j + 1
	return T3
# Testujemy:

T1 = [-4, -2, 0, 4, 6, 8, 9, 11]
T2 = [2, 3, 4, 5, 5, 6, 7, 12, 13, 14, 16, 19]
T3 = scalaj(T1, T2)

print(T1)
print(T2)
print(T3)
