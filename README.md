# Created by Shane Downs, Wilson Goins, and Leonardo Cobaleda

Welcome to the README for the unordered_map section of the TrendLens project.

The unordered map class needs two other files to work, a class called Article and a class called HashTable that is the backend of the map.

-------------------------------------------------------------------------------------------------------------------------------------------------------------------

**unordered_map:**
  Contains attributes self.map and self.size. Attribute self.map is what holds the actual data and self.size is the number of unique Article objects in our map.
  Keys in our map are the keywords of articles, values are lists of all the articles with that keyword. Keys/keywords are NOT case-sensitive.

  InsertAll(articleList) - takes a parameter articleList which is a list of Article objects. Returns nothing. We insert every Article object in the list into the
    unordered map via the insertion function of the hash table. We also increment the size of the map.
    O(n) where n is the number of Article objects in the articleList parameter.
  
  ClearMap() - erases all the data inside the map by replacing self.map with a new instance of the HashTable class.
    O(1)
    
  GetSize() - returns self.map which is the number of unique Article objects that have been added to our map.
    O(1)

  DeleteValue(article) - returns nothing, this deletes a specific article object from the map. article must be an Article object. Calls DeleteArticle(article) from 
    the HashTable class. Then assigns the size of the HashTable (self.map.buckets) to the self.size attribute. We do this because we don't know if the article was
    successfully delete (the article may not have existed) and so if we properly decremented the number of buckets in the hash table then assigning self.size with 
    that should give us the correct size.
    Example: "myMap.DeleteArticle(articleObject1)" This deletes articleObject1 from our map.
    O(n) where n is the number of article in the sub-list. This is because we have to find the specific article in the sub-list which is just an unsorted list.
    This is higher than other functions because they do not return a specific article, they return the sub-list.
  
  getitem(key) - returns a list of all the items in the map that have the same keyword as the key parameter. If the key does not exist in the map, there is
    nothing to return so the function will return an empty list. This supports the use of brackets to access values from the map. This function works by using      
    the Access(key) function of the HashTable class (detailed below). The key must be a string.
    Example: "keyList = myMap["Dirt"]" This will assign a list of all the Article objects with the keyword "Dirt" to keyList.
    O(1) 
    
  setitem(key, value) - returns nothing, this function is used to insert something into the map. It increments the self.size attribute of the unordered_map     
    instance. Then it uses the Insert(value) function of the HashTable class to add the Article object passed in through the value parameter to the hash table. The     key parameter is not actually used, but must be included so that this function supports the bracket operators for assignment. The value parameter must be an        Article object.
    Example: "myMap[articleObj.keyword] = articleObj" This will insert something into the map with a key of the article object's keyword and a value of the article     object. 
    O(1) amortized

  delitem(key) - returns nothing, this function deletes a entire key-value pair from the map. This supports the use of brackets and the "del" keyword. In our
    implementation the value is a list of article that all share the same keyword (the value) so this function effectively deletes an entire sub-list from the hash     table. We accomplish this by calling DeleteSubList(key) from the HashTable class. Then we decrement the size of our table in the same way as in 
    DeleteValue(article) mentioned above.
    Example: "del myMap["Dirt"]" This will delete the value associated with "Dirt" and then decrement the size by the amount of objects removed.
    O(1) 
    
  contains(key) - returns a boolean. This function is used to check if a certain key has any article inserted with it in the map. The key parameter must be a           string. Then we use the Access(key) function of the HashTable to get a list of all Article objects with that keyword. If the length of the resulting list is        0 there are no articles with that as a keyword in our HashTable, so it wouldn't be in the map either. Thus we return false. Otherwise, if the length of the         resulting list is > 0, we return true. This function supports the "in" keyword.
    Example: "if ('Dirt' in myMap)..." The conditional part of this will return true if there is an article in the map with a keyword of 'Dirt'
    O(1)

-------------------------------------------------------------------------------------------------------------------------------------------------------------------

