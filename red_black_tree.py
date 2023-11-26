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
            self.root = new_node   # First node in the tree, create root
            return root

        current = root
        parent = None

        while current is not None:
            parent = current
            if keyword < current.keyword:  # Traverse left subtree
                current = current.left
            else:
                current = current.right  # Traverse right subtree

        if keyword < parent.keyword:
            parent.left = new_node
            new_node.parent = parent   # Assign parent nodes
        else:
            parent.right = new_node
            new_node.parent = parent

        self.insert_helper(new_node)  # Branch to insertion helper to maintain red black properties

    def print_bfs(self, root):
        node_queue = deque()   # Queue for traversing root node then adj nodes down to leaves
        height_queue = deque()  # Height queue to print nodes on same lvl
        node_queue.append(root)
        height = 1
        height_queue.append(height)
        current_lvl = 1  # Maintain lvl to print nodes on same line

        while bool(node_queue):  # while not empty
            height = height_queue.popleft()   # Get current node and height
            current = node_queue.popleft()
            if height > current_lvl:   # Update current lvl
                print("\n")
                current_lvl = height

            print(current.datetimes, end=" ")

            if current.left is not None:    # Traverse left subtree
                node_queue.append(current.left)
                height_queue.append(height + 1)

            if current.right is not None:   # Traverse right subtree
                node_queue.append(current.right)
                height_queue.append(height + 1)

    def search_red_black(self, root, keyword):
        current = root

        while current is not None:   # While curr is not a leaf
            if current.keyword == keyword:   # Found the matching node
                return current.datetimes

            if keyword < current.keyword:   # Traverse left subtree
                current = current.left
            else:
                current = current.right   # Traverse right subtree

        return root.datetimes

    def inorder_traverse(self, root):
        if root is not None:    # LNR
            yield from self.inorder_traverse(root.left)  # Yield keyword used for iter over large datasets
            yield root.keyword, root.datetimes
            yield from self.inorder_traverse(root.right)

    def delete_node(self, root, keyword):
        current = root

        while current is not None:
            if current.keyword == keyword:  # Found the matching node
                self.delete_helper(current)

            if keyword < current.keyword:  # Traverse left subtree
                current = current.left
            else:
                current = current.right

    def delete_helper(self, node):
        original_color = node.color

        # Delete leaf node
        if node.left is None and node.right is None:
            if node.parent.left == node:
                node.parent.left = None
            else:
                node.parent.right = None

            node.double_black = True

        # Delete node w/ 1 child
        elif node.left is None and node.right is not None:
            parent = node.parent
            child = node.right
            if parent.left == node:
                parent.left = child
            else:
                parent.right = child

            del node

        elif node.left is not None and node.right is None:
            parent = node.parent
            child = node.left
            if parent.right == node:
                parent.right = child
            else:
                parent.left = child

            del node

        # Deletion w/ 2 children
        elif node.right is not None:
            parent = node.parent

            if node.right.left is not None:
                inorder_successor = node.right.left
            else:
                inorder_successor = node.right

            if parent == node:
                inorder_successor.left = node.left
                if node.right.left == inorder_successor:
                    inorder_successor.right = node.right
                    node.right.left = None

                if node.right == inorder_successor:
                    node.right = None

                self.root = inorder_successor

                del node

            if parent.right == node:
                if node.left is not None:
                    inorder_successor.left = node.left
                parent.right = inorder_successor
                del node

            else:
                if node.left is not None:
                    inorder_successor.left = node.left
                parent.left = inorder_successor
                del node
