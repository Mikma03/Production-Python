
In Python, `super()` is a built-in function that is used to call a method from the parent class. This function is commonly used in the context of single inheritance to call parent class constructors and methods, but it becomes particularly useful in multiple inheritance scenarios.

### Basic Usage:

In a single inheritance scenario, `super()` can be used to call methods from the parent class. Here’s a basic example:


```python
class Parent:
    def greet(self):
        print("Hello from Parent")

class Child(Parent):
    def greet(self):
        super().greet()
        print("Hello from Child")

c = Child()
c.greet()
```


Output:

```markdown
Hello from Parent
Hello from Child
```

In this example, `super().greet()` calls the `greet` method from `Parent` class.

### super() in Constructors:

`super()` is often used in constructors (`__init__` methods) to ensure that the parent class's constructor is also being called when an object is instantiated:

```python
class Parent:
    def __init__(self, name):
        self.name = name

class Child(Parent):
    def __init__(self, name, age):
        super().__init__(name)
        self.age = age

c = Child("Alice", 10)
```

Here, `super().__init__(name)` ensures that the `__init__` method of `Parent` class is called, initializing the `name` attribute.

### super() in Multiple Inheritance:

In multiple inheritance scenarios, `super()` plays a crucial role in invoking methods from parent classes in a predictable order (following the Method Resolution Order - MRO).

pythonCopy code

```python
class A:
    def show(self):
        print("A")

class B(A):
    def show(self):
        print("B")
        super().show()

class C(A):
    def show(self):
        print("C")
        super().show()

class D(B, C):
    def show(self):
        print("D")
        super().show()

d = D()
d.show()
```

Output:

`D B C A`

In this example, calling `show` on an instance of `D` triggers the method calls in the order `D -> B -> C -> A`, which is defined by Python's MRO.

### Method Resolution Order (MRO):

MRO is the order in which base classes are searched when executing a method. The MRO ensures that a class is only visited once in the inheritance chain. You can view the MRO by using the `__mro__` attribute or the `mro()` method:


```python
print(D.mro())
```

### super() with Arguments:

`super()` can also be called with two parameters: the first is the subclass, and the second parameter is an object that is an instance of that subclass.

```python
class Parent:
    def greet(self):
        print("Hello from Parent")

class Child(Parent):
    def greet(self):
        super(Child, self).greet()
        print("Hello from Child")

c = Child()
c.greet()
```

In Python 3, `super(Child, self)` is equivalent to just `super()` when used inside a class method.

### Key Points:

- `super()` allows you to avoid hardcoding the parent class name in method calls.
- In multiple inheritance scenarios, `super()` navigates through the class hierarchy based on the MRO.
- `super()` can be used in any method, not just `__init__`, to call corresponding methods in the parent class.

### Conclusion:

`super()` is a powerful function in Python that allows you to avoid referring to the base class explicitly, which can be especially handy in multiple inheritance scenarios. It helps in calling methods from parent classes in a clear and maintainable way.