class Node:
    # Constructor
    def __init__(self,key):
        self.left = None
        self.right = None
        self.val = key

    # Insert function
    def insert(root,node):
        if root is None:
            root = node
        else:
            if root.val < node.val:
                if root.right is None:
                    root.right = node
                else:
                    Node.insert(root.right, node)
            else:
                if root.left is None:
                    root.left = node
                else:
                    Node.insert(root.left, node)

     # Sorting Binary tree from least to greatest                   
    def Sort(root):
        if root:
            Node.Sort(root.left)
            print(root.val)
            Node.Sort(root.right)

# Main method

if __name__ == "__main__":
    print("Please enter 10 numbers: ")
    num = 0
    n = Node(50)
    for x in range(0, 10):
        num = int(input())
        Node.insert(n,Node(num))
    Node.Sort(n)
