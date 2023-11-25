a = 1
b = 0

results = a/b
print(results)

exception_ = ValueError("My custom message")

repr(exception_)
str(exception_)
print(exception_)

raise exception_

name = "John"

if len(name) > 3:
    raise NameError("Name is too short")

issubclass(NameError, Exception)