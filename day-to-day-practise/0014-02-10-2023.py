
# Given an integer array nums of length n, you want to create an array ans of length 2n where ans[i] == nums[i] and ans[i + n] == nums[i] for 0 <= i < n (0-indexed).

# Specifically, ans is the concatenation of two nums arrays.

# Return the array ans.

from typing import List
myArr = [1,2,3,4]

class Solution:
    def getConcatenation(self, nums: List[int]) -> List[int]:
        ans = []
        for i in nums:
            ans.append(i)

        ans = ans * 2
        return ans

s = Solution()
s.getConcatenation(myArr)


#####
from typing import List
myArr = [1,2,3,4]

class Solution_2:
    def getConcatenation(self, nums: List[int]) -> List[int]:
        ans = nums + [i for i in nums]
        return ans

s = Solution_2()
s.getConcatenation(myArr)


####
from typing import List
myArr = [1,2,3,4]


class Solution_3:
    def getConcatenation(self, nums: List[int]) -> List[int]:
        ans = []
        
        for z in range(2):
            for i in nums:
                ans.append(i)
        return ans

s = Solution_3()
s.getConcatenation(myArr)




# Given an integer array nums, return true if any value appears at least twice in the array, and return false if every element is distinct.

class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:
        arr_len = len(nums)
        arr_to_set = set(nums)

        if arr_len > len(arr_to_set):
            return True
        
        if arr_len == len(arr_to_set):
            return False


arr = [1,1,2,3]
len(arr)

to_set = set(arr)
len(to_set)



class Solution_2:
    def containsDuplicate(self, nums: List[int]) -> bool:
        set_ = set()
        for i in nums:
            if i in set_:
                return True
            set_.add(i)
        return False
    

my_set = set(x for x in range(20))

my_set