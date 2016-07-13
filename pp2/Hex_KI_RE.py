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
        self.last_move = None

    def chooseOrder(self, firstmove):
        """
        """
        # Wechseln wenn von oben nach unten
        return 2 # nicht wechseln



    def calculateMove(self):
        """
        """
        i,j = self.last_move

        if j < self.n:
            self.best_move = self.oposit_move((i,j))

        return True

    def oposit_move(self,move):
        n =self.m
        m =self.m -1
        print(self.m)
        print(self.n)
        # liegt im linken teil
        if move[0] + move[1] < self.m:
            n = self.m
            m = self.m -1
            n1 = m - move[1] # n
            m1 = n - move[0] # m
            return (n1,m1)

        # liegt im rechtne teil

        elif move[0] + move[1] in range(self.m, self.m +self.m) and move[1]< self.m:
            n = self.m -1
            m = self.m
            m1 = n - move[0] # n
            n1 = m - move[1] # m
            return (n1,m1)

        # liegt am Rand
        else:
            i = 0
            while True:
                if self.board[i][self.n-1]==0:
                    return (i,self.n-1)
                else:
                    i+= 1

    def nextMove(self):
        """
        """

        self.board[self.best_move[0]][self.best_move[1]] = 1
        return self.best_move

    def receiveMove(self, move):
        """
        """
        self.last_move = move
        self.board[move[0]][move[1]] = 2

    def readBoard(self, board, current=True):
        """
        """
        self.board = board

    def __random_move(self):
        while True:
            i = random.randint(0, self.size[0])
            j = random.randint(0, self.size[1])

            if self.board[i][j].colour == 0:
                return (i, j)

A = HexKI_R(4,6)
            # n m
A.receiveMove((0,0))
A.calculateMove()
A.nextMove()


A.receiveMove((1,5))
A.calculateMove()
A.nextMove()

print(' \n'.join(' '.join(str(el) for el in row ) for row in A.board ))