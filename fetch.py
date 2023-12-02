import requests
import csv
import time
from ordered_map import OrderedMap
from unordered_map import unordered_map


class Article:
    def __init__(self, title="", year="", month="", url="", keywords=""):
        self.title = title
        self.year = year
        self.month = month
        self.url = url
        self.keyword = keywords


def writeArticlesToRawCSV(array):    # never used again since we only needed to do it once
    col_headers = ["Title", "Year", "Month", "Url", "Keyword"]
    filename = "nyt_data.csv"
    with open(filename, 'w', encoding='utf-8', newline='') as csvfile:
        # creating a csv writer object
        csvwriter = csv.writer(csvfile)

        # writing the fields
        csvwriter.writerow(col_headers)

        for i in array:
            # writing the data rows
            row = [i.title, i.year, i.month, i.url, ", ".join(i.keyword)]
            csvwriter.writerow(row)


def getArticlesFromAPI(array, startYear, endYear):     # never used again since we only needed to do it once
    api_key = 'rw3uRjFP0HcePAbOw7629sEzEWSnfZcU'

    # iterating through entire new york times archive api
    for i in range(startYear, endYear):
        for j in range(1, 13):
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
                        year_pub = time[0:4]
                        month_pub = time[6:7]

                        # extracting  keywords
                        keywords = [article_data.get('keywords', [])[0]['value']] if article_data.get(
                            'keywords') else []
                        if not keywords:
                            continue

                        array.append(Article(title, year_pub, month_pub, url, keywords))

                    # for article_info in array:
                    #     print("Title:", article_info.title)
                    #     print("URL:", article_info.url)
                    #     print("Date Published:", article_info.year, "-", article_info.month)
                    #     print("Keywords:", ", ".join(article_info.keyword))
                    #     print("\n" + "=" * 50 + "\n")
                else:
                    print("Error: 'response' or 'docs' keys not found in the API response.")
            else:
                # Print an error message if the request was not successful
                print(f"Error: {response.status_code}, {response.text}")

            return array


def getArticlesFromMapsAndInsertToCSV(keyword, startYear, endYear, unorderedMap, orderedMap):
    # we need to track time so the following is time for unordered map
    startTimeUnordered = time.time()
    garbage = unorderedMap[keyword]       # get the data (should take a bit), but don't store it because we don't need two
    endTimeUnordered = time.time()
    UnorderedElapsed = endTimeUnordered - startTimeUnordered

    # we need to track time so the following is time for ordered map
    startTimeOrdered = time.time()
    dataList = orderedMap[keyword]  # get the data (should take a bit)
    endTimeOrdered = time.time()
    OrderedElapsed = endTimeOrdered - startTimeOrdered

    usageMap = {}                               # map to hold key of year and value of usages in that year
    formattedList = [["Year", "Usage"]]

    for i in range(len(dataList)):       # go through list to check article dates
        if ((startYear <= dataList[i].year) and (endYear >= dataList[i].year)):   # if we are within the year range
            usageMap[dataList[i].year] += 1      # increment the usage of the keyword at that year in the map
        else:       # if we are not in the right range, continue
            continue

    # now we have a map of all the right usages, we need to put that into a list and then write that list to a new CSV
    for pair in usageMap:
        formattedList.append([pair.first, pair.second])     # add each piece of data to the new list

    # now let's write to the CSV
    filePath = 'formatted_nyt_data.csv'
    with open(filePath, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(formattedList)


if __name__ == "__main__":
    arr = []            # initialize array
    arr = getArticlesFromAPI(arr, 1852, 2022)       # get all the articles from the API
    writeArticlesToRawCSV(arr)      # this creates (or overwrites) a new csv called "nyt_data.csv"
