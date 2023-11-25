from red_black_tree import RedBlackTree
from node import Node

if __name__ == "__main__":
    rb_tree = RedBlackTree()
    rb_tree.insert_node(rb_tree.root, "NBA", "10/17/2004")
    rb_tree.insert_node(rb_tree.root, "Rob Gronkowski", "1/12/2008")
    rb_tree.insert_node(rb_tree.root, "Jamie Benn", "9/19/2009")
    rb_tree.insert_node(rb_tree.root, "Peter James", "6/16/2066")
    rb_tree.insert_node(rb_tree.root, "Michael Jordan", "3/33/2033")
    rb_tree.insert_node(rb_tree.root, "Lebron Alan", "1/12/2077")
    node = rb_tree.search_red_black(rb_tree.root, "Michael Jordan")
    print(f"\n {node.datetimes}")
