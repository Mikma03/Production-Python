
<!-- TOC -->

- [Iterable elements:](#iterable-elements)
  - [Strings](#strings)
    - [Start stop step](#start-stop-step)
    - [String Methods](#string-methods)
  - [Lists](#lists)
    - [lists methods](#lists-methods)
  - [Tuples](#tuples)
  - [Dictionaries](#dictionaries)
  - [Set](#set)
- [For loop](#for-loop)

<!-- /TOC -->


# Iterable elements:

- lists, strings, tuples, set

___

## Strings

Strings are immutables. Zero base indexing.

___

### Start stop step

We can take a slice using a combination of three parameters: start, stop, and step

You can omit a parameter and use its default value it by adding a colon (:) like this:

a[start:]  - end and step are omitted, so their default values are used (end of the string and 1, respectively).

a[:end]      - start and step are omitted, so their default values are used (0 and 1).

a[::step]  -  start and end are omitted, so their default values are used (0 and the end of the string).

___

### String Methods

<str>.capitalize()
<str>.count(sub[, start[, end]])
<str>.endswith(suffix[, start[, end]])
<str>.find(sub[, start[, end]])
<str>.index(sub[, start[, end]])
<str>.isalnum()
<str>.isdigit()
<str>.islower()
<str>.isupper()
<str>.isspace()
<str>.lower()
<str>.upper()
<str>.split(sep=None, maxsplit=-1)

___

## Lists

Zero base indexing. Can containg different data types. List are mutable.

We can take a slice using a combination of three parameters: start, stop, and step.

- start indicates the index where we want to start adding elements to the slice. By default, it is 0, so if you omit it the slice will start from the first element of the list.

- stop indicates the index where we want to stop adding elements to the slice. The element at the stop index is NOT included in the final slice. By default, the value of stop is the end of the list, so if you omit it every element up to and including the last element of the list will be included.

- step indicates how we want to "jump" from one index to the next. By default, it is 1 so every element in the sequence is included from start to stop

### lists methods

<list>.append(x)
<list>.extend(iterable)
<list>.insert(i, x)
<list>.remove(x)
<list>.pop([i])
<list>.clear()
<list>.index(x, [start[, end]])
<list>.count(x)
<list>.sort(key=None, reverse=False)
<list>.reverse()
<list>.copy()

___

## Tuples

Ordered sequences.
Contain values of any data.
Each element has a particular index.
Immutable.

___

## Dictionaries

Keys have to be unique and immutable.

dictionaries method

image.png

<dictionary>.clear(x)
<dictionary>.get(key[, default])
<dictionary>.items()
<dictionary>.keys()
<dictionary>.pop(key[, default])
<dictionary>.popitem()
<dictionary>.values()
<dictionary>.update([other])

___

## Set

No duplicated elements.
Are mutable.

___

# For loop

for<var> in <iterable_or_sequence>:
Code

for <var> in range(start, stop, step)




