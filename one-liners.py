import random

# Reverse a String
reversed_string = "Hello World"[::-1]

# Check if a Number is Even
is_even = lambda x: x % 2 == 0

# Find the Intersection of Two Lists
intersection = list(set(list1) & set(list2))

# Remove Duplicates from a List
no_duplicates = list(set(my_list))

# Calculate the Length of a String without Using len()
length = sum(1 for _ in 'Hello World')

# Check if a List Contains All Elements of Another List
contains_all = all(elem in list1 for elem in list2)

# Generate a String of Random Characters
random_str = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=10))

# Convert a List of Integers to a Single Number
num = int(''.join(map(str, [1, 2, 3, 4, 5])))

# Palindromic Check
is_palindrome = lambda s: s == s[::-1]

# List Flattening
flatten_list = sum([[1, 2], [3, 4]], [])

# Find the Most Frequent Element in a List
most_frequent = max(set(my_list), key=my_list.count)

# Merge Two Dictionaries
merged_dict = {**dict1, **dict2}
