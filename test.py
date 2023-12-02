from ordered_map import OrderedMap
from fetch import *

if __name__ == "__main__":
    nyt_map = OrderedMap()
    articles = []
    articles = getArticles(articles, 2019, 2020)
    print(articles)

