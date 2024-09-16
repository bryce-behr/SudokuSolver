import sys
from Sudoku.Generator import *

def generateSudoku(difficultyLevel):

    difficulties = {
        'easy': (35, 0),
        'medium': (81, 5),
        'hard': (81, 10),
        'extreme': (81, 15)
    }

    difficulty = difficulties[difficultyLevel]

    gen = Generator('base.txt')

    gen.randomize(100)

    initial = gen.board.copy()

    gen.reduce_via_logical(difficulty[0])

    if difficulty[1] != 0:
        gen.reduce_via_random(difficulty[1])

    final = gen.board.copy()

    # print("The initial board before removals was: \r\n\r\n{0}".format(initial))

    # print("The generated board after removals was: \r\n\r\n{0}".format(final))

    return(final)