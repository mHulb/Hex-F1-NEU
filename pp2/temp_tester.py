from Hex_KI import HexKI
from Hex import HexBoard
import time

m, n = 5, 5
testKI = HexKI(m, n)
board = HexBoard(m, n)
player_colour = 1
opponent_colour = 2
testKI.player_colour = player_colour
testKI.opponent_colour = opponent_colour

while not board.finished():
    random_move = testKI.random_move()
    print("Random move {}".format(random_move))
    testKI.receiveMove(random_move)
    board.receiveMove(random_move, opponent_colour)
    # print(testKI)
    print(board)
    t0 = time.clock()
    testKI.calculateMove()
    calculated_move = testKI.nextMove()
    print("Evaluations: {} boards".format(testKI.eval_number))
    print("Average time per evaluation: {} sec".format(testKI.eval_time_average))
    print("Calculation for move {1} took {0} seconds.".format(
        time.clock() - t0, calculated_move))
    board.receiveMove(calculated_move, player_colour)
    # print(testKI)
    print(board)

print("Player {} won the game!".format(board.winner()))

