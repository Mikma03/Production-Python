l = [1,2,3,4]

iterator = iter(l)

try:
    while True:
        element = next(iterator)
        print(element)
except StopIteration:
    pass

from time import perf_counter

start = perf_counter()
l = range(100_000_000_000)
end = perf_counter()
print(f'elapsed: {end - start}')



start = perf_counter()
l = list(range(100_000_000_000))
end = perf_counter()
print(f'elapsed: {end - start}')