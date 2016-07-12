from tkinter import *
from tkinter import messagebox
import math
import random
from helpers import Node
from time import sleep


"""
Hex Game
"""

COLOR_THEMES = {"standard":
                {"color_1": "#f42525",
                 "color_2": "#2a67cb",
                 "bg": "#eeeeee",
                 "tile": "#dca256",
                 "tile_hover": "#e5b980",
                 "tile_outline": "#654a27"},
                "b/w":
                {"color_1": "#282828",
                 "color_2": "white",
                 "bg": "#676767",
                 "tile": "#dca256",
                 "tile_hover": "#e5b980",
                 "tile_outline": "#654a27"},
                "dark":
                {"color_1": "#8eaee3",
                 "color_2": "#f8c083",
                 "bg": "#676767",
                 "tile": "#555555",
                 "tile_hover": "#666666",
                 "tile_outline": "#111111"},
                }


class HexGui(object):
    """
    HexGui: Creates the GUI for the Hex Game.
    """

    def __init__(self, m, n, game, color_theme="standard"):
        theme = COLOR_THEMES[color_theme]
        # set colors from theme
        self.red = theme["color_1"]
        self.blue = theme["color_2"]
        self.bg = theme["bg"]
        self.tile = theme["tile"]
        self.tile_outline = theme["tile_outline"]
        self.tile_hover = theme["tile_hover"]
        self.game = game
        self.last_field = None
        #self.round = 0
        self.size = (m, n)
        # Saves for every Hexagon the points
        self.point_coordinates = [[[0 for i in range(12)]
                                   for j in range(n)] for k in range(m)]
        # Array to save if a field is already colored or not
        self.field_array = [[0 for i in range(n)]for j in range(m)]

        # Creates GUI
        self.master = Tk()
        self.master.configure(background=self.bg)
        self.player = game.currentPlayer()
        # set color and name from player label
        if self.player == 1:
            self.lab = Label(self.master,
                             text="Spieler 2 ist am Zug",
                             fg=self.tile,
                             bg=self.red,)
        else:
            self.lab = Label(self.master,
                             text="Spieler 1 ist am Zug",
                             fg=self.tile,
                             bg=self.blue,)
        self.lab.pack()
        # creates board with hexagons
        self.__create_board()
        # Colours outline
        self.__print_outline()
        # left klick to color the field in the color of the player
        self.w.bind("<Button-1>", lambda e: self.__find_move(e))
        # mouse move to color the current field
        self.w.bind('<Motion>', lambda e: self.__color_field_enter(e))

    def __color_field_enter(self, event):
        """
        Colours the Hexagon field where the mouse is in self.tile_hover color
        changes the color of the last Hexagon back to self.tile color
        """
        # go through all Hexagon fields
        for j in range(self.size[0]):
            for i in range(self.size[1]):
                poly = [[self.point_coordinates[j][i][k],
                         self.point_coordinates[j][i][k + 1]]
                        for k in range(0, 11, 2)]

                # if mouse position is in the Hexagon field:
                if self.__contains_point(event.x, event.y, poly) >= 0:
                    # changes the field color back to standard
                    if self.last_field:
                        if (not j == self.last_field[0] or
                                not i == self.last_field[1]):
                            point = list(self.point_coordinates[
                                self.last_field[0]][self.last_field[1]])
                            self.w.create_polygon(point,
                                                  outline=self.tile_outline,
                                                  fill=self.tile,
                                                  width=3)

                    # changes field where the mouse is over to tile_hover color
                    if self.field_array[j][i] != 1:
                        self.w.create_polygon(
                            list(self.point_coordinates[j][i]),
                            outline=self.tile_outline,
                            fill=self.tile_hover,
                            width=3)
                        self.last_field = (j, i)
                    return

    def __contains_point(self, x, y, P):
        """
        Uses point-in-polygen test from Jordan to test if the given point
        is in the given polygen
        """
        Q = [x, y]
        t = -1
        P.append(P[0])

        for i in range(5 - 1):
            t = t * self.__kreuzProdTest(Q, P[i], P[i + 1])
        return t

    def __kreuzProdTest(self, A, B, C):
        # first part it looks if A is one the line BC
        # if A is on the same y-line
        if A[1] == B[1] == C[1]:
            # and between the points
            if B[0] <= A[0] <= C[0] or C[0] <= A[0] <= B[0]:
                return 0
            else:
                return 1
        # C should be the higher y point
        if B[1] > C[1]:
            B, C = C, B
        # A is on B
        if A[1] == B[1] and A[0] == B[0]:
            return 0

        if A[1] <= B[1] or A[1] > C[1]:
            return 1
        d = ((B[0] - A[0]) * (C[1] - A[1])) - ((B[1] - A[1]) * (C[0] - A[0]))
        if d > 0:
            return -1
        elif d < 0:
            return 1
        else:
            return 0

    def __create_board(self):
        """
        Creates a Canvas widget where Hexagon fields are marked on it
        """
        m = self.size[0]
        n = self.size[1]
        edge_length = 24
        # calculates the size of the Hexagon
        y_top, x_right = self.__Hex_size(edge_length)
        canvas_width = x_right * n + x_right * m / 2 + 50
        canvas_height = y_top * m + 100

        self.w = Canvas(self.master, width=canvas_width, height=canvas_height)
        self.w.configure(background=self.bg)
        self.w.pack()
        # creates Hexagon Grid
        for j in range(m):
            for i in range(n):
                x = 40 + x_right * i + x_right / 2 * j
                y = 50 + y_top * j
                k = 0
                for angle in range(0, 360, 60):
                    y += math.cos(math.radians(angle)) * edge_length
                    x += math.sin(math.radians(angle)) * edge_length
                    self.point_coordinates[j][i][k] = x
                    self.point_coordinates[j][i][k + 1] = y
                    k += 2
                # draws Hexagon to the canvas widget
                self.w.create_polygon(list(
                    self.point_coordinates[j][i]),
                    outline=self.tile_outline, fill=self.tile, width=3)

    def __print_outline(self):
        """
        Colours the top und botten outline side of the Hexagon field in red
        and the left and right outline side in blue
        """
        left = self.blue
        top = self.red
        m = self.size[0] - 1
        n = self.size[1] - 1
        line_width = 3

        for i in range(self.size[1]):
            # top edge
            a = self.point_coordinates[0][i][11] - 3
            b = self.point_coordinates[0][i][10]
            c = self.point_coordinates[0][i][9] - 3
            d = self.point_coordinates[0][i][8]
            self.w.create_line(d, c, b, a, fill=top, width=line_width)
            if i != self.size[0] - 1:
                a = self.point_coordinates[0][i][9] - 3
                b = self.point_coordinates[0][i][8]
                c = self.point_coordinates[0][i][7] - 3
                d = self.point_coordinates[0][i][6]
                self.w.create_line(d, c, b, a, fill=top, width=line_width)

            # bottom edge
            a = self.point_coordinates[m][i][3] + 3
            b = self.point_coordinates[m][i][2]
            c = self.point_coordinates[m][i][1] + 3
            d = self.point_coordinates[m][i][0]
            self.w.create_line(d, c, b, a, fill=top, width=line_width)
            a = self.point_coordinates[m][i][5] + 3
            b = self.point_coordinates[m][i][4]
            c = self.point_coordinates[m][i][3] + 3
            d = self.point_coordinates[m][i][2]
            self.w.create_line(d, c, b, a, fill=top, width=line_width)

        for i in range(self.size[0]):
            # left edge
            a = self.point_coordinates[i][0][11]
            b = self.point_coordinates[i][0][10] - 3
            c = self.point_coordinates[i][0][1]
            d = self.point_coordinates[i][0][0] - 3
            self.w.create_line(d, c, b, a, fill=left, width=line_width)
            if i != self.size[0] - 1:
                a = self.point_coordinates[i][0][1]
                b = self.point_coordinates[i][0][0] - 3
                c = self.point_coordinates[i][0][3]
                d = self.point_coordinates[i][0][2] - 3
                self.w.create_line(d, c, b, a, fill=left, width=line_width)

            # right edge
            a = self.point_coordinates[i][n][9]
            b = self.point_coordinates[i][n][8] + 3
            c = self.point_coordinates[i][n][7]
            d = self.point_coordinates[i][n][6] + 3
            self.w.create_line(d, c, b, a, fill=left, width=line_width)
            a = self.point_coordinates[i][n][7]
            b = self.point_coordinates[i][n][6] + 3
            c = self.point_coordinates[i][n][5]
            d = self.point_coordinates[i][n][4] + 3
            self.w.create_line(d, c, b, a, fill=left, width=line_width)

    def __Hex_size(self, edge_length):
        """
        Calculates the Hexagon size in order to create the board
        without gaps.
        """
        xs, ys = [], []
        y, x = 0, 0
        for angle in range(0, 360, 60):
            y += math.cos(math.radians(angle)) * edge_length
            ys.append(y)
            x += math.sin(math.radians(angle)) * edge_length
            xs.append(x)
        y_top = (max(ys))
        x_right = (max(xs))
        return y_top, x_right

    def receiveMove(self, move):
        """
        Updates the Player label with the current player. Colours the Hexagon
        field in the color of the current player if the field is not already
        colored. If its the first move, Player 2 is asked if he/she wants
        to play with the first move.
        """
        # color sets for the field
        if self.game.currentPlayer() == 1:
            player_color = self.red
            self.lab.configure(text="Spieler 1 ist am Zug",
                               fg=self.tile,
                               bg=self.blue, )
        else:  # if player == 2
            player_color = self.blue
            self.lab.configure(text="Spieler 2 ist am Zug",
                               fg=self.tile,
                               bg=self.red, )
        # colors the field which is clicked/selected
        j, i = move[0], move[1]
        if self.field_array[j][i] == 0:
            self.game.round += 1
            self.field_array[j][i] = 1
            latest_poly = self.w.create_polygon(
                list(self.point_coordinates[j][i]),
                outline=self.tile_outline, fill=player_color, width=3)
            self.last_field = None

        # Swap rule at first turn
        if self.game.round == 1 and self.setFirst() == 1:
            self.game.changePlayer()
            self.field_array[j][i] = 0
            self.w.delete(latest_poly)
            self.receiveMove(move)
            self.game.round = 1

    def setFirst(self):
        """
        Ask Player 2 if he/she wants to take the first move
        """
        if messagebox.askyesno(
                'Verify', 'Möchte Spieler {} übernehmen?'.format(self.player)):
            return 1
        else:
            return 2

    def __find_move(self, event):
        """
        Finds the Hexagon where is clicked on
        """
        for j in range(self.size[0]):
            for i in range(self.size[1]):

                poly = [[self.point_coordinates[j][i][k],
                         self.point_coordinates[j][i][k + 1]]
                        for k in range(0, 11, 2)]

                # if mouse position is in the Hexagon field:
                if self.__contains_point(event.x, event.y, poly) >= 0:
                    if not self.field_array[j][i]:
                        self.game.makeMove((j, i))
                    return

    def finish(self, player):
        """
        If the Game is finished, the player label is updated with the winner
        """
        if player == 1:
            self.lab.configure(text="Spieler 1 hat gewonnen",
                               fg=self.tile,
                               bg=self.red, )
        else:  # if player == 2
            self.lab.configure(text="Spieler 2 hat gewonnen",
                               fg=self.tile,
                               bg=self.blue, )


