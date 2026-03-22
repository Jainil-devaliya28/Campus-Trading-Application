from graphviz import Digraph

# B+ Tree Node class. Can be used as either internal or leaf node.
class BPlusTreeNode:
    def __init__(self, order, is_leaf=True):
        self.order = order                  # Maximum number of children a node can have
        self.is_leaf = is_leaf              # Flag to check if node is a leaf
        self.keys = []                      # List of keys in the node
        self.values = []                    # Used in leaf nodes to store associated values
        self.children = []                  # Used in internal nodes to store child pointers
        self.next = None                    # Points to next leaf node for range queries

    def is_full(self):
        # A node is full if it has reached the maximum number of keys (order - 1)
        return len(self.keys) >= self.order - 1


class BPlusTree:
    def __init__(self, order=8):
        self.order = order                          # Maximum number of children per internal node
        self.root = BPlusTreeNode(order)            # Start with an empty leaf node as root


    def search(self, key):
        """Search for a key in the B+ tree and return the associated value"""
        pass

    def _search(self, node, key):
        """Helper function to recursively search for a key starting from the given node"""
        pass


    def insert(self, key, value):
        """Insert a new key-value pair into the B+ tree"""
        pass

    def _insert_non_full(self, node, key, value):
        """Insert key-value into a node that is not full"""
        pass

    def _split_child(self, parent, index):
        """
        Split the child node at given index in the parent.
        This is triggered when the child is full.
        """
        pass


    def delete(self, key):
        """Delete a key from the B+ tree"""
        pass

    def _delete(self, node, key):
        """Recursive helper function for delete operation"""
        pass

    def _fill_child(self, node, index):
        """Ensure that the child node has enough keys to allow safe deletion"""
        pass

    def _borrow_from_prev(self, node, index):
        """Borrow a key from the left sibling"""
        pass

    def _borrow_from_next(self, node, index):
        """Borrow a key from the right sibling"""
        pass

    def _merge(self, node, index):
        """Merge two child nodes into one"""
        pass


    def update(self, key, new_value):
        """Update the value associated with a key"""
        pass


    def range_query(self, start_key, end_key):
        """
        Return all key-value pairs where start_key <= key <= end_key.
        Utilizes the linked list structure of leaf nodes.
        """
        pass

    def get_all(self):
        """Get all key-value pairs in the tree in sorted order"""
        pass

    def _get_all(self, node, result):
        """Recursive helper function to gather all key-value pairs"""
        pass


    def visualize_tree(self, filename=None):
        """
        Visualize the tree using graphviz.
        Optional filename can be provided to save the output.
        """
        pass

    def _add_nodes(self, dot, node):
        """Add graph nodes for visualization"""
        pass

    def _add_edges(self, dot, node):
        """Add graph edges for visualization"""
        pass
