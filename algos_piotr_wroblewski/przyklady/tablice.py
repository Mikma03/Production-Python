T1=[3, 4, 6]
T2=[6, 7, 8]
T3=[T1, T2]

print("T1=", T1)
print("T1=T3[0]=", T3[0])

print("T2=", T2)
print("T2=T3[1]=", T3[1])

print("T3=", T3)   # Wypisze [ [3, 4, 6], [6, 7, 8] ]

for i in range(2):          # Od 0 do 1
    for j in range(3):      # Od 0 do 2
        print(f"T3[{i}][{j}]={T3[i][j]}")