class HexBoard:
    """
    HexBoard: ...
    """

    def __init__(self, n, m):
        self.nodes = [[Node(i, j) for j in range(m)] for i in range(n)]
        self.n = n
        self.m = m
        self.__initialize_nodes(m, n)
        self.winning_player = None
        self.is_finished = False
        self.last_move = None

    def finished(self):
        return self.is_finished

    def winner(self):
        return self.winning_player

    def receiveMove(self, move, player):
        """
        Receives a move from the Game class.
        """
        i, j = move[0], move[1]
        print("Player {} - move on board: ({}, {})".format(
            player, move[0] + 1, move[1] + 1))
        clicked_node = self.nodes[i][j]
        clicked_node.colour = player  # change colour of node to player colour
        self.last_move = move  # store the move

        # Check if move wins the game
        if self.__winning_move(clicked_node):
            self.is_finished = True
            self.winning_player = player

    def __winning_move(self, start_node):
        """
        Checks if the last move won the game.
        First, builds a subgraph connected to the recently clicked
        node by breadth first search, then checks if that subgraph
        satisfies the victory condition.
        """
        visited, stack = set(), [start_node]
        colour = start_node.colour

        while stack:
            node = stack.pop()
            if node not in visited:
                visited.add(node)
                stack.extend([n for n in node.neighbours
                              if n not in visited and n.colour == colour])

        return self.__connects_both_sides(visited, colour)

    def __connects_both_sides(self, subgraph, colour):
        """
        Checks if a subraph connects the sides of the board.
        If it does, True is returned.
        """
        if colour == 1:  # "red"
            top_exists, bottom_exists = False, False
            for node in subgraph:
                if node.i == 0:              # node is part of top row
                    top_exists = True
                elif node.i == self.n - 1:   # node is part of bottom row
                    bottom_exists = True
            return top_exists and bottom_exists

        else:  # if colour is "blue"
            left_exists, right_exists = False, False
            for node in subgraph:
                if node.j == 0:              # node is part of leftmost column
                    left_exists = True
                elif node.j == self.m - 1:   # node is part of rightmost column
                    right_exists = True
            return left_exists and right_exists

    def getLastMove(self):
        return self.last_move

    # String representation to test logic without GUI dependency
    def __str__(self):
        colours = [[node.string_rep() for node in row] for row in self.nodes]
        output = ""
        for i, row in enumerate(colours):
            output += i * "   " + "   ".join(row) + "\n"
        return output

    def __initialize_nodes(self, m, n):
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


