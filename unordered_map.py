from HashTable import *
import random


class unordered_map:        # map backed up by hash table. Key is a keyword, value is a list of article with that keyword
    def __init__(self):
        self.map = HashTable()      # map is just a hash table
        self.size = 0

    def InsertAll(self, articleList):       # takes a list of article objects and inserts them all into the map
        for article in articleList:     # for every article object in the list of article objects
            self.size += 1      # increment the size by 1
            self.map.Insert(article)        # insert the article into the map

    def ClearMap(self):     # clear the contents of the map
        self.map = HashTable()      # overwrite the current map with a new hashtable object that is empty
        self.size = 0               # reset size to 0

    def GetSize(self):          # returns the size of the map
        return self.size

    def GetRandomKeyword(self):
        return self.map.FetchRandomKeyword()

    def __getitem__(self, key):        # this overloads the [ ] operator when used to access (on right hand side)
        return self.map.Access(key)         # return the list of items that have the requested keyword

    def __setitem__(self, key, value):      # this overloads the [ ] operator when used to assign (on the left hand side)
        self.size += 1      # increment size
        # the value parameter is an article object, but we have it for the python built-in function. But we will have it just for fun
        self.map.Insert(value)    # insert the object indicated into the hash table (O(1)) amortized

    def __contains__(self, key):    # this returns a bool that tells if the key is a keyword in the hash table
        if (len(self.map.Access(key)) == 0):        # if the attempt to access it returns an empty list, we didn't find it in our table
            return False        # so return False because our map doesn't contain it
        else:       # if we returned anything else (such as a list) it is in our hash table
            return True     # return True