**HashTable:**
  The HashTable class has many attributes. self.LOAD_FACTOR is a constant which represents the maximum load factor. self.tableSize is the current size of our table   which is initialized to 10. self.buckets is the number of unique Article objects currently being stored in our table. self.table is the actual array that holds     our data. self.table is a list of lists, where each sub-list contains articles that all share the same keyword.
  
  Hash(article) - returns an integer that is the index in our table where we will first try to insert the article object. The article parameter needs to be an 
    Article object. We don't want the keyword to be case sensitive so we first convert the keyword to lowercase. Then, in order to have correct indexing later in
    the function, we reverse the string. Then we multiply every character in the keyword (starting at the end since we reversed it) by 27 raised to the power of the
    index of the character we are currently looking at. This part of the code was provided by Amanpreet Kappor in the Module 7 Lecture Slides on slide 30. Doing 
    this ensures that each index will be unique, at least until we modulo it with the table size. This is the next step since we want our index to be within the 
    bounds of our table.
    O(1)
    
  Insert(article) - returns nothing. This function inserts the article parameter, which needs to be an Article object, into the appropriate sub-list in the table.
    First we need to find the index that our article object should try to be inserted into. For this we pass the article parameter through the Hash() function. Then
    we start a loop that increases quadratically for the length of our table so that we can do quadratic probing if our first attempt to insert into the table          causes a collision. We modulo the quadratically increasing index (quadIndex) with table size so that it is within the bounds of our table. Then, for
    readability, we declare a variable called currIndex which will be the spot we are currently trying to insert into in the table. CurrIndex comes from adding the 
    hashed index and the quadratic index, and then modulo-ing it with the table size so that it is within the bounds. Then once we have the right index we look at
    that index in the table. If the sub-list at that spot is empty, there won't be a collision so we add this article object to the sub-list and break out of the 
    for loop since there is no need for quadratic probing. If the sub-list isn't empty two more things could happen. One, the sub-list could be the correct 
    sub-list such that all the articles in the list have the same keyword. We check if the first article in the sub-list has the same keyword as the article we are
    trying to insert, if it does we append the article object to the end of the sub-list. We also check if the current sub-list has a size greater than 0, if it 
    doesn't a index error would be thrown by trying to check the keyword of the first article in the sub-list. Two, if the sub-list doesn't represent the correct
    keyword, we continue to the top of the for-loop so that our quadratic probing can continue. After the insertion happens we now need to check if we are over the 
    load factor. To find our load factor divide the size of the table with the number of buckets in the table. If the result is greater than self.LOAD_FACTOR we 
    need to resize our table and rehash all our values. So, we multiply self.tableSize by the resizing factor which is 2. Then we declare a new table which we will 
    insert the rehashed values into so that we don't overwrite the buckets in our original table while we are still trying to access it. After declaring this table
    we add {self.tableSize} number of empty lists. Then we iterate through every sub-list in the hash table and get the new hash value for any article in that
    list. For each sub-list we assign it to the spot it goes to (using the hashIndex and quadIndex). This way we move the entire sub-list at once instead of moving
    each article object in the sub-list. This significantly decreases our time complexity from O(n) where n is the number of unique Article objects to O(b) where b
    is the number of buckets (or unique keywords) in the hash table. At the end after we have rehashed every sub-list we assign newTable to self.table.
    O(1) amortized - O(b) otherwise
    
  Access(keyword, getIndex=false) - returns a list of every article that has the same keyword as the keyword parameter. The keyword paramater must be a string. 
    The getIndex parameter lets us know if we need to return the index of the sub-list as well. We hash the keyword and then use quadratic probing to look through      the table until we find the sub-list that has that keyword. If we find it and getIndex was true we return a tuple of the sub-list and its index which is just       "currIndex" at the point where we found it. If getIndex was False we just return the sub-list. If we never find it we return a tuple of the empty list and an       index of -1 (if getIndex is True). 
    O(1)

  DeleteSubList(keyword) - returns nothing; deletes an entire sub-list from the hash table. First we get the sub-list that we want to delete and its index in the       hash table by calling the Access() function from this class. We pass in the keyword as the first parameter and then getIndex=True as the second. This returns a     tuple. We assign the first value of of the result to subList and the second value to subListIndex. Then we check if subListIndex was -1, this would indicate        that the sub-list didn't exist in which case we return because there is nothing to delete. Then we reassign the correct spot at the hash table with an empty        list, effectively deleting the contents of the list. Finally, we decrement self.buckets by the length of the sub-list we just deleted.                              O(1)                                                                                                                                                                                                                                                                                                                                  DeleteArticle(article) - returns nothing; deletes a singular article entry from the hash table. The first part of this function is very similar to                    DeleteSubList() until we confirm that the sub-list this article should exist in has contents. After that we need to find the actual article. So we iterate          through the entire sub-list until we find it. Then we use the "del" keyword to delete it from the hash table. Following that we decrement self.buckets by 1         since we just deleted something from the table. If the article doesn't exist we will have never found it and will exit the function.                                O(n) where n is the number of article objects in the sub-list. This is because we have to iterate through the entire sub-list to find the article to delete.
    
-------------------------------------------------------------------------------------------------------------------------------------------------------------------

  **Article:**
  This is the Article class of which each article becomes before being inserted into the unordered_map. Each article object has attributes of its title, keyword, 
  year published, and month published.


    
