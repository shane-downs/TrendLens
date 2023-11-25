from node import Node
from collections import deque
'''
Code snippets from Shane Downs Gator AVL project 1 submission
red black tree algorithm advice from Programiz
'''


class RedBlackTree:

    def __init__(self):
        self.root = None

    def left_rotate(self, n):
        child = n.right
        n.right = child.left
        if child.left is not None:
            child.left.parent = n

        child.parent = n.parent
        if n.parent is None:
            self.root = child

        elif n.parent.left == n:
            n.parent.left = child

        else:
            n.parent.right = child

        child.left = n
        n.parent = child

    def right_rotate(self, n):
        child = n.left
        n.left = child.right
        if child.right is not None:
            child.right.parent = n

        child.parent = n.parent

        if n.parent is None:
            self.root = child

        elif n.parent.right == n:
            n.parent.right = child

        else:
            n.parent.left = child

        child.right = n
        n.parent = child

    def insert_helper(self, new_node):
        parent = new_node.parent
        grandparent = parent.parent
        while parent.color == "R":
            if parent == grandparent.right:
                uncle = grandparent.left
                if uncle is not None and uncle.color == "R":
                    parent.color, uncle.color = "B", "B"
                    grandparent.color = "R"
                    new_node = grandparent
                else:
                    if new_node == parent.left:
                        new_node = parent
                        self.right_rotate(new_node)
                    parent.color = "B"
                    grandparent.color = "R"
                    self.left_rotate(grandparent)
            else:
                uncle = grandparent.right
                if uncle is not None and uncle.color == "R":
                    parent.color, uncle.color = "B", "B"
                    grandparent.color = "R"
                    new_node = grandparent
                else:
                    if new_node == parent.right:
                        new_node = parent
                        self.left_rotate(new_node)

                    parent.color = "B"
                    grandparent.color = "R"
                    self.right_rotate(grandparent)
            if new_node == self.root:
                break
        self.root.color = "B"

    def insert_node(self, root, keyword, datetimes):
        new_node = Node(keyword, datetimes)
        if root is None:
            new_node.color = "B"
            self.root = new_node
            return root

        current = root
        parent = None

        while current is not None:
            parent = current
            if keyword < current.keyword:
                current = current.left
            else:
                current = current.right

        if keyword < parent.keyword:
            new_node.color = "R"
            parent.left = new_node
            new_node.parent = parent
        else:
            new_node.color = "R"
            parent.right = new_node
            new_node.parent = parent

        self.insert_helper(new_node)

    def print_bfs(self, root):
        node_queue = deque()
        height_queue = deque()
        node_queue.append(root)
        height = 1
        height_queue.append(height)
        current_lvl = 1

        while bool(node_queue):
            height = height_queue.popleft()
            current = node_queue.popleft()
            if height > current_lvl:
                print("\n")
                current_lvl = height

            print(current.keyword, end=" ")

            if current.left is not None:
                node_queue.append(current.left)
                height_queue.append(height + 1)

            if current.right is not None:
                node_queue.append(current.right)
                height_queue.append(height + 1)

    def search_red_black(self, root, keyword):
        current = root

        while current is not None:
            if current.keyword == keyword:
                return current

            if keyword < current.keyword:
                current = current.left
            else:
                current = current.right

        return root
