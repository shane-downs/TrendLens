# **TrendLens**: COP3530 Group 29 Final Project Submission
_Created by Shane Downs, Wilson Goins, and Leonardo Cobaleda_

## Link to Video Demo:
https://youtu.be/-Cwc7H2krQw

## Project Description:

### Inspiration:

As avid followers of news and current events, the team brainstormed ideas on how we can enagage more with the news media.
We wanted a way to visualize trending topics in the news over time. This not only helps keep the news media accountable
by tracking public opinion agendas, but it also is an entertaining way to see how your interests have been represented in
the media over time. By creating TrendLens, we have given ourselves and others a tool to directly interact with the news they consume.

### What it Does:

TrendLens is a data analysis web-app that allows users to enter a year range (start year - end year) and a "keyword" to see the frequency of this keyword appearing 
in New York Times articles. A keyword is what the New York Times deems to be the focal point or main category the article fits in to. 
For example, an article about the 2016 NBA Finals may have the primary keyword being "NBA", "Stephen Curry", or "LeBron James".
The user's input will then be processed into a line graph with the x-axis being the year range and y-axis being the amount of articles
that keyword is associated with. Users can also click the "Generate Random Input" button generate a line graph for a random year range and keyword.
The graph's UI features many tools like zooming, lasso-select, and interactive components to enhance the user's experience.
The keyword input field also contains an autofill dropdown to aid in the keyword selection process.

### How We Built It:

The TrendLens web-app was created using the dash framework and plotly library for embedding a graph in the website.
We used HTML and CSS for the frontend and Python and the New York Times Developer API for the backend. Our class, Data
Structures and Algorithms (COP3530), required us to use two comparable data structures created from scratch and analyze
their operations' performance with a large data set. Our data set contains metrics from over 900,000 articles from the
New York Times Archive API. In the beginning of the project, we fetched all published articles spanning the period of 1853 to 2023 and wrote
their data points to a csv files titled `nyt_data.csv`. In our backend processes, we read data from that csv file for use in the graph front end.
A future improvement to TrendLens that the group hopes to achieve is to implement a database and Amazon AWS EC2 instance that runs the
backend processes constantly so the website will always have the newest articles and keywords available to plot. For now, TrendLens
provides a comprehensive graphical analysis of over 100,000 keywords spanning the period 1853 to December 2023. The ordered-map
we used is backed by a red-black tree and the unordered map is backed by a hash map data structure with a custom hashing algorithm.

### Challenges We Ran Into:

We struggled with finding a way to constantly fetch data from the New York Times API whenever the user inputs the year range
and keyword. The NYT API also has a request limit that inhibited our ability to implement this feature. We decided that
writing data to a csv and referencing that data throughout the web-app's runtime was the best approach given the circumstances.


### Accomplishments:

We are proud to have used the New York Times' open source developer API to generate a massive data set for use in this project.
Our class's final project description only required us to use >100,000 data points and we far exceeded this expectation by using
900,000. We also are proud to have been able to utilize the dash library to effectively display data to the user in
a way that is highly customizable and offers many tools to improve their experience. Lastly, navigating the logic of the backend
red-black tree and hash map data structures was difficult but rewarding to implement in Python as opposed to C++.

### What's Next for TrendLens?

We hope to implement constant data fetching from the NYT Archive API. This would require a backend database so we hope to implement
that functionality later on. Additionally, we hope to add more features to side-bar of the website.



## SETUP:
* Clone the repository
* Setup a Python virtual environment or use local interpreter.
* Pip install dependencies listed below
* Run app.py and click on local host link in output terminal

## Dependencies (Pip Install)
* _dash_
* _pandas_
* _csv_
* _plotly.express_
* _statsmodels.api_
* Optional: _requests_

### App.py is driver file, create_maps.py contains most backend processes including the reading and writing of NYT article data from nyt_data.csv and insertion to map data structures


# Description of Backend Processes

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
    
  getitem(key) - returns a list of all the items in the map that have the same keyword as the key parameter. If the key does not exist in the map, there      is
    nothing to return so the function will return an empty list. This supports the use of brackets to access values from the map. This function works by using      
    the Access(key) function of the HashTable class (detailed below). The key must be a string.
    Example: "keyList = myMap["Dirt"]" This will assign a list of all the Article objects with the keyword "Dirt" to keyList.
    O(1) 
    
  setitem(key, value) - returns nothing, this function is used to insert something into the map. It increments the self.size attribute of the unordered_map     
    instance. Then it uses the Insert(value) function of the HashTable class to add the Article object passed in through the value parameter to the hash table. The     key parameter is not actually used, but must be included so that this function supports the bracket operators for assignment. The value parameter must be an        Article object.
    Example: "myMap[articleObj.keyword] = articleObj" This will insert something into the map with a key of the article object's keyword and a value of the article     object. 
    O(1) amortized
    
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
    
  Access(keyword) - returns a list of every article that has the same keyword as the keyword parameter. The keyword paramater must be a string. We hash the keyword
    and then use quadratic probing to look through the table until we find the sub-list that has that keyword. If we never find it we return an empty list.
    O(1)
    
