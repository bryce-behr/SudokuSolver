# this is the main Bryce used to test exact cover

# !/usr/bin/python
import sys
from Sudoku.Generator import *
from ExactCoverSolver import DLX


def matrix_to_board(lst: list[list[int]]):
    b = Board()
    for row in range(0, len(lst)):
        for col in range(0, len(lst[0])):
            b.rows[row][col].value = lst[row][col]
    return b

def genBoard(diff: str) -> Board:
    # setting difficulties and their cutoffs for each solve method
    difficulties = {
        'easy': (35, 0), 
        'medium': (81, 5), 
        'hard': (81, 10), 
        'extreme': (81, 15)
    }

    # getting desired difficulty from command line
    difficulty = difficulties[diff]

    # constructing generator object from puzzle file (space delimited columns, line delimited rows)
    gen = Generator("base.txt")

    # applying 100 random transformations to puzzle
    gen.randomize(100)

    # getting a copy before slots are removed
    initial = gen.board.copy()

    # applying logical reduction with corresponding difficulty cutoff
    gen.reduce_via_logical(difficulty[0])

    # catching zero case
    if difficulty[1] != 0:
        # applying random reduction with corresponding difficulty cutoff
        gen.reduce_via_random(difficulty[1])


    # getting copy after reductions are completed
    return gen.board.copy()


# # printing out complete board (solution)
# # print("The initial board before removals was: \r\n\r\n{0}\n\n".format(initial))

# # printing out board after reduction
# print("Unsolved board: \r\n\r{0}\n\n".format(final))

# sol = matrix_to_board(DLX(final.get_list()).search())

# print("Solution: \r\n\r\n{0}\n\n".format(sol))

def runExactCover(difficulty, v: int=0):
    v = int(v)

    avergeNodesAssigned = 0
    averageFraction = 0

    for i in range(7):
        board = genBoard(difficulty)
        openCells=len(board.get_unused_cells())
        if v == 1 or v == 2 or v == 3: 
            print("Board " + str(i+1) + " unsolved: " + "\r\r\n{0}\n".format(board))

        if v == 3 : searchBoard = DLX(board.get_list(), 3)
        else: searchBoard = DLX(board.get_list())
        sol = matrix_to_board(searchBoard.search())
        print("Board " + str(i+1) + " solved: " + "\r\r\n{0}".format(sol))

        nodesAssigned = searchBoard.getNodesExplored()
        avergeNodesAssigned += nodesAssigned
        averageFraction += (nodesAssigned/openCells)
        if v == 2:
            print("Nodes visited: " + str(nodesAssigned))
            print("Nodes visited / open cells = " + str())

        print("\n\n")

    if v == 2:
        print("Average nodes visited: " + str(avergeNodesAssigned/7))
        print("Average fraction: " + str(averageFraction/7))
    
if __name__ == '__main__':
# setting difficulties and their cutoffs for each solve method
    if len(sys.argv) == 3:
        runExactCover(sys.argv[1], sys.argv[2])
    else:
        runExactCover(sys.argv[1])