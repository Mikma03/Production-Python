
# Given two strings s and t, return true if t is an anagram of s, and false otherwise.

# An Anagram is a word or phrase formed by rearranging the letters of a different word or phrase, typically using all the original letters exactly once.

# Solution_1
s = "cax"
t = "tac"

class Solution:
    def check_(self, s: str, t: str):
        if len(s) != len(t):
            return False

        s_list = list(s)
        t_list = list(t)

        for item in s_list:
            if item in t_list:
                t_list.remove(item)  # remove the found item from t_list
            else:
                return False  # return False as soon as an unmatched character is found

        return True  # return True only if all characters have been matched

sol = Solution()
res = sol.check_(s, t)
print(res)




# Solution_2
s = "cax"
t = "tac"

class Solution:
    def check_(self, s: str, t: str):
        if len(s) != len(t):
            return False

        # Create dictionaries to hold the frequency of each character
        s_dict = {}
        t_dict = {}

        # Count the frequency of each character in s
        for char in s:
            s_dict[char] = s_dict.get(char, 0) + 1
        
        # Count the frequency of each character in t
        for char in t:
            t_dict[char] = t_dict.get(char, 0) + 1

        # Compare the dictionaries to see if they are equal
        return s_dict == t_dict

sol = Solution()
res = sol.check_(s, t)
print(res)



# Solution_3
class Solution:
    def check_(self, s: str, t: str):
        return sorted(s) == sorted(t)

sol = Solution()
res = sol.check_(s, t)
print(res)
