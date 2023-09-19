import typing


class HandleList:
    def __init__(self):
        self._list = []

    def add_to(self, element):
        self._list.append(element)
        print(self._list)
    

l = HandleList()
l.add_to(3)
l.add_to(4)


def _add(a,b):
    print(a+b)

_add(4,5)


def x_inerate(_element):
    for e in _element:
        print(e)

x_inerate('str')