-------------------------------------------------------------------------------------------------------------------------------------------------------------------

  **Article:**
  This is the Article class of which each article becomes before being inserted into the unordered_map. Each article object has attributes of its title, keyword, 
  year published, and month published.
-------------------------------------------------------------------------------------------------------------------------------------------------------------------

-------------------------------------------------------------------------------------------------------------------------------------------------------------------
**OrderMap**
__init__: Initializes an OrderedMap object. It has an O(1) time complexity.

__setitem__: Inserts a keyword and its corresponding articles into the ordered map. This function has an O(log N) time complexity, where N is the number of keywords in the map.

__getitem__: Retrieves the articles associated with a given keyword. This function has an O(log N) time complexity, where N is the number of keywords in the map.

print_map_contents: Prints the contents of the ordered map using a breadth-first search traversal. This function has an O(N) time complexity, where N is the total number of nodes in the underlying Red-Black Tree.

__iter__: Returns an iterator for the ordered map using an inorder traversal of the underlying Red-Black Tree. This function has an O(N) time complexity, where N is the total number of nodes in the underlying Red-Black Tree.

get_item_count: Returns the count of items (keywords) in the ordered map. It has an O(1) time complexity.

-------------------------------------------------------------------------------------------------------------------------------------------------------------------

**RedBlackTree**
__init__: Initializes a Red-Black Tree object. It has an O(1) time complexity.

left_rotate: Performs a left rotation on the Red-Black Tree. This function has an O(1) time complexity.

right_rotate: Performs a right rotation on the Red-Black Tree. This function has an O(1) time complexity.

insert_helper: Helps with the insertion of a new node while maintaining the Red-Black Tree properties. This function has an O(log N) time complexity, where N is the number of nodes in the tree.

insert_node: Inserts a new node into the Red-Black Tree. This function has an O(log N) time complexity, where N is the number of nodes in the tree.

print_bfs: Prints the Red-Black Tree using a breadth-first search traversal. This function has an O(N) time complexity, where N is the total number of nodes in the tree.

search_red_black: Searches for a node with a specific keyword in the Red-Black Tree. This function has an O(log N) time complexity, where N is the number of nodes in the tree.

inorder_traverse: Performs an inorder traversal of the Red-Black Tree. This function has an O(N) time complexity, where N is the total number of nodes in the tree.

delete_node: Deletes a node from the Red-Black Tree. This function has an O(log N) time complexity, where N is the number of nodes in the tree.

delete_helper: Assists in the deletion of a node while maintaining the Red-Black Tree properties. This function has an O(log N) time complexity, where N is the number of nodes in the tree.

swap_nodes: Swaps two nodes in the Red-Black Tree. It has an O(1) time complexity.

fix_rb_delete: Fixes the Red-Black Tree after a deletion to maintain its properties. This function has an O(log N) time complexity, where N is the number of nodes in the tree.xity, where N is the number of keywords in the map.

-------------------------------------------------------------------------------------------------------------------------------------------------------------------
**fetch.py:**
writeArticlesToRawCSV(array): Writes Article objects to a CSV file. The time complexity is O(n), where n is the number of Article objects in the array. This function is a one-time operation to store articles in a CSV format.
  
getArticlesFromAPI(array, startYear, endYear): Fetches articles from the New York Times Archive API within a specified year range. The time complexity is O(k * m), where k is the range of years and m is the number of months per year. This function populates an array with Article objects retrieved from the API.

getArticlesFromMapsAndInsertToCSV(keyword, startYear, endYear, unorderedMap, orderedMap): Accesses data from unordered and ordered maps, records usage statistics, and writes results to a new CSV file. The time complexity is O(u + o), where u is the time to access data from the unordered map and o is the time to access data from the ordered map. This function provides insights into keyword usage over a specified time range.

-------------------------------------------------------------------------------------------------------------------------------------------------------------------

**create_maps.py:**
read_csv_to_list(): Reads data from a CSV file and creates a list of Article objects. The time complexity is O(c), where c is the number of rows in the CSV file. This function is part of the initial data loading process.
  
create_ordered_map(articles_list): Creates an ordered map from a list of Article objects. The time complexity is O(n), where n is the number of Article objects in the list. This function transforms raw data into an ordered map for efficient keyword-based retrieval.
  
create_unordered_map(articles_list): Creates an unordered map from a list of Article objects. The time complexity is O(n), where n is the number of Article objects in the list. Similar to `create_ordered_map`, this function transforms raw data into an unordered map, optimizing for fast access.

