class Node:
    def __init__(self, keyword, article):
        self.articles = []
        self.left = None
        self.right = None
        self.parent = None
        self.keyword = keyword
        self.height = 0
        self.article = article
        self.color = "R"
