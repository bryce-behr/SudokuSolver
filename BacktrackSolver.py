"""
    pseudo code from slides were used
    @author David Le Roux
"""

import sys
from GenerateSudoku import *
from BacktrackSolver import *
from Sudoku.Generator import *

def runBacktrack(difficultylevel, verbosity: int):
    # Get a sudoku problem of the appropriate difficulty level from the sudoku generator
    unsolved: Board = generateSudoku(difficultylevel)

    # get a solved sudoku problem from the backtrack method
    results = backtrack(unsolved, verbosity)
    solved = results[0]
    visitedNodes = results[1]
    openVals = results[2]

    totalNodesExplored = results[1]
    ratio = totalNodesExplored/openVals
    totalNodes_Opens = ratio

    if verbosity == 2:
        print("=====================================")
        print(str(totalNodesExplored) + " nodes were visited")
        print(str(openVals) + " open squares in the starting state")
        print(str(totalNodes_Opens) + " = (# nodes visited)/(# of open squares in starting state)")
        print("=====================================")

def backtrack(board: Board, verbosity: int):
    numOpenVals = len(board.get_unused_cells())
    nodesVisited = [0]

    print("The original unsolved sudoku puzzle is: \r\r\n{0}".format(board) + "\n")

    def solve():
        # Gets a list of 'unused celld' from th eboard, these cells all have a value of 0
        openCells = board.get_unused_cells()
        # If there are no more open cells then you have a solution
        if len(openCells) == 0:
            return True
        # Gets the next open cell to assign a value to
        cell = openCells[0]
        for number in range(1, 10):
            #look at every possible value for the cell but only assign it if it is valid
            if valid(board, cell, number):
                nodesVisited[0] += 1
                cell.value = number
                
                if verbosity == 3:
                    print("Changing value of (" + str(cell.row) + "," + str(cell.col) + ") to " + str(number) + ": \r\r\n{0}".format(board) + "\n")

                # Send the recursive functions return value back down the recursive calls
                if solve():
                    return True
                # Backtrack if the previous value did not return True
                cell.value = 0

                if verbosity == 3:
                    print("Backtracking and changing value of (" + str(cell.row) + "," + str(cell.col) + ") back to " + str(0) + ": \r\r\n{0}".format(board) + "\n")
        return False
    solve() 

    print("The solved sudoku puzzule is: \r\r\n{0}".format(board) + "\n")

    # returns the solved board, the number of nodes visited, and the number of originally open squares
    return [board, nodesVisited[0], numOpenVals]

def valid(board: Board, cell: Cell, number: int):
    rowValues = board.rows[cell.row]
    for value in rowValues:
        if value.value == number:
            return False
            
    colValues = board.columns[cell.col]
    for value in colValues:
        if value.value == number:
            return False
            
    boxValues = board.boxes[cell.box]
    for value in boxValues:
        if value.value == number:
            return False
            
    return True