squares = [i**2 for i in range(10)]

print(squares)

generator_ = (i**2 for i in range(10))

for i    in generator_:
    print(i)

print(iter(generator_) is generator_)