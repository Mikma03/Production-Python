my_dict = {
    'a': 12,
    'b': 13
}

print(my_dict)

for i in my_dict.values():
    print(i)


def longest(x, y):
    '''Return the longest of two strings.'''
    return x if len(x) >= len(y) else y
