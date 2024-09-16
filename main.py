"""
@author David Le Roux
"""

import sys
from GenerateSudoku import *
from BacktrackSolver import *
from sudoku_generator import runExactCover

try:
    algo = sys.argv[1]
    difficulty = sys.argv[2]
    verbosity = int(sys.argv[3])

    if (algo == "backtrack"):
        runBacktrack(difficulty, verbosity)
    elif (algo == "exactcover"):
        runExactCover(difficulty, verbosity)
    else:
        print("Incorrect arguments, usage example: py main.py algorithm difficulty verbosity")
        print("algorithm usages: backtrack, exactcover")
        print("difficulty usages: easy, medium, hard, extreme")
        print("verbosity usages: 1, 2, 3")
except:
    print("Incorrect arguments, usage example: py main.py algorithm difficulty verbosity")
    print("algorithm usages: backtrack, exactcover")
    print("difficulty usages: easy, medium, hard, extreme")
    print("verbosity usages: 1, 2, 3")



