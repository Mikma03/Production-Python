
<!-- TOC -->

- [Link to the book](#link-to-the-book)
- [Arrays](#arrays)
  - [Searching with Duplicates](#searching-with-duplicates)
  - [Deletion with Duplicates](#deletion-with-duplicates)

<!-- /TOC -->

# Link to the book

Data Structures & Algorithms in Python

- https://learning.oreilly.com/library/view/data-structures/9780134855912/


# Arrays

There are several actions you would like to be able to perform:

- Insert - this is analogy for (in the case of data structures) **add**

- Check - this is analogy for (in the case of data structures) **search**

- Delete - this is analogy for (in the case of data structures) **remove**

- List - this is analogy for (in the case of data structures) **iterate**


| Algorithm      | Unordered Array | Ordered Array |
|----------------|-----------------|---------------|
| Linear search  | O(N)            | O(log N)      |
| Binary search  | Not possible    | O(log N)      |
| Insertion      | O(1)            | O(N)          |
| Deletion       | O(N)            | O(N)          |


- Arrays are sequential groupings of data elements. Each element can store a value called an item.

- Each element of the array can be accessed by knowing the start of the array and an integer index to the element.

- Object-oriented programs are used to implement data structures to encapsulate the algorithms that manipulate the data.

- Data structures use private instance variables to restrict access to important values of the structure that could cause errors if changed by the calling program.

- Unordered arrays offer fast insertion but slow searching and deletion.

- A binary search can be applied to an ordered array.

- The logarithm to the base B of a number A is (roughly) the number of times you can divide A by B before the result is less than 1.

- Linear searches require time proportional to the number of items in an array.

- Binary searches require time proportional to the logarithm of the number of items.

- Data structures usually store complex data types like records.

- A key must be defined to order complex data types.

- If duplicate items or keys are allowed in a data structure, the algorithms should have a predictable behavior for how they are managed.

## Searching with Duplicates

Allowing duplicates complicates the search algorithm, as we noted. Even if the search finds a match, it must continue looking for possible additional matches until the last occupied cell. At least, this is one approach; you could also stop after the first match and perform subsequent searches after that. How you proceed depends on whether the question is “Find me everyone with the family name of Smith,” “Find me someone with the family name of Smith,” or the similar question “Find how many entries have the family name Smith.”

Finding all items matching a search key is an exhaustive search. Exhaustive searches require N steps because the algorithm must go all the way to the last occupied cell, regardless of what is being sought.

## Deletion with Duplicates

Deletion may be more complicated when duplicates are allowed, depending on exactly how “deletion” is defined. If it means to delete only the first item with a specified value, then, on the average, only N/2 comparisons and N/2 moves are necessary. This is the same as when no duplicates are allowed. This would be the desired way to handle deleting an item such as a can of beans from a kitchen pantry when it gets used. Any items with duplicate keys remain in the pantry.

If, however, deletion means to delete every item with a specified key value, the same operation may require multiple deletions. Such an operation requires checking N cells and (probably) moving more than N/2 cells. The average depends on how the duplicates are distributed throughout the array.