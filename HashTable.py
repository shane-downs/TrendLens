from Article import *


class HashTable:        # hash table where each index is a list. Each list holds article of a similar keyword. Quadratic Probing
    def __init__(self):
        self.LOAD_FACTOR = 0.7       # load factor is 0.6
        self.tableSize = 10         # initiate table size to 10
        self.buckets = 0           # number of items is 0 until we insert something
        self.table = []      # table to hold the actual information
        for item in range(10):      # add 10 empty lists to the table
            self.table.append([])

    def Hash(self, article):        # returns an integer that is the hashed value derived from the article keyword
        # first we need to reverse the article keyword so that our indexing later is correct
        keyword = article.keyword[::-1]
        index = 0
        for i in range(len(keyword)):       # iterate through keyword
            index += ord(keyword[i]) * pow(27, i)       # multiply the unicode value of current char by 27^i
            # CITATION: Amanpreet Kapoor (Module 7 - Lecture Slides - Slide 30)
        # now we are done and have the sum of the chars in the keyword, so convert it to an index
        index = index % self.tableSize
        return index            # return the index

    def Insert(self, article):      # returns nothing. Inserts the article object into the appropriate sub-list in our table
        # get the index to insert the article into
        hashIndex = self.Hash(article)

        # find the right spot in the table and insert it
        # we start a quadratic for loop here so that if the spot we are looking at is a diff keyword we can go right into quadratic probing
        for i in range(self.tableSize - 1):     # iterate through size of table
            quadIndex = (i ** 2) % self.tableSize       # this increases our index quadratically -> (0, 1, 4, 9, 16...)
            currIndex = (hashIndex + quadIndex) % self.tableSize        # the current index for our article to be inserted into
            # since each spot in the table represents a different keyword we need to check if inserting this creates conflict
            if (len(self.table[currIndex]) == 0):        # if this sub-list is empty, there won't be conflict
                self.table[currIndex].append(article)        # so just add it to the list at that spot
                break           # and break out of the for loop because there is no need to do quadratic probing
            else:       # otherwise there is something here, so lets check if it has the same keyword as our article
                if ((len(self.table[currIndex]) > 0) and (self.table[currIndex][0].keyword == article.keyword)):  # if the sub-list isn't empty and has the same keyword
                    self.table[currIndex].append(article)          # add this article to the sub-list
                    break       # and then break out of the for loop
                else:    # if there was something there that was a conflict, in which case we continue with quadratic probing
                    continue        # we continue in the for loop (this conditional isn't necessary but helps readability)

        # now, increment table variables and check load factor
        self.buckets += 1      # increment the number of total articles
        if ((self.buckets / self.tableSize) >= self.LOAD_FACTOR):   # if  we are at/over load factor, we need to resize and rehash
            self.tableSize *= 2     # double the size of our table
            newTable = []       # new table which will replace the current table
            for i in range(self.tableSize):     # add a sub-list for every possible spot in the table
                newTable.append([])
            for i in range(int(self.tableSize / 2) - 1):     # for every sub-list in original table...
                for j in range(len(self.table[i])):        # for every article in the table list (it will skip over if empty)
                    # get the hash index again
                    newHashIndex = self.Hash(self.table[i][j])
                    # we might have to quadratic probing to insert, so prepare for that again
                    for k in range(self.tableSize - 1):  # iterate through size of new table (so our quadratic probing covers the entirety of new table)
                        quadIndex = (k ** 2) % self.tableSize  # this increases our index quadratically -> (0, 1, 4, 9, 16...)
                        currIndex = (newHashIndex + quadIndex) % self.tableSize     # current index in our new table to look at
                        # since each spot in the table represents a different keyword we need to check if inserting this creates conflict
                        if (len(newTable[currIndex]) == 0):  # if it is empty, there won't be conflict
                            newTable[currIndex].append(self.table[i][j])  # so just append the article we are referring to in OG table to the new table at that sub-list
                            break  # and break out of the for loop to move on to the next article in the OG table
                        else:  # otherwise there is something here, so lets check if it has the same keyword as our article
                            if (newTable[currIndex][0].keyword == self.table[i][j].keyword):  # if they have the same keyword
                                newTable[currIndex].append(self.table[i][j])  # add the corresponding article to the new table's correct sub-list
                                break  # and then break out of the for loop to go to next article in OG table
                            else:  # if there was something there that was a conflict, in which case we continue with quadratic probing
                                continue  # we continue in the for loop (this conditional isn't necessary but helps readability)

            # now that we are done going through the table and rehashing all of our items, update self.table
            self.table = newTable

    def Access(self, keyword):   # takes a keyword and returns a list of articles with that keyword (or empty list if key doesn't exist)
        # first get hash that keyword is hopefully at (the reason it wouldn't be here would be because of quadratic probing)
        hashIndex = self.Hash(Article("None", keyword, -1, -1))     # generate it with a garbage Article object (the only part we need is the keyword part)
        # if it isn't at keyHash we may have to do quadratic probing to find it so prepare for that
        for i in range(self.tableSize - 1):     # iterate through size of our table to look for it
            quadIndex = (i ** 2) % self.tableSize       # this increases our index quadratically -> (0, 1, 4, 9, 16...)
            currIndex = (hashIndex + quadIndex) % self.tableSize        # the current index we are looking at in our table
            # check if the current sub-list is the right list
            if ((len(self.table[currIndex]) > 0) and (self.table[currIndex][0].keyword == keyword)):        # if the sub-list isn't empty and has the same keyword
                return self.table[currIndex]           # return that list since it is a list of all the right keywords
            else:       # if it wasn't the right keyword
                continue        # we continue quadratic probing (this conditional isn't necessary but is for readability)
        return []       # if we get here we did not find the keyword in the hash table so return -1