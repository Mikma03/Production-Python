
# test for classes: my practise
# class MyClass:

#     # atribute
#     name_test_atribute = "Jack"

#     def __init__(self, first, second):
#         self.first = first
#         self.second = second

#     def call_1(self):
#         return f"I have access to atr {self.name_test_atribute}"
    
#     def call_2(self):
#         return f"I have access to {self.first} as well {self.second}"
    

# insta_ = MyClass(1,2)

# print(insta_.first)
# print(insta_.second)

# print(insta_.call_1())
# print(insta_.call_2())



class Dog:
    def __init__(self, name):
        self.name = name

    def speak(self, sound):
        # Print the 'self' parameter to show it's the 'buddy' instance
        print(f'self is {self}, which has name: {self.name}')
        return f'{self.name} says {sound}'

# Custom print function to simulate what Python does internally
def custom_print(method, *args, **kwargs):
    print(f'Calling {method.__name__}() with self={args[0]} and sound={args[1]}')
    return method(*args, **kwargs)

# Create an instance of Dog
buddy = Dog('Buddy')

# Call the instance method normally
normal_call = buddy.speak('Woof')
print(f'Normal call result: {normal_call}')

# Call the instance method using our custom print function to simulate internal behavior
simulated_internal_call = custom_print(Dog.speak, buddy, 'Woof')
print(f'Simulated internal call result: {simulated_internal_call}')


# Explanation

# instance method like `buddy.speak('Woof')` translates to `Dog.speak(buddy, 'Woof')` internally in Python
# in speak() example: self = instance of class: buddy = Dog('Buddy'); plus argument: sound = "Woof"

# Results

# self is <__main__.Dog object at 0x11b860d10>, which has name: Buddy
# Normal call result: Buddy says Woof

# Calling speak() with self=<__main__.Dog object at 0x11b860d10> and sound=Woof
# self is <__main__.Dog object at 0x11b860d10>, which has name: Buddy
# Simulated internal call result: Buddy says Woof