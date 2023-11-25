
# Given an integer array nums, return true if any value appears at least twice in the array, and return false if every element is distinct.

from typing import List

class Solution:
    def containsDuplicate(self, my_list: List):
        self.my_list = my_list
        if len(self.my_list) > len(set(self.my_list)):
            return True
        else:
            return False

_list = [1,4,3]

s = Solution()
s.containsDuplicate(_list)




# Given two strings s and t, return true if t is an anagram of s, and false otherwise.

# An Anagram is a word or phrase formed by rearranging the letters of a different word or phrase, typically using all the original letters exactly once.




class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        if len(s) != len(t):
            return False
        
        _s,_t = {}, {}
        for x in range(len(s)):
            ...

str1 = "mikko"
str2 = "okim"

s = Solution()
s.isAnagram(str1, str2)


from collections import Counter


class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        if len(s) != len(t):
            return False
        
        if Counter(s) == Counter(t):
            return True
        else:
            return False
        


str1 = "mikko"
str2 = "okim"

s = Solution()
s.isAnagram(str1, str2)