class Game():

    def __init__(self, m, n, mode, color_theme):
        # bei human soll ein Spielfeld erstellt werden
        # und eine GUI gestartet
        self.board = HexBoard(m, n)     # Spielbrett
        self.cur_player = self.chooseFirst()
        self.round = 0
        self.gui = HexGui(m, n, self, color_theme)   # GUI
        self.mode = mode

        if mode == "human":
            self.gui.master.mainloop()
        # Bei inter/ki soll noch nichts passieren
        if mode == "test":
            self.cur_player = 1

        else:
            pass

        self.round = 0

    # Spieler durch 1 und 2 festgelegt
    def changePlayer(self):
        if self.cur_player == 1:
            self.cur_player = 2
        else:
            self.cur_player = 1

    def chooseFirst(self):
        # wähle zufällig ersten Spieler aus
        s = [1, 2]
        return random.choice(s)

    def currentPlayer(self):
        return self.cur_player

    # Spielfeld wird aktualisiert
    # nach Spielzug wird Spieler am Zug geändert
    # sets next move, increments round number and switches current player
    def makeMove(self, move):

        if not self.board.finished():
            self.gui.receiveMove(move)
            self.board.receiveMove(move, self.cur_player)
            self.round += 1         # nächster ist neuer Zug.
            self.changePlayer()     # anderer Spieler am Zug
            self.gui.master.update()  # used to update gui in test mode
            print(self.board)

            if self.board.finished():
                print("Player {} has won!".format(self.board.winner()))
                self.gui.finish(self.board.winner())
                self.gui.master.update()

                if self.mode == "test":
                    # In test mode, endscreen remains open until closed
                    self.gui.master.mainloop()

