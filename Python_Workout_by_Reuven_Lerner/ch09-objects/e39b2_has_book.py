#!/usr/bin/env python3

"""Solution to chapter 9, exercise 39, beyond 2: has_book"""


class Book:
    def __init__(self, title, author, price):
        self.title = title
        self.author = author
        self.price = price


class Shelf:
    def __init__(self):
        self.books = []

    def add_books(self, *args):
        self.books += args

    def total_price(self):
        return sum(one_book.price
                   for one_book in self.books)

    def has_book(self, title):
        return title in (one_book.title
                         for one_book in self.books)
