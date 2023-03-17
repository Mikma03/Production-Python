N=3

def greedy(M, W, C, X):
    Z=M # Pozostaje do wypełnienia
    for i in range(N):
        if W[i] > Z:
            break
        X[i] = 1
        Z = Z - W[i]
    if i < N:
        X[i] = Z/W[i]

# Przetestujmy:
W=[10, 12, 16]
C=[60, 70 ,80]
X=[0,  0,   0]
greedy(20, W, C, X)
p=float()
for i in range(N):
    p = p+ X[i] * C[i]
    print (f" i={i}  W[i]={W[i]} C[i]={C[i]}  X[i]={X[i]}")
print("Razem:", p)