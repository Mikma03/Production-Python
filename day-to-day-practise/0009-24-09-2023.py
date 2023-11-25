

my_var = 10

while my_var > 0:
    print("Hello World")
    my_var = my_var - 1

# this is prefered way
my_data = [100, 200, 300, 400, 500]

while len(my_data) > 0:
    last_element = my_data.pop()
    print(f'processing element {last_element}')


# this works okay
my_data = [100, 200, 300, 400, 500]

for i in range(len(my_data)):
    element = my_data.pop()
    print(f'processing element {element}')
    print('-'*20)
    print(f'My data after processing: {my_data}')

# here is bug
my_data = [100, 200, 300, 400, 500]

for i in range(len(my_data)):
    element = my_data.pop(i)
    print(f'processing element {element}')