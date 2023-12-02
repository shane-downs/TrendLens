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


def getArticles(startYear, endYear):
    api_key = 'CqAGNdgXrh1N2aDKZhnF7tWLeAKrDYwj'
    articleArray = [["test1", "test1", "test1", "test1", "test1"]]

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
                        # old (got all keys) keywords = [keyword['value'] for keyword in article_data.get('keywords', [])]
                        # new (gets 1st key) \/
                        keywords = [article_data.get('keywords', [])[0]['value']] if article_data.get('keywords') else []

                        articleArray.append([title, yearPub, monthPub, url, keywords])

                    for article_info in articleArray:
                        print("got one!")
                        # print("Title:", article_info.headline)
                        # print("URL:", article_info.url)
                        # print("Date Published:", article_info.year, "-", article_info.month)
                        # print("Keywords:", ", ".join(article_info.keywords))
                        # print("\n" + "=" * 50 + "\n")
                else:
                    print("Error: 'response' or 'docs' keys not found in the API response.")
            else:
                # Print an error message if the request was not successful
                print(f"Error: {response.status_code}, {response.text}")

    # now we have an array with all the articles
    file = "new_nyt_data.csv"
    fields = ["title", "year", "month", "url", "keyword"]
    # write to the file
    with open(file, 'w') as file:
        csvWriter = csv.writer(file)        # helper for writing
        csvWriter.writerow(fields)
        csvWriter.writerows(articleArray)


def insertArticles(_unorderedMap, _orderedMap):
    fileName = 'nyt_data.csv'     # name of file
    articleList = []        # list of article objects

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

            # if (month == 2):
            print("title = ", title, " | keyword = ", keyword, " | year = ", year, " | month = ", month)

            # make a new article object
            currentObj = Article(title, year, month, title, keyword)
            # add it to the list
            articleList.append(currentObj)

        # insert all articles into the maps
        for art in articleList:
            _unorderedMap[art.keyword] = art     # put into map
            # _orderedMap[art.keyword] = art       # put into map


if __name__ == "__main__":
    getArticles(2000, 2001)

    # orderedMap = OrderedMap()               # empty ordered map
    # unorderedMap = unordered_map()          # empty unordered map
    # insertArticles(unorderedMap, orderedMap)
    #
    # for article in unorderedMap["Unites States Politics and Government"]:
    #     print(article.title, " -- ", article.year)
