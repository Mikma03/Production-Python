<!-- TOC -->

- [Online materials](#online-materials)
  - [Data structures road map](#data-structures-road-map)
  - [Leetcode](#leetcode)
- [Books](#books)
- [Online courses](#online-courses)
- [GitHub repos](#github-repos)
- [Important questions and steps](#important-questions-and-steps)
- [Chapter 16 - John Canning Book](#chapter-16---john-canning-book)
  - [Key points from that chapter](#key-points-from-that-chapter)
    - [Analyzing the Problem](#analyzing-the-problem)
    - [What Kind of Data?](#what-kind-of-data)
    - [How Much Data?](#how-much-data)
    - [What Creates the Data?](#what-creates-the-data)
    - [What Operations and How Frequent?](#what-operations-and-how-frequent)
    - [Who Will Maintain the Software?](#who-will-maintain-the-software)
    - [Speed and Algorithms](#speed-and-algorithms)
      - [**Arrays**](#arrays)
      - [**Linked Lists**](#linked-lists)
      - [**Binary Search Trees**](#binary-search-trees)
      - [**Hash Tables**](#hash-tables)
- [Data structures in Python: builtin](#data-structures-in-python-builtin)
  - [List](#list)
  - [Tuple](#tuple)
  - [Set](#set)
  - [Dictionary](#dictionary)
  - [Deque](#deque)
  - [Heapq](#heapq)
  - [Counter](#counter)
  - [Defaultdict](#defaultdict)

<!-- /TOC -->

# Online materials

## Data structures road map

- https://neetcode.io/roadmap

## Leetcode

- https://leetcode.com/problemset/all/

# Books

Data Structures & Algorithms in Python

- https://learning.oreilly.com/library/view/data-structures/9780134855912/

Algorytmy w Pythonie. Techniki programowania dla praktyków

- https://helion.pl/ksiazki/algorytmy-w-pythonie-techniki-programowania-dla-praktykow-piotr-wroblewski,algpyt.htm#format/d

# Online courses

- https://neetcode.io/courses

# GitHub repos

- Minimal examples of data structures and algorithms in Python

  - https://github.com/keon/algorithms

- A collection of design patterns/idioms in Python Topics
  - https://github.com/faif/python-patterns

---

# Important questions and steps

1. Analyzing the Problem: What actually need to be done?
2. What Kind of Data? That need to be clear.
3. How Much Data?: Volume of data.
4. What Creates the Data?: Maybe IoT or humans?
5. What Operations and How Frequent? Read / Write etc.
6. Who Will Maintain the Software?: Skills other developers
7. Speed and Algorithms: Is speed important?

# Chapter 16 - John Canning Book

This chapter comes with some caveats. Of necessity, it’s very general. Every real-world situation is unique, so what we say here may not be the right answer to your problem. You need to analyze the problem to determine its characteristics and see whether they match those of the data structure or algorithm.

This chapter is divided into these somewhat arbitrary sections:

- Analyzing the problem: Determine the characteristics that guide the choice of data structure and algorithm

- Foundational data structures: Arrays, linked lists, trees, hash tables

- Special-ordering data structures: Stacks, queues, priority queues, heaps

- Sorting: Insertion sort, Shellsort, quicksort, mergesort, heapsort

- Specialty data structures: Quadtrees, graphs

- External storage: Sequential storage, indexed files, B-trees, hashing

## Key points from that chapter

### Analyzing the Problem

As a developer, you should always review the plans for the software you intend to develop. There can be—and usually are—many goals for a particular software project. Commercial companies want to create products that sell. Scientific organizations want systems that accurately record, model, and analyze their data. Governments want software that helps educate, protect, and account for their citizens and jurisdictions. Analyzing these kinds of goals is important; it tells you what needs to be built or changed. The organization’s goals are less informative about how to build it to achieve the speed, cost (in terms of memory and other computing resources), and ease of maintenance that everyone wants.

### What Kind of Data?

The problem domain usually makes very clear what type of data will be manipulated. It could be records about company transactions, audio recordings of animal calls, measurements of experiments in a lab, or videos that will be streamed to viewers.

### How Much Data?

When you know the kinds of data, how they fit into chunks, and how they are going to be addressed, the next question is how many of those chunks are there? This characteristic often drives the choice of data structure significantly and is sometimes the hardest to determine.

### What Creates the Data?

The biggest difference in amounts of data comes from how it is produced. If the data is manually produced, it is likely to be far smaller than data produced by automation. Things that people produce manually like text messages, songs, or paintings are all limited by the amount of time spent doing the activity and the number of people doing it.

### What Operations and How Frequent?

The system to be built does something with these chunks of data. A good design lists all the operations, along with estimates of how frequently they will be done and what the requirements are for their performance.

The processing order of data items strongly influences the choice of structures. For example, reconciling all the transactions that streamed in during a trading day likely must be done in the order they occurred. That means a queue is more appropriate than a stack. If the streaming order is not quite the same as the trading order, then a priority queue or heap would be better.

### Who Will Maintain the Software?

Determining what data structures and algorithms to use depends not only on the data and operations on that data, but on the people who will maintain the software as (the inevitable) changes are made. Programmers have different skill levels, and using highly complicated algorithms or structures could become a barrier to being able to make changes easily.

### Speed and Algorithms

The general-purpose data structures can be roughly arranged in terms of speed when items are specified by key: arrays and linked lists are slow, trees are fairly fast, and hash tables are very fast.

Don’t draw the conclusion, however, that it’s always best to use the fastest structures. There’s a penalty for using them. First, they are—in varying degrees—more complex to program than the array and linked list. Also, hash tables use memory somewhat inefficiently. Ordinary binary trees revert to slow O(N) operation for ordered data; and balanced trees, which avoid this problem, are more complex to program.

#### **Arrays**

In many situations the array is the first kind of structure you should consider when storing and manipulating data. Arrays are useful when

- The amount of data is reasonably small.

- The amount of data is predictable in advance.

- The items will be addressed by index for most of the time.

- The order the items will be accessed is variable.

When the array size grows, data must be copied from the existing array to the new one. The growth operation can sometimes lead to a significant amount of memory being allocated but unused.

#### **Linked Lists**

Consider a linked list when

- The amount of data to be stored is not easily predicted in advance and minimizing memory usage is important.

- Data will frequently be inserted and deleted, and the order of the items is important.

- The data will be addressed or processed in the order it was received (or the reverse).

#### **Binary Search Trees**

A binary search tree is the next structure to consider when arrays and linked lists prove too slow. Consider binary search trees

- When data will be addressed and ordered by a key.

- When data will be frequently inserted and deleted.

- When minimizing memory usage is important.

A tree provides fast O(log N) insertion, searching, and deletion. Traversal in key order is O(N), which is the fastest for any data structure. [The fact that binary search trees order their items by a key means a traversal in sorted order takes O(N) time while an unsorted array or list would need to be sorted first.] You can also find the minimum and maximum quickly, O(log N), and traverse a range of items.

An unbalanced binary tree is much easier to program than one that balances itself, but unfortunately ordered data can reduce its performance to O(N) time, no better than a linked list. If you’re certain the data will be inserted in random order with respect to the key, there’s not much point in using a balanced tree.

#### **Hash Tables**

Hash tables have the most desirable performance for almost all data items referenced by a key. The keys can be any data type that might be considered an index, including integers. The O(1) performance for searching, insertion, and deletion by key are the fastest possible.

Consider a hash table

- When data will be addressed by a key and the traversal order of the items by the key is unimportant.

- When minimizing memory usage is somewhat important and some unused memory is tolerable.

- When the complexities of the hashing and collision resolution algorithms are handled by experienced developers.

> **This part will be continiued**

# Data structures in Python: builtin

In Python, several data structures are known for their efficiency in different use cases. It's essential to choose the right data structure based on the problem you are trying to solve. Here are some of the most efficient data structures in Python:

## List

- List: Lists are versatile and widely used in Python. They allow for fast O(1) access and modification by index. However, insertion and deletion operations have O(n) complexity because elements must be shifted.

## Tuple

- Tuple: Tuples are similar to lists but immutable. They are faster and consume less memory than lists since they cannot be modified after creation. Tuples are ideal for storing fixed-size collections of related data.

## Set

- Set: Sets are unordered collections of unique elements. They are implemented as hash tables, which allow for fast O(1) average time complexity for insertions, deletions, and search operations. Sets are ideal for solving problems that involve deduplication or membership testing.

## Dictionary

- Dictionary (dict): Dictionaries are key-value pairs implemented as hash tables. They provide fast O(1) average time complexity for insertion, deletion, and search operations. Dictionaries are efficient for problems involving data organization and retrieval based on keys.

## Deque

- deque (collections module): Deques are double-ended queues, which are optimized for fast O(1) appends and pops from both ends. They are useful for implementing stacks and queues or other data structures requiring fast access at both ends.

## Heapq

- heapq (heapq module): Heapq provides an implementation of heap queue algorithm (priority queue) with O(log n) time complexity for insertion and extraction of the smallest element. It is useful for problems that require priority-based scheduling or maintaining a running list of the smallest or largest items.

## Counter

- Counter (collections module): Counter is a specialized dictionary subclass for counting elements in an iterable. It is efficient for counting frequency, finding the most common elements, or performing operations like addition and subtraction between counts.

## Defaultdict

- defaultdict (collections module): defaultdict is a dictionary subclass that provides a default value for a nonexistent key, specified upon initialization. It is useful for grouping and counting operations where keys might not be present initially.
