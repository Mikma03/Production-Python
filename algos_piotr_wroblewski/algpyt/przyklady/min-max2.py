def min_max2(left, right, t):
	if len(t) < 1:
		return None, None
	if left==right:
		min, max =t[left], t[right] # Jeden element
	else:
		if left==right-1: 	# Dwa elementy
			if t[left]<t[right]:
				min = t[left]
				max = t[right]
			else:
				min = t[right]
				max = t[left]
		else:
			mid = (left + right) // 2
			temp_min1, temp_max1 = min_max2(left,    mid,   t)
			temp_min2, temp_max2 = min_max2(mid + 1, right, t)
			if temp_min1 < temp_min2: 	# (*)
				min = temp_min1
			else:
				min = temp_min2
			if temp_max1 > temp_max2:	# (**)
				max = temp_max1
			else:
				max = temp_max2
	return min, max

# Testujemy
tab0 = []
tab1 = [-23]
tab2 = [-23, 12, 1, -5, 34, -7, 45, 2, 88, -3, -9, 1]

print(f" tab0={tab0}")
print(f" min={min_max2(0, len(tab0)-1, tab0)[0]}, max={min_max2(0, len(tab0)-1, tab0)[1]}") #  min=None, max=None
print(f" tab1={tab1}")
print(f" min={min_max2(0, len(tab1)-1, tab1)[0]}, max={min_max2(0, len(tab1)-1, tab1)[1]}") #  min=None, max=None
print(f" tab0={tab2}")
print(f" min={min_max2(0, len(tab2)-1, tab2)[0]}, max={min_max2(0, len(tab2)-1, tab2)[1]}") #  min=None, max=None

"""
 tab0=[]
 min=None, max=None
 tab1=[-23]
 min=-23, max=-23
 tab0=[-23, 12, 1, -5, 34, -7, 45, 2, 88, -3, -9, 1]
 min=-23, max=88
"""