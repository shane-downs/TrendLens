class Node:
    def __init__(self, keyword, datetimes):
        self.left = None
        self.right = None
        self.parent = None
        self.keyword = keyword
        self.height = 0
        self.datetimes = datetimes
        self.color = "R"
        self.double_black = False
