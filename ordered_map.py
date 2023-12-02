from red_black_tree import RedBlackTree


class OrderedMap:
    def __init__(self):
        self.rb_tree = RedBlackTree()

    def __setitem__(self, keyword, articles):
        res = self.rb_tree.search_red_black(self.rb_tree.root, keyword)
        # if res == keyword:
        # delete (not in final build because unnecessary
        self.rb_tree.insert_node(self.rb_tree.root, keyword, articles)

    def __getitem__(self, keyword):
        return self.rb_tree.search_red_black(self.rb_tree.root, keyword).articles

    def print_map_contents(self):
        self.rb_tree.print_bfs(self.rb_tree.root)

    def __iter__(self):
        return self.rb_tree.inorder_traverse(self.rb_tree.root)

    def get_item_count(self):
        return self.rb_tree.node_count
