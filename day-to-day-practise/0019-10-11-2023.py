from typing import Optional

# Link: https://www.youtube.com/watch?v=Y0lT9Fck7qI&ab_channel=NeetCode
# Link: https://neetcode.io/courses/dsa-for-beginners/9

class Solution:
    def climbStairs(self, n: int) -> int:
        if n <= 3:
            return n
        n1, n2 = 2, 3

        for i in range(4, n + 1):
            temp = n1 + n2
            n1 = n2
            n2 = temp
        return n2


# Link: https://neetcode.io/courses/dsa-for-beginners/8

# Recursive implementation of n! (n-factorial) calculation
def factorial(n):
    # Base case: n = 0 or 1
    if n <= 1:
        return 1

    # Recursive case: n! = n * (n - 1)!
    return n * factorial(n - 1)


# Link: https://neetcode.io/courses/dsa-for-beginners/9

# Recursive implementation to calculate the n-th Fibonacci number
def fibonacci(n):
    # Base case: n = 0 or 1
    if n <= 1:
        return n

    # Recursive case: fib(n) = fib(n - 1) + fib(n - 2)
    return fibonacci(n - 1) + fibonacci(n - 2)


# Link: https://neetcode.io/courses/dsa-for-beginners/8
# Link: https://www.youtube.com/watch?v=G0_I-ZF0S38&ab_channel=NeetCode

# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None


class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        prev, curr = None, head

        while curr:
            temp = curr.next
            curr.next = prev
            prev = curr
            curr = temp
        return prev
