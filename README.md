# Created by Shane Downs, Wilson Goins, and Leonardo Cobaleda

Welcome to the README for the unordered_map section of the TrendLens project.

The unordered map class needs two other files to work, a class called Article and a class called HashTable that is the backend of the map.


**unordered_map:**
  Contains attributes self.map and self.size. Attribute self.map is what holds the actual data and self.size is the number of unique Article objects in our map.
  Keys in our map are the keywords of articles, values are lists of all the articles with that keyword. Keys/keywords are NOT case-sensitive.
  
  ClearMap() - erases all the data inside the map by replacing self.map with a new instance of the HashTable class.
    O(1)
    
  GetSize() - returns self.map which is the number of unique Article objects that have been added to our map.
    O(1)
    
  __getitem__(key) - returns a list of all the items in the map that have the same keyword as the key parameter. If the key input does not exist in the map, there      is nothing to return so the function will return an empty list. This supports the use of brackets to access values from the map. This function works by using       the Access(key) function of the HashTable class (detailed below). The key must be a string.
    Example: "keyList = myMap["Dirt"]" This will assign a list of all the Article objects with the keyword "Dirt" to keyList.
    O(1) 
    
  __setitem__(key, value) - returns nothing, this function is used to insert something into the map. It increments the self.size attribute of the unordered_map     
    instance. Then it uses the Insert(value) function of the HashTable class to add the Article object passed in through the value parameter to the hash table. The     key parameter is not actually used, but must be included so that this function supports the bracket operators for assignment. The value parameter must be an        Article object.
    Example: "myMap[articleObj.keyword] = articleObj" This will insert something into the map with a key of the article object's keyword and a value of the article     object. 
    O(1) amortized
    
  __contains(key)__ - returns a boolean. This function is used to check if a certain key has any article inserted with it in the map. The key parameter must be a       string. Then we use the Access(key) function of the HashTable to get a list of all Article objects with that keyword. If the length of the resulting list is        0 there are no articles with that as a keyword in our HashTable, so it wouldn't be in the map either. Thus we return false. Otherwise, if the length of the         resulting list is > 0, we return true. This function supports the "in" keyword.
    Example: "if ('Dirt' in myMap)..." The conditional part of this will return true if there is an article in the map with a keyword of 'Dirt'
    O(1)


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
    we add self.tableSize number of empty lists. Then we iterate through every article in the hash table and get the new hash value. For each of these article we 
    go through the aforementioned process of inserting something into the table and using quadratic probing to resolve collisions. At the end after we have rehashed
    the entire list we assign self.table with newTable. This may be able to improved by rehashing only the first article from every sub-list and inserting the 
    entire list at the new spot.
    O(1) amortized
    
  Access(keyword) - returns a list of every article that has the same keyword as the keyword parameter. The keyword paramater must be a string. We hash the keyword
    and then use quadratic probing to look through the table until we find the sub-list that has that keyword. If we never find it we return an empty list.
    O(1)
    

  **Article:**
  This is the Article class of which each article becomes before being inserted into the unordered_map. Each article object has attributes of its title, keyword, 
  year published, and month published.


    
