def N(n, p):
    if (n==0):
        return 1;
    else:
        return N( n-1, N(n-p, p) )
# Programu nie da sie poprawnie uruchmomić!
#  File "/Users/piotr/Documents/books/python-algo/przyklady/n.py", line 5, in N
#    return N(n-1,N(n-p,p))
#  [Previous line repeated 995 more times]
#  File "/Users/piotr/Documents/books/python-algo/przyklady/n.py", line 2, in N
#    if (n==0):
#RecursionError: maximum recursion depth exceeded in comparison

print( "N(1,0)=", N(1,0) )
print("Ta linijka nigdy się nie wyświetli...")