f = ("a", "b", "c")

f[0]
f[2]

# error occue
f[1] = "d"

# methods
f.count("a")
f.index("c")

len(f)
bool(f)

f[1:1]
f[::-1]
f[1:1:1]

# adding elements of tuple
f = f + (1, 2, 3)

# nasted tuples
a = ((1, 2, 3), (4, 5, 6), (7, 8, 9))
a[0]
a[0][0]




