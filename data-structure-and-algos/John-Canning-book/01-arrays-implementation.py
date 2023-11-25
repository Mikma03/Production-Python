# Link: https://learning.oreilly.com/library/view/data-structures/9780134855912/ch02xhtml#:-:text=An%20Array%20Class%20Example


# Implement an Array data structure as a simplified type of list.
class Array(object):
    def __init__(self, initialSize):  # Constructor
        self.__a = [None] * initialSize  # The array stored as a list
        self.nItems = 0  # No items in array initially

    def insert(self, item):  # Insert item at end
        self.__a[self.nItems] = item  # Item goes at current end
        self.nItems += 1  # Increment number of items

    def search(self, item):
        for j in range(self.nItems):  # Search among current
            if self.__a[j] == item:  # If found,
                return self.__a[j]  # then return item

        return None  # Not found -> None

    def delete(self, item):  # Delete first occurrence
        for j in range(self.nItems):  # of an item
            if self.__a[j] == item:  # Found item
                for k in range(j, self.nItems):  # Move items from
                    self.__a[k] = self.__a[k + 1]  # right over 1
                self.nItems -= 1  # One fewer in array now
                return True  # Return success flag

        return False  # Made it here, so couldn't find the item

    def traverse(self, function=print):  # Traverse all items
        for j in range(self.nItems):  # and apply a function
            function(self.__a[j])


# | Algorithm      | Unordered Array | Ordered Array |
# |----------------|-----------------|---------------|
# | Linear search  | O(N)            | O(log N)      |
# | Binary search  | Not possible    | O(log N)      |
# | Insertion      | O(1)            | O(N)          |
# | Deletion       | O(N)            | O(N)          |

A = Array(10)  # Create an array
A.insert(5)  # Insert 5
A.insert(6)  # Insert 6
A.insert(7)  # Insert 7
# now print Array
A.traverse()  # Print array


# Implement an Array data structure as a simplified type of list.
class Array(object):
    def __init__(self, initialSize):  # Constructor
        self.__a = [None] * initialSize  # The array stored as a list
        self.__nItems = 0  # No items in array initially

    def __len__(self):  # Special def for len() func
        return self.__nItems  # Return number of items

    def get(self, n):  # Return the value at index n
        if 0 <= n and n < self.__nItems:  # Check if n is in bounds, and
            return self.__a[n]  # only return item if in bounds

    def set(self, n, value):  # Set the value at index n
        if 0 <= n and n < self.__nItems:  # Check if n is in bounds, and
            self.__a[n] = value  # only set item if in bounds

    def insert(self, item):  # Insert item at end
        self.__a[self.__nItems] = item  # Item goes at current end
        self.__nItems += 1  # Increment number of items

    def find(self, item):  # Find index for item
        for j in range(self.__nItems):  # Among current items
            if self.__a[j] == item:  # If found,
                return j  # then return index to item
        return -1  # Not found -> return -1

    def search(self, item):  # Search for item
        return self.get(self.find(item))  # and return item if found

    def delete(self, item):  # Delete first occurrence
        for j in range(self.__nItems):  # of an item
            if self.__a[j] == item:  # Found item
                self.__nItems -= 1  # One fewer at end
                for k in range(j, self.__nItems):  # Move items from
                    self.__a[k] = self.__a[k + 1]  # right over 1
                return True  # Return success flag

        return False  # Made it here, so couldn't find the item

    def traverse(self, function=print):  # Traverse all items
        for j in range(self.__nItems):  # and apply a function
            function(self.__a[j])
