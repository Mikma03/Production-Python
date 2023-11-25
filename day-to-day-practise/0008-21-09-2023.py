try:
    1 / 0
except ZeroDivisionError as ex:
    print(f'Exception type {type(ex)}, {ex}')
print('Code running here')

data = [1,3,6,7]

suma_data = 0
count_data = 0

for element in data:
    suma_data = suma_data + element
    count_data = count_data + 1

print(f'suma_data: {suma_data}')

try:
    raise ValueError('My custom message')
except ValueError as ex:
    print(f'handled exception {ex}')

finally:
    print("This will always run")