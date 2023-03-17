
def min_max1(t):
	if len(t) < 1:
		return None, None
	min, max = t[0], t[0]
	for i in range( 1, len(t) ): # Od 1 do n-1
		if max < t[i]:		# (*)
			max = t[i]
		if min>t[i]:		# (**)
			min = t[i]
	return (min, max)

# Testujemy
tab0 = []
tab1 = [-23]
tab2 = [-23, 12, 1, -5, 34, -7, 45, 2, 88, -3, -9, 1]
print(f" tab0={tab0}")
print(f" min={min_max1(tab0)[0]}, max={min_max1(tab0)[1]}") #  min=None, max=None
print(f" tab1={tab1}")
print(f" min={min_max1(tab1)[0]}, max={min_max1(tab1)[1]}") #  min=-23, max=-23
print(f" tab2={tab2}")
print(f" min={min_max1(tab2)[0]}, max={min_max1(tab2)[1]}") #  min=-9, max=88
