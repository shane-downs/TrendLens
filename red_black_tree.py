from node import Node
from collections import deque


class RedBlackTree:

    def __init__(self):
        self.height = 0
        self.root = None
        self.ll = False
        self.lr = False
        self.rr = False
        self.rl = False

    def insert_helper(self, new_node):


    def insert_node(self, root, keyword, datetimes):
        new_node = Node(keyword, datetimes)
        if root is None:
            new_node.color = "B"
            root = new_node
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

    def print_inorder(self, root):
        pass

    def print_bfs(self, root):
        node_queue = deque()
        height_queue = deque()
        node_queue.append(root)
        height = 1
        height_queue.append(height)
        current_lvl = 1

        while not node_queue:
            height = height_queue.popleft()
            current = node_queue.popleft()

            if height > current_lvl:
                current_lvl = height

            if current.left:
                node_queue.append(current.left)
                height_queue.append(height + 1)

            if current.right:
                node_queue.append(current.right)
                height_queue.append(height + 1)
