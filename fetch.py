import requests
import csv
from ordered_map import OrderedMap
from unordered_map import unordered_map


class Article:
    def __init__(self, title, year, month, url, keywords):
        self.title = title
        self.year = year
        self.month = month
        self.url = url
        self.keyword = keywords


def getArticles(arr, startYear, endYear):
    api_key = 'CqAGNdgXrh1N2aDKZhnF7tWLeAKrDYwj'

    # iterating through entire new york times archive api
    for i in range(startYear, endYear):
        for j in range(13):
            year = i
            month = j
    

            url = f'https://api.nytimes.com/svc/archive/v1/{year}/{month}.json?api-key={api_key}'

            # API call
            response = requests.get(url)

            # checking success code
            if response.status_code == 200:
                # parsing json file
                data = response.json()

                # checking for response and docs inside the data
                if 'response' in data and 'docs' in data['response']:

                    for article_data in data['response']['docs']:
                        # checking for publish dates aka checking if the month of articles is empty
                        if 'pub_date' not in article_data:
                            continue
                        
                        # titles, url, time 
                        title = article_data['headline']['main']
                        url = article_data['web_url']
                        # time structure is "year-month-day-hours:minutes:seconds+0000"
                        # ex: 2019-01-01T05:00:00+0000"
                        # T is just a string to represent time

                        time = article_data['pub_date']
                        yearPub = time[0:4]
                        monthPub = time[6:7]

                        # extracting  keywords
                        keywords = [keyword['value'] for keyword in article_data.get('keywords', [])]

                        arr.append(Article(title, yearPub, monthPub, url, keywords))

                    for article_info in arr:
                        print("Title:", article_info.headline)
                        print("URL:", article_info.url)
                        print("Date Published:", article_info.year, "-", article_info.month)
                        print("Keywords:", ", ".join(article_info.keywords))
                        print("\n" + "=" * 50 + "\n")
                else:
                    print("Error: 'response' or 'docs' keys not found in the API response.")
            else:
                # Print an error message if the request was not successful
                print(f"Error: {response.status_code}, {response.text}")

            return arr


def insertArticles():
    fileName = 'TrendLens/nyt_data.csv'     # name of file
    articleList = []        # list of article objects
    orderedMap = OrderedMap()               # empty ordered map
    unorderedMap = unordered_map()          # empty unordered map

    with open(fileName, 'r') as file:
        csvReader = csv.reader(file)       # helper to read the csv file from the CSV package

        # skip the header row       - format is "TITLE,YEAR,MONTH,KEYWORD"
        next(csvReader, None)

        for row in csvReader:
            # Assuming a CSV with two columns, modify accordingly for more columns
            title = row[0]
            year = int(row[1])
            month = int(row[2])
            url = row[3]
            keyword = row[4]        # just get the first keyword
            # make a new article object
            currentObj = Article(title, year, month, title, keyword)
            # add it to the list
            articleList.append(currentObj)

        # insert all articles into the maps
        for article in articleList:
            unorderedMap[article.keyword] = article     # put into map
            orderedMap[article.keyword] = article       # put into map

        # now print the size of the maps
        print(unorderedMap.GetSize())