#A = Game(10,10,"human","dark")

if __name__ == "__main__":

    mode = input(
        'Please enter game mode (human, test): ').strip().lower()
    theme = input(
        "Select color scheme (standard, dark, b/w): ").strip().lower()

    # Mode for human vs. human
    if mode == "human":
        n,m = 0,0
        while n < 2 or m < 2:
            dim = input("Please enter dimensions (min 2) (n m): ")
            n, m = int(dim.split(" ")[0]), int(dim.split(" ")[1])
            if n < 2 or m < 2:
                print("Die Dimensionen sind zu klein")
        hex_game = Game(n, m, "human", theme)

    # Additional test mode to have a predefined game played automatically
    elif mode == "test":
        name = input("Name of testfile: ")
        file = open(name.strip(), "r")

        for game in file:
            game = game.strip()

            dim, moves = game.split("; ")[0], game.split("; ")[1].split(", ")
            moves = list(map(lambda st: (
                int(st.split(" ")[0]) - 1, int(st.split(" ")[1]) - 1), moves))

            n, m = int(dim.split(" ")[0]), int(dim.split(" ")[1])
            hex_game = Game(n, m, "test", theme)
            print("Starting game...")

            for move in moves:
                hex_game.makeMove(move)
                sleep(0.7)

    else:
        print("Gamemode {} is not available.".format(mode))

