from ordered_map import OrderedMap
from fetch import Article

if __name__ == "__main__":
    a = Article("James Madison", "2022", "January", "Shane.com", "Wilson")
    b = Article("Jimbo", "1995", "Feb", "Alan.com", "Roger")
    nyt_map = OrderedMap()
    nyt_map["Michael Jordan"] = a
    nyt_map["Michael Jordan"] = b

    print(nyt_map["Michael Jordan"][0].title)
    print(nyt_map["Michael Jordan"][1].title)
    print(nyt_map.get_item_count())
