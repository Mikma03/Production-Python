N=5
nastepny=[-1, -1, -1, -1, -1] # Tablica 'nastepny' Zapamiętuje ostatni wybór,  na samym początku nastepny[-1+1]=0,
                              # później posuwamy się o 1 pozycję dalej podczas danego etapu wyboru
dobor=[-1, -1, -1, -1, -1]    # Tu wyliczymy docelowe rozwiązanie zadania
wybiera= [
	      [0, 4, 3, 2, 1],  # A
	      [1, 0, 4, 2, 3],  # B
	      [0, 3, 1, 2, 4],  # C
	      [3, 4, 0, 1, 2],  # D
	      [4, 3, 2, 1, 0] ] # E
# Preferencje promotorów: lubi[i][0] = nr A na liście 'i',  lubi[i][1] = nr B na liście 'i' itd.
lubi=[ # A  B  C  D  E
	    [3, 4, 0, 2, 1],
        [2, 1, 3, 4, 0],
		[0, 1, 2, 4, 3],
		[4, 3, 2, 0, 1],
		[2, 3, 4, 0, 1] ]
# W trakcie progresji algorytmu będziemy używali zmiennych typu integer: student, wybierajacy, promotor, odrzucony
# Konwersję wartości całkowitej zapisanej w tablicy na odpowiadający jej znak 'A', ... 'E' zapewniają funkcje chr() i ord()
for student in range(N):
	wybierajacy=student
	print("Wybierającym staje się ", chr (wybierajacy +ord('A')) )
	while wybierajacy!=-1:
		nastepny[wybierajacy]=nastepny[wybierajacy]+1
		promotor=wybiera[wybierajacy][nastepny[wybierajacy]]
		print("-->próbuje on tematu (promotora) ", promotor)
		if dobor[promotor]==-1:	# Promotor (i jego temat) jest wolny
			print("Temat (promotor) ", promotor, " był wolny i zostaje on przyznany studentowi ", chr ( (wybierajacy +ord('A'))))
			dobor[promotor]=wybierajacy
			wybierajacy=-1
		else:
			if lubi[promotor][wybierajacy]<lubi[promotor][dobor[promotor]]:
				odrzucony=dobor[promotor]
				print("Promotor ", promotor, " porzuca swój aktualny wybór ", chr ( odrzucony + ord('A')), end =" ")
				print(" na rzecz ", chr (wybierajacy + ord('A')), end=" ")
				dobor[promotor]=wybierajacy
				wybierajacy=odrzucony
				print("  --- Wybierającym staje się ", chr ( wybierajacy + ord('A') ))
print("Wyniki:")
for i in range(N):
	print("Promotor ", i, ", student ",   chr ( dobor[i]+ ord('A') ) )



