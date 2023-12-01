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
            self.root = new_node  # First node in the tree, create root
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
            new_node.parent = parent  # Assign parent nodes
        else:
            parent.right = new_node
            new_node.parent = parent

        self.insert_helper(new_node)  # Branch to insertion helper to maintain red black properties

    def print_bfs(self, root):
        node_queue = deque()  # Queue for traversing root node then adj nodes down to leaves
        height_queue = deque()  # Height queue to print nodes on same lvl
        node_queue.append(root)
        height = 1
        height_queue.append(height)
        current_lvl = 1  # Maintain lvl to print nodes on same line

        while bool(node_queue):  # while not empty
            height = height_queue.popleft()  # Get current node and height
            current = node_queue.popleft()
            if height > current_lvl:  # Update current lvl
                print("\n")
                current_lvl = height

            print(current.datetimes, end=" ")

            if current.left is not None:  # Traverse left subtree
                node_queue.append(current.left)
                height_queue.append(height + 1)

            if current.right is not None:  # Traverse right subtree
                node_queue.append(current.right)
                height_queue.append(height + 1)

    def search_red_black(self, root, keyword):
        current = root

        while current is not None:  # While curr is not a leaf
            if current.keyword == keyword:  # Found the matching node
                return current

            if keyword < current.keyword:  # Traverse left subtree
                current = current.left
            else:
                current = current.right  # Traverse right subtree

        return -1

    def inorder_traverse(self, root):
        if root is not None:  # LNR
            yield from self.inorder_traverse(root.left)  # Yield keyword used for iter over large datasets
            yield root.keyword, root.datetimes
            yield from self.inorder_traverse(root.right)

    def delete_node(self, root):
        current = root
        keyword = root.keyword

        while current is not None:
            if current.keyword == keyword:  # Found the matching node
                self.delete_helper(current)

            if keyword < current.keyword:  # Traverse left subtree
                current = current.left
            else:
                current = current.right

    def delete_helper(self, node):
        if node is None:
            return

        original_color = node.color

        if node.left is None:
            x = node.right
            self.swap_nodes(node, x)

        elif node.right is None:
            x = node.left
            self.swap_nodes(node, x)
        else:
            if node.right.left is not None:  # Find inorder successor
                inorder_successor = node.right.left
            else:
                inorder_successor = node.right

            original_color = inorder_successor.color
            x = inorder_successor.right

            if node.right == inorder_successor:
                x.parent = inorder_successor

            else:
                self.swap_nodes(inorder_successor, inorder_successor.right)
                inorder_successor.right = node.right
                inorder_successor.right.parent = inorder_successor

            self.swap_nodes(node, inorder_successor)
            inorder_successor.left = node.left
            inorder_successor.left.parent = inorder_successor
            inorder_successor.color = node.color
        if original_color == "B":
            self.fix_rb_delete(x)

        # # Deletion w/ 2 children
        # if node.right is not None and node.left is not None:  # node is "x", inorder successor is "y"
        #     if node.right.left is not None:  # Find inorder successor
        #         inorder_successor = node.right.left
        #     else:
        #         inorder_successor = node.right
        #
        #     if parent is None:
        #         inorder_successor.left = node.left
        #         if node.right.left == inorder_successor:
        #             inorder_successor.right = node.right
        #             node.right.left = None
        #
        #         if node.right == inorder_successor:
        #             node.right = None
        #
        #         self.root = inorder_successor
        #
        #     if parent.right == node:
        #         if node.left is not None:
        #             inorder_successor.left = node.left
        #         parent.right = inorder_successor
        #
        #     else:
        #         if node.left is not None:
        #             inorder_successor.left = node.left
        #         parent.left = inorder_successor
        #
        #     if inorder_successor.color == "B" and node.color == "B":
        #         self.fix_rb_delete(inorder_successor)
        #     else:
        #         del node
        #
        # # Delete leaf node
        # if node.left is None and node.right is None:  # node is "x", double_black is "y"
        #     node.color = "B"
        #     self.fix_rb_delete(node)
        #
        # # Delete node w/ 1 child
        # if node.left is None and node.right is not None:  # node is "x", child is "y"
        #     child = node.right
        #     if parent.left == node:
        #         parent.left = child
        #     else:
        #         parent.right = child
        #
        #     if node.color == "B" and child.color == "B":
        #         self.fix_rb_delete(child)
        #     else:
        #         del node
        #
        # if node.left is not None and node.right is None:
        #     child = node.left
        #     if parent.right == node:
        #         parent.right = child
        #     else:
        #         parent.left = child
        #
        #     if node.color == "B" and child.color == "B":
        #         self.fix_rb_delete(child)
        #     else:
        #         del node

    def swap_nodes(self, a, b):
        if a.parent is None:
            self.root = b

        if a.parent.left == a:
            a.parent.left = b
        else:
            a.parent.right = b
        b.parent = a.parent

    def fix_rb_delete(self, node_to_del):
        parent = node_to_del.parent

        while not node_to_del == self.root and node_to_del.color == "B":
            if parent.left == node_to_del:
                sibling = parent.right
                if sibling is not None and sibling.color == "R":
                    sibling.color = "B"
                    parent.color = "R"
                    self.left_rotate(parent)
                    sibling = parent.right

                if sibling is not None and sibling.left.color == "B" and sibling.right.color == "B":
                    sibling.color = "R"
                    node_to_del = parent
                else:
                    if sibling is not None and sibling.right.color == "B":
                        sibling.left.color = "B"
                        sibling.color = "R"
                        self.right_rotate(sibling)
                        sibling = parent.right

                    sibling.color = parent.color
                    parent.color = "B"
                    sibling.right.color = "B"
                    self.left_rotate(parent)
                    self.root = node_to_del
            else:
                sibling = parent.left
                if sibling is not None and sibling.color == "R":
                    sibling.color = "B"
                    parent.color = "R"
                    self.right_rotate(parent)
                    sibling = parent.left

                if sibling is not None and sibling.right.color == "B" and sibling.left.color == "B":
                    sibling.color = "R"
                    node_to_del = parent
                else:
                    if sibling is not None and sibling.left.color == "B":
                        sibling.right.color = "B"
                        sibling.color = "R"
                        self.left_rotate(sibling)
                        sibling = parent.left

                    sibling.color = parent.color
                    parent.color = "B"
                    sibling.left.color = "B"
                    self.right_rotate(parent)
                    self.root = node_to_del
        # Case 2
        self.root.color = "B"
