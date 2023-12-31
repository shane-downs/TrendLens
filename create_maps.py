from ordered_map import OrderedMap
from unordered_map import unordered_map
import csv
from fetch import Article, getArticlesFromMapsAndInsertToCSV
from timeit import default_timer as timer
import time


def read_csv_to_list():  # Returns list of article objects found in csv (~900,000 data points/articles in csv)
    csvfile = open('nyt_data.csv', newline='', encoding='utf-8', errors='replace')

    c = csv.reader(csvfile)

    articles_list = []
    for row in c:
        a = Article()
        a.title = row[0]
        a.year = row[1]
        a.month = row[2]
        a.url = row[3]
        end_first_index = row[4].find(',')
        if end_first_index == -1:
            a.keyword = row[4]
        else:
            a.keyword = row[4][:end_first_index]

        articles_list.append(a)
        # # Print statements moved inside the loop
        # print(a.title)
        # print(a.year)
        # print(a.month)
        # print(a.url)
        # print(a.keyword)
        # print("\n")  # Add a newline for better readability
    return articles_list


def create_ordered_map(art_list):
    # do insertion
    ordered_map = OrderedMap()
    for i in range(len(art_list)):
        ordered_map[art_list[i].keyword] = art_list[i]

    return ordered_map


def create_unordered_map(art_list):

    # do insertion
    unorderedMap = unordered_map()
    for i in range(len(art_list)):
        unorderedMap[art_list[i].keyword] = art_list[i]

    return unorderedMap


def create_map_of_keywords():
    csvfile = open('nyt_data.csv', newline='', encoding='utf-8', errors='replace')
    c = csv.reader(csvfile)
    suggestions_set = set()
    suggestions = []
    for row in c:
        word = row[4].split(',')
        first_word = word[0].strip()
        suggestions_set.add(first_word)

    for elem in suggestions_set: 
        suggestions.append(elem)
    return suggestions


if __name__ == "__main__":
    articles_list = read_csv_to_list()
    # get information for ordered map
    nyt_ordered_map = create_ordered_map(articles_list)
    # get information for unordered map
    nyt_unordered_map = create_unordered_map(articles_list)
    getArticlesFromMapsAndInsertToCSV("Movies", 2000, 2019, nyt_unordered_map, nyt_ordered_map)
