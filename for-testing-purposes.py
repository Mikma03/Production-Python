class Parent:
    def greet(self):
        print("Hello from Parent")

class Child(Parent):
    def greet(self):
        super().greet()
        print("Hello from Child")

# c = Child()
# c.greet()

# my_list = [1, 2, 3, 4, 5]