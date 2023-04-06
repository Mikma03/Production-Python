def palindrom(s):
    dl = len (s)
    cpt = 0
    test = True # 's' jest (na razie) palindromem
    while cpt <= dl // 2 and test == True:
        if s[cpt] == s[dl-cpt-1]:
            cpt = cpt+1
        else:
            test = False
    print(s, end="")
    if test==True:
        print(" ...jest palindromem")
    else:
        print(" ...jest zwykłym słowem...")


# --------------------------------------------
palindrom("ab")
palindrom("a")
palindrom("abba")
palindrom("abkba")
palindrom("abkca")