from red_black_tree import RedBlackTree

class OrderedMap:
    def __init__(self):
        self.rb_tree = RedBlackTree()

    def __setitem__(self, keyword, datetimes):
        res = self.rb_tree.search_red_black(self.rb_tree.root, keyword)
        if res != -1:
            self.rb_tree.delete_node(res)
        self.rb_tree.insert_node(self.rb_tree.root, keyword, datetimes)

    def __getitem__(self, keyword):
        return self.rb_tree.search_red_black(self.rb_tree.root, keyword).datetimes

    def print_map_contents(self):
        self.rb_tree.print_bfs(self.rb_tree.root)

    def __iter__(self):
        return self.rb_tree.inorder_traverse(self.rb_tree.root)
