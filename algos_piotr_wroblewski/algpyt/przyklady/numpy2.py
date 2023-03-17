import numpy as np
t1 = np.arange(1, 6)  #  Od 1. do 5.
print("t1: ",t1)
t2 = np.arange(6, 11) #  Od 6. do 10.
print("t2: ",t2)
t3 = np.vstack((t1, t2))
print("Kształt t3 to", t3.shape)
print("t3 po zastosowaniu vstack()\n",t3)
t3 = t3.transpose()
print("t3 po transpozycji:",t3)
print("Nowy kształt t3 to", t3.shape)
print("Liczba wymiarów tablicy t3 to", t3.ndim)
t4 = np.hstack((t1, t2))
print("t4=t1 sklejona horyzontalnie z t2:",t4)