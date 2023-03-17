def silnia_it(x, res=1):
    while (x!=0):
        res=x*res
        x=x-1
    return res

print ("Silnia(5)=", silnia_it(5) )
