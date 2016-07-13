from helpers import AINode, Edge, Dijkstra
import random
import time


class HexKI:
    """
    HexKI: Implements an AI opponent.
    """

    def __init__(self, m, n):
        """
        """
        self.depth = 2
        self.m = m  # number of rows
        self.n = n  # number of columns
        self.move_number = 1
        self.moves = None
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
        for node in self.nodes[0]:      # upper side
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

    def chooseOrder(self, firstmove):
        """
        """
        self.move_number += 1
        if self.n == 1:
            if firstmove(0,1):
                return 1
            else:
                return 2
        elif self.n == 2:
            if firstmove == (1,0):
                return 1
            else:
                return 2
        elif self.n == 3:
            if firstmove == (1,1):
                return 1
            else:
                return 2
        elif self.n == 5:
            if firstmove == (2,2):
                return 1
            else:
                return 2
        elif self.n % 2 == 0:
            if firstmove[0]+firstmove[1] == self.n-1:
                self.move_number +=1
                return 1  # wechsel?
            else:
                return 2 # kein wechsel?
        else:
            if firstmove[0] == self.n//2 and firstmove[1] == self.n//2:
                self.move_number += 1
                return 1 # wechsel?
            else:
                return 2 # kein wechsel?



    def calculateMove(self):
        self.eval_number = 0    # zum testen
        self.eval_times = []
        """
        """
        # Kann spaeter geloescht werden, ist nur zum print da
        show_board = [["#" for i in range(self.n)] for j in range(self.m)]
        # Minimum fuer a intialisieren
        mini = 1000
        mo = {}
        nodes = self.nodes

        # Nachfolgende ist zum Speichern der besten moves gedacht
        # Wenn man mit besseren moves anfängt, spart man sich angeblich zeit
        if self.n == 2:
            if self.move_number == 1:
                self.best_move = (1,0)
                self.move_number += 1
                return True
            else:
                self.moves = {}
                (self.moves.setdefault(1, [])).append((1, 0))
                (self.moves.setdefault(1, [])).append((1, 1))


        elif self.n == 3 and self.move_number == 1:
            self.moves = {}
            self.best_move = (1,1)
            self.move_number += 1
            self.depth -= 2
            return True

        elif self.n == 4:
            if self.move_number == 1:
                self.moves = {}
                (self.moves.setdefault(1, [])).append((3, 0))
                (self.moves.setdefault(1, [])).append((2, 1))
                (self.moves.setdefault(1, [])).append((1, 2))
                (self.moves.setdefault(1, [])).append((0, 3))
                self.move_number += 1
            else:
                self.moves = {}
                # noch in list comprehension
                for i in range(self.n):
                    for j in range(self.m ):
                        (self.moves.setdefault(1, [])).append((i, j))
        elif self.n == 5:
            if self.move_number == 1:
                self.move_number += 1
                self.best_move = (2,2)
                return True
            # abfragen ob eins schon belegt ist
            elif self.move_number == 2:
                self.move_number +=1
                self.moves = {}
                top_left,bottom_left,top_ri,bottom_ri = False,False,False,False
                if self.nodes[1][1].colour == 0 and self.nodes[1][2].colour == 0 and self.nodes[2][1].colour == 0:
                    top_left = True
                    (self.moves.setdefault(1, [])).append((1, 1))
                    (self.moves.setdefault(1, [])).append((1, 2))
                    (self.moves.setdefault(1, [])).append((2, 1))
                if self.nodes[3][1].colour == 0:
                    bottom_left = True
                    (self.moves.setdefault(1, [])).append((3, 1))
                if self.nodes[3][2].colour == 0 and self.nodes[3][3].colour == 0 and self.nodes[2][3].colour == 0:
                    bottom_ri = True
                    (self.moves.setdefault(1, [])).append((3, 2))
                    (self.moves.setdefault(1, [])).append((3, 3))
                    (self.moves.setdefault(1, [])).append((2, 3))
                if self.nodes[2][3].colour == 0:
                    (self.moves.setdefault(1, [])).append((2, 3))
                    top_ri = True

                if top_left == False:
                    self.best_move = (3,1)
                    return True
                elif bottom_left == False:
                    self.best_move = (1,1)
                    return True
                elif top_ri == False:
                    self.best_move = (3, 3)
                    return True
                else:
                    self.best_move = (1,3)
                    return True

            elif self.move_number == 3:
                self.move_number += 1

            elif self.move_number == 4:
                self.moves = {}
                # noch in list comprehension
                for i in range(self.n):
                    for j in range(self.m ):
                        (self.moves.setdefault(1, [])).append((i, j))

        else:
            # Beim ersten Zug werden nur das mittlere quadrat durchsucht
            # muss noch angepasst werden mit swap später
            if self.move_number == 1:
                self.moves = {}
                # noch in list comprehension
                for i in range(1, self.n - 1):
                    for j in range(1, self.m - 1):
                        (self.moves.setdefault(1, [])).append((i, j))

                self.move_number += 1
                print(self.moves)

            # Beim zweiten move werden alle fehlenden moves hinzugefuegt
            else:
                self.moves = {}
                for i in range(self.n):
                    for j in range(self.m):
                        if i not in range(1, self.n - 1) or j not in range(1, self.m - 1):
                            (self.moves.setdefault(1, [])).append((i, j))
                self.move_number += 1
                print(self.moves)

        # Sortiere Moves nach a wert, so dass er mit dem kleinsten a
        # beginnt (kleines a -> guter move)
        for val in sorted(self.moves):
            if val == 0:
                self.depth = 1
            elif val == 0 and len(self.moves[val]) > 1:
                moves = [self.moves[val]]
                val = 0  # as integer
                self.depth = 1
            else:
                moves = self.moves


            for i, j in moves[val]:
                if nodes[i][j].colour == 0:
                    # Zum probieren des jeweiligen moves muss die Farbe
                    # geändert werden.
                    # Daher tmporere nodes
                    nodes[i][j].change_colour(self.player_colour)
                    # theoretisch muesste hier min_value aufgerufen werden
                    a = self.min_value(nodes, float("inf"), -float("inf"), self.depth)
                    # wieder zurueck setzten, damit es beim naechsten move
                    # nicht stoert
                    nodes[i][j].change_colour(0)

                    # ?Frage? Warum wird potential auf 1 gesetzt?
                    #nodes[i][j].pot = 1

                    # Moves für die naechste Runde abspeichern
                    (mo.setdefault(a, [])).append((i, j))

                    show_board[i][j] = round(a, 3)
                    if a < mini:
                        mini = a
                        self.best_move = (i, j)
        self.moves = mo
        # Ausgabe der a Werte in Matrixform
        print(' \n'.join(
            '       '.join(str(a) for a in row) for row in show_board))

        if self.eval_times:
            self.eval_time_average = sum(self.eval_times
                                         ) / len(self.eval_times)
        return True

    def evaluate(self, nodes=None):
        t0 = time.clock()
        """
        Evaluates a board
        """
        if not nodes:
            nodes = self.nodes

        key = "".join(["".join(
            [str(n.colour) for n in row]) for row in nodes])

        value = self.board_scores.get(key)
        if value:
            # print(value)
            self.eval_times.append(time.clock() - t0)
            return value

        self.eval_number += 1
        # if not edges:
        #    edges = self.edges
        start_node = self.boundaries[self.player_colour][0]
        end_node = self.boundaries[self.player_colour][1]
        # Evaluate board with Dijkstra's algorithm.
        board_eval_1 = Dijkstra(nodes, start_node, end_node)
        value_1 = board_eval_1.value

        start_node = self.boundaries[self.opponent_colour][0]
        end_node = self.boundaries[self.opponent_colour][1]
        board_eval_2 = Dijkstra(nodes, start_node, end_node)
        value_2 = board_eval_2.value
        """
        if value_1 == 0:
            return 0 """

        # edge case division by zero
        self.eval_times.append(time.clock() - t0)
        if value_2 == 0:
            value = float("inf")
        else:
            value = value_1 / value_2

        self.board_scores[key] = value
        return value


    def setColours(self, player, opponent):
        """
        Sets the colours for the AI
        """
        self.player_colour = player
        self.opponent_colour = opponent

    def swapColours(self):
        self.player_colour, self.opponent_colour = \
        self.opponent_colour, self.player_colour

    def nextMove(self):
        """
        """
        best_i, best_j = self.best_move
        self.nodes[best_i][best_j].change_colour(
            self.player_colour)

        print("AI BOARD")
        print(self)
        return self.best_move

    def receiveMove(self, move, colour=None):
        """
        """
        i, j = move
        if not colour:
            colour = self.opponent_colour
        self.nodes[i][j].change_colour(colour)
        print("AI BOARD")
        print(self)

    def readBoard(self, board, current=True):
        """
        """
        for i, row in enumerate(board):
            for j, player_num in enumerate(row):
                self.board[i][j].colour = player_num

    def random_move(self):
        while True:
            i = random.randint(0, self.m - 1)
            j = random.randint(0, self.n - 1)

            if self.nodes[i][j].colour == 0:
                return (i, j)

    def max_value(self, nodes, a, b, depth):

        if (depth == 0):
            return self.evaluate(nodes)
        # moves = [(i, j) for i in range(self.n) for j in range(self.m)]
        # for move in moves:
        for val in sorted(self.moves):
            for i, j in self.moves[val]:
                if nodes[i][j].colour == 0:
                    nodes[i][j].change_colour(self.player_colour)

                    a = min(a, self.min_value(nodes, a, b, depth - 1))

                    nodes[i][j].change_colour(0)
                    # nodes[i][j].pot = 1

            # this ia a cutoff point
                if a <= b:
                    return a
        return a

    def min_value(self, nodes, a, b, depth):
        if (depth == 0):
            return self.evaluate(nodes)
        # moves = [(i, j) for i in range(self.n) for j in range(self.m)]
        # for move in moves:
        for val in sorted(self.moves):
            for i, j in self.moves[val]:
                if nodes[i][j].colour == 0:
                    nodes[i][j].change_colour(self.opponent_colour)

                    b = max(b, self.max_value(nodes, a, b, depth - 1))
                    nodes[i][j].change_colour(0)
                    # nodes[i][j].pot = 1

                # this is a cutoff point
                if b >= a:
                    return b
        return b

    # String representation to test logic without GUI dependency
    def __str__(self):
        colours = [[node.string_rep() for node in row] for row in self.nodes]
        output = ""
        for i, row in enumerate(colours):
            output += i * "   " + "   ".join(row) + "\n"
        return output


