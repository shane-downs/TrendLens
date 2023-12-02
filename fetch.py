import requests
import csv
from unordered_map import unordered_map
from ordered_map import OrderedMap


class Article:
    def __init__(self, headline="None", year=1861, month=1, url="www.newyorktimes.com", keywords="None"):
        self.title = headline
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
                        print("Title:", article_info.title)
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


# def insertArticles():
#     # title, year, month, url, keyword
#     fileName = "TrendLens/nyt_data.csv"
#     orderedMap = OrderedMap()
#     unorderedMap = unordered_map()
#
#     # read from the csv and make into an article object
#     articleList = []
#     with open(fileName, 'r') as file:
#         csvReader = csv.reader(file)       # reader from csv module to help
#
#         # skip the header row
#         next(csvReader, None)
#
#         # for every row in the file
#         for row in csvReader:
#             # get data from row
#             title = row[0]
#             year = int(row[1])
#             month = int(row[2])
#             url = row[3]
#             keyword = row[4]        # just get the first one and forget the rest of the keywords for now
#             # make into an article object
#             newObject = Article(title, year, month, url, keyword)
#             articleList.append(newObject)
#     # insert the stuff into the maps
#     for article in articleList:
#         orderedMap[article.keyword] = article
#         unorderedMap[article.keyword] = article
#
#     print("unordered map: ", unorderedMap.GetSize())


if __name__ == "__main__":
    # title, year, month, url, keyword
    fileName = "TrendLens/nyt_data.csv"
    orderedMap = OrderedMap()
    unorderedMap = unordered_map()

    # read from the csv and make into an article object
    articleList = []
    with open(fileName, 'r') as file:
        csvReader = csv.reader(file)  # reader from csv module to help

        # skip the header row
        next(csvReader, None)

        # for every row in the file
        for row in csvReader:
            # get data from row
            title = row[0]
            year = int(row[1])
            month = int(row[2])
            url = row[3]
            keyword = row[4]  # just get the first one and forget the rest of the keywords for now
            # make into an article object
            newObject = Article(title, year, month, url, keyword)
            articleList.append(newObject)
    # insert the stuff into the maps
    for art in articleList:
        # put into the maps
        orderedMap[art.keyword] = art
        unorderedMap[art.keyword] = art

    # print the size of the unordered map
    print("unordered map: ", unorderedMap.GetSize())


