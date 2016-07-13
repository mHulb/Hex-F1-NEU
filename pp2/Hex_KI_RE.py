from helpers import AINode, Edge, Dijkstra
import random

class HexKI_R(object):
    """
    HexKI: Implements an AI opponent.
    """

    def __init__(self, n, m):
        """
        """
        self.board = [[0 for j in range(m)] for i in range(n)]
        self.n = m
        self.m = n
        self.best_move = None
        self.move_number = 0
        self.last_move = (0,0)

        self.first_player = False
        self.nodes = [[AINode(i, j) for j in range(m)] for i in range(n)]
        # boundary nodes have no indices, but a predefined colour (1 or 2)
        self.boundaries = {1: [AINode(None, None, 1), AINode(None, None, 1)],
                           2: [AINode(None, None, 2), AINode(None, None, 2)]}
        for _, nodes in self.boundaries.items():
            for node in nodes:
                node.update_resistances()

        self.__initialize_nodes(m, n)
        self.edges = self.__make_edges()
        self.best_move = None
        self.player_colour = None
        self.opponent_colour = None

        # Zum zeitesten
        self.eval_number = 0
        self.eval_times = []
        self.board_scores = {}
        self.eval_time_average = 0

    def chooseOrder(self, firstmove):
        """
        """
        # Wechseln wenn von oben nach unten
        return 2 # nicht wechseln



    def calculateMove(self):
        """
        """
        self.best_move = self.__random_move()
        # if self.move_number == 0:
        #     self.first_player = True
        #
        # if self.first_player:
        #     self.best_move = self.__random_move()
        #     return True
        # else:

        i,j = self.last_move

        if j < self.n:
            self.best_move = self.oposit_move((i,j))

        return True

    def oposit_move(self,move):
        n =self.m
        m =self.m -1
        #print(self.m)
        #print(self.n)
        # liegt im linken teil
        if move[0] + move[1] < self.m:
            n = self.m
            m = self.m -1
            n1 = m - move[1] # n
            m1 = n - move[0] # m
            return (n1,m1)

        # liegt im rechtne teil

        elif move[0] + move[1] in range(self.m, self.m +self.m) and move[1]<= self.m:
            n = self.m -1
            m = self.m
            m1 = n - move[0] # n
            n1 = m - move[1] # m
            return (n1,m1)

        # liegt am Rand
        else:
            return self.random_move_in_outside()

    def random_move_in_outside(self):
        mo = self.last_move
        diff = self.n - self.m

        while True:
            i = random.randint(0, diff)
            j = random.randint(0, self.m - 1)
            if self.board[j][self.m -1 + i] == 0:
                return (j,self.m -1 + i)


    def nextMove(self):
        """
        """

        self.board[self.best_move[0]][self.best_move[1]] = 1
        best_i, best_j = self.best_move
        self.nodes[best_i][best_j].change_colour(
            self.player_colour)

        self.move_number += 1
        return self.best_move


    def receiveMove(self, move, current_player = None):
        """
        """
        self.board[move[0]][move[1]] = 2
        self.last_move = move
        i, j = move
        self.nodes[i][j].change_colour(self.opponent_colour)
        self.move_number += 1

    def readBoard(self, board, current=True):
        """
        """
        for i, row in enumerate(board):
            for j, player_num in enumerate(row):
                self.board[i][j].colour = player_num

    def __random_move(self):
        while True:
            i = random.randint(0, self.m - 1)
            j = random.randint(0, self.n - 1)

            if self.nodes[i][j].colour == 0:
                return (i, j)

    def setColours(self, player, opponent):
        """
        Sets the colours for the AI
        """
        self.player_colour = player
        self.opponent_colour = opponent

    def swapColours(self):
        self.player_colour, self.opponent_colour = \
        self.opponent_colour, self.player_colour

    def __make_edges(self):
        edges = []
        for row in self.nodes:
            for node in row:
                for neighbour in node.neighbours:
                    # resistance default value is 2 for both sides
                    new_edge = Edge(node, neighbour)
                    if new_edge not in edges:
                        edges.append(new_edge)

                        # add edge to both nodes
                        node.adjacent_edges.append(new_edge)
                        neighbour.adjacent_edges.append(new_edge)

        for edge in edges:
            edge.update_resistances()
        return edges


    def __initialize_nodes(self, m, n):
        # initializing the basic board nodes
        for i, row in enumerate(self.nodes):
            for j, node in enumerate(row):
                if i > 0:
                    node.neighbours.append(self.nodes[i - 1][j])
                if j > 0:
                    node.neighbours.append(self.nodes[i][j - 1])
                if i < n - 1:
                    node.neighbours.append(self.nodes[i + 1][j])
                if j < m - 1:
                    node.neighbours.append(self.nodes[i][j + 1])
                if i < n - 1 and j > 0:
                    node.neighbours.append(self.nodes[i + 1][j - 1])
                if i > 0 and j < m - 1:
                    node.neighbours.append(self.nodes[i - 1][j + 1])

        # initializing the boundary nodes
        upper_bound = self.boundaries[1][0]
        lower_bound = self.boundaries[1][1]
        for node in self.nodes[0]:  # upper side
            node.neighbours.append(upper_bound)
            upper_bound.neighbours.append(node)
        for node in self.nodes[n - 1]:  # lower side
            node.neighbours.append(lower_bound)
            lower_bound.neighbours.append(node)

        left_bound = self.boundaries[2][0]
        right_bound = self.boundaries[2][1]
        for row in self.nodes:
            # leftmost side
            row[0].neighbours.append(left_bound)
            left_bound.neighbours.append(row[0])
            # rightmost side
            row[self.m - 1].neighbours.append(right_bound)
            right_bound.neighbours.append(row[self.m - 1])


