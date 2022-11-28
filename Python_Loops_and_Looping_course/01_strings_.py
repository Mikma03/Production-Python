

# simple loop over string
s = "first_string"

for items in s:
    print(items)


# we can get part of a given string
s[0]
s[3]

# error will occure
s[4] = "t"

# negative indexes
s[-1]
s[-2]

len(s)

s[1:3]
s[:4]
s[::2]
s[::-1]


# string methods
s.capitalize()
s.count("f")
s.lower()
s.upper()
s.islower()
s.isupper()

d = "another str"
a = s + ' ' + d


