"""
Helpers file containing the classes Node and Subgraph
"""


class Node:
    """
    Class to store a node.
    """

    def __init__(self, i, j):
        self.colour = None
        self.neighbours = []
        self.i = i
        self.j = j

    def __str__(self):
        return self.string_rep()

    def __repr__(self):
        return "Node ({}, {}) ".format(self.i, self.j)

    def string_rep(self):
        # string_rep for testing without GUI
        if not self.colour:
            return "[ ]"
        elif self.colour == 1:  # red
            return "[X]"
        elif self.colour == 2:  # blue
            return "[O]"


class Subgraph:
    """
    Class to store a subgraph that a player has built by placing their pieces.
    Can add nodes to the subgraph, add another subgraph to the subgraph and
    check if that subgraph satisfies the win condition.
    """

    def __init__(self, first_node):
        self.nodes = {first_node}  # set for fast membership testing
        self.colour = first_node.colour

    def connects_both_sides(self, n, m):
        """
        Checks if a subraph connects the sides of the board where
        n, m are the dimensions of the current board.
        If it does, True is returned.
        """
        if self.colour == 1:  # "red"
            top_exists, bottom_exists = False, False
            for node in self.nodes:
                if node.i == 0:         # node is part of top row
                    top_exists = True
                elif node.i == n - 1:   # node is part of bottom row
                    bottom_exists = True
            return top_exists and bottom_exists

        else:  # if colour is "blue"
            left_exists, right_exists = False, False
            for node in self.nodes:
                if node.j == 0:         # node is part of leftmost column
                    left_exists = True
                elif node.j == m - 1:   # node is part of rightmost column
                    right_exists = True
            return left_exists and right_exists

    def __contains__(self, other):
        return other in self.nodes

    def __iter__(self):
        return self.nodes.__iter__()  # iterating over nodes

    def add(self, other_node):
        self.nodes.add(other_node)

    def merge_with(self, other_graph):
        for node in other_graph:
            self.add(node)

    def __repr__(self):
        return "{" + ", ".join(
            ["({}, {})".format(n.i, n.j) for n in self.nodes]) + "}"
