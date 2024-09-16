"""
https://www.geeksforgeeks.org/introduction-to-exact-cover-problem-and-algorithm-x/?ref=ml_lbp
https://www.geeksforgeeks.org/implementation-of-exact-cover-problem-and-algorithm-x-using-dlx/?ref=ml_lbp
^^ pseudocode used from this page ^^

https://en.wikipedia.org/wiki/Exact_cover#Sudoku
https://en.wikipedia.org/wiki/Knuth%27s_Algorithm_X
https://en.wikipedia.org/wiki/Dancing_Links

@author Bryce Behr
"""


from __future__ import annotations
from typing import Generator

from Sudoku.Board import Board

# standard node class which can link 4 directions and can carry a counter
class Node:
    def __init__(self, row: int, col: int, up: Node=None, down: Node=None, left: Node=None, right: Node=None, count: int=1):
        self.row = row
        self.col = col
        self.up = up or self
        self.down = down or self
        self.left = left or self
        self.right = right or self
        self.count = count
    
    # this def yields each of the node above a node
    def loopUp(self, excl: bool=True) -> Generator[Node,None,None]:
        itr = self
        if not excl: yield itr

        # loop until header is reached
        while itr.up != self:
            itr = itr.up
            yield itr

    # this def yields each of the node below a node
    def loopDown(self, excl: bool=True) -> Generator[Node,None,None]:
        itr = self
        if not excl: yield itr

        # loop until header is reached
        while itr.down != self:
            itr = itr.down
            yield itr

    # this def yields each of the nodes to the left of a node
    def loopLeft(self, excl: bool=True) -> Generator[Node,None,None]:
        itr = self
        if not excl: yield itr

        # loop until header is reached
        while itr.left != self:
            itr = itr.left
            yield itr

    # this def yields each of the nodes to the right of a node
    def loopRight(self, excl: bool=True) -> Generator[Node,None,None]:
        itr = self
        if not excl: yield itr

        # loop until header is reached
        while itr.right != self:
            itr = itr.right
            yield itr


# here we define the four sections that correspond to our four constraints in the matrix
# these constraints define the column in which the nodes will go

# this constraint is for the section that checks for exactly one number in each cell
def valConstraint(row: int) -> int: return int(row/9)

# this constraint corresponds to the section that checks that there's a 1-9 in each row
def rowConstraint(row:int) -> int: return 81 + 9*(int(row/81)) + row % 9

# this constraint corresponds to the section that checks that there's a 1-9 in each column
def colConstraint(row:int) -> int: return 2*81 + (row % 81)

# this constraint corresponds to the section that checks that there's a 1-9 in each box
def boxConstraint(row:int) -> int: return int(3*81 + (int(row/(3*81)))*(9*3) + ((int(row/(3*9))) % 3)*9 + (row % 9))

constraint_list = [valConstraint, rowConstraint, colConstraint, boxConstraint]
    

# this is the primary class for the dancing links matrix
class DLX:
    # constructor
    def __init__(self, board: list[int], v: int=0):
        self.numRows = 9**3
        self.numCols = 9**2 * 4

        # create a frame for the matrix
        self.root = Node(-1, -1)
        self.colHeader: list[Node] = [Node(-1, i) for i in range(self.numCols)]
        self.rowHeader: list[Node] = [Node(i, -1) for i in range(self.numRows)]

        self.verbosity = v
        self.nodesExplored: int = 0
        self.solved: bool = False

        # link the nodes in the row header (end nodes link to themselves rather than None)
        for i, node in enumerate(self.rowHeader):
            node.right = node
            node.left = node
            node.down = self.rowHeader[i+1] if i < self.numRows-1 else self.root
            node.up = self.rowHeader[i-1] if i > 0 else self.root

        # link the nodes in the column header (end nodes link to themselves rather than None)
        for i, node in enumerate(self.colHeader):
            node.up = node
            node.down = node
            node.right = self.colHeader[i+1] if i < self.numCols-1 else self.root
            node.left = self.colHeader[i-1] if i > 0 else self.root

        # link column and row readers to root (the corner node on the frame)
        self.root.right = self.colHeader[0]
        self.root.left  = self.colHeader[-1]
        self.root.down  = self.rowHeader[0]
        self.root.up    = self.rowHeader[-1]
                
        # fill in the DLX matrix given a certain sudoku board
        for i, cell in enumerate(board):
            # if the cell is empty add a row for all potential entries
            if cell == 0:
                for j in range(9):
                    # this formula is key for extracting necessary info
                    row = i*9+j
                    for constraint in constraint_list:
                        self.addNode(row, constraint(row))
            # node is full so just add one row defining the proper constraints
            else:
                row = i*9+cell-1
                for constraint in constraint_list:
                        self.addNode(row, constraint(row))

    def getNodesExplored(self):
        return self.nodesExplored

    # this def adds a node to the proper colHeader and rowHeader list and
    # and links it to its neighbors
    def addNode(self, row: int, col: int):
        newNode: Node = Node(row, col)
        
        # link row to left and right neighbors / put it in the row
        node = self.root
        for node in self.rowHeader[row].loopRight(excl=False):
            if node.right.col == -1 or node.right.col > col: break
        if node.col == col: return
        newNode.right = node.right
        newNode.left = node
        newNode.right.left = newNode
        node.right = newNode

        # link row to top and bottom neighbors / put it in the column
        for node in self.colHeader[col].loopDown(excl=False):
            if node.down.row == -1 or node.down.row > row: break
        newNode.down = node.down
        newNode.up = node
        newNode.down.up = newNode
        node.down = newNode
        self.colHeader[col].count += 1

    # cover this node and corresponding rows and columns from DLX
    # this effectively unlinks the node and hides it but it is recoverable
    def cover(self, node: Node) -> None:
        # get the col header node
        if node.col == -1: col = self.root
        else: col = self.colHeader[node.col]

        # unlink the col header horizontally
        col.right.left = col.left
        col.left.right = col.right

        # unlink all nodes in any row in this columns
        # get each node in column
        for colLoop in col.loopDown():
            # get each node in corresponding rows
            for rowLoop in colLoop.loopRight():
                # vertically unlink
                rowLoop.up.down = rowLoop.down
                rowLoop.down.up = rowLoop.up
                # dec header count
                if rowLoop.col == -1: colHead = self.root
                else: colHead = self.colHeader[rowLoop.col]
                colHead.count -= 1

    def uncover(self, node: Node) -> None:
        # get the column header
        if node.col == -1: col = self.root
        else: col = self.colHeader[node.col]

        # relink this node and all corresponding
        # iterate through column nodes
        for colLoop in col.loopUp():
            # iterate through corresponding rows
            for rowLoop in colLoop.loopLeft():
                # relink vertically
                rowLoop.up.down = rowLoop
                rowLoop.down.up = rowLoop
                # inc header count
                if rowLoop.col == -1: colHead = self.root
                else: colHead = self.colHeader[rowLoop.col]
                colHead.count += 1

        # relink horizontally
        col.right.left = col
        col.left.right = col
    
    # this is the main search method
    def search(self) -> list[int]:
        solutions = []
        
        # this is the main recursive loop
        def helper() -> bool:
            # If the matrix A has no columns, the current partial solution is a valid solution; terminate successfully.
            if self.root.right == self.root:
                self.solved = True
                return True

            # Otherwise choose a column c (deterministically via min column)
            minCol  = self.root.right
            minCount = self.root.right.count
            for col in self.root.loopRight():
                if col.count < minCount:
                    minCol  = col
                    minCount = col.count

            # min count is 0 so backtrack
            if minCol.count < 1 : return False


            for colLoop in minCol.loopDown():
                # Include row r in the partial solution
                solutions.append(colLoop.row)
                # delete rows and cols from matrix
                for sol_node in colLoop.loopRight(excl=False):
                    if sol_node.col >= 0: self.cover(sol_node)

                self.nodesExplored += 1

                if self.verbosity == 3:
                    # recover solution values
                    solution = [0] * 81
                    for row in solutions:
                        solution[int(row / 9)] = (row % 9) + 1

                    # send to matrix form for return
                    mat: list[list[int]] = [[0 for i in range(9)] for i in range(9)]
                    for r in range(len(mat)):
                        for c in range(len(mat[0])):
                            mat[r][c] = solution[9*r + c]

                    b = Board()
                    for row in range(0, len(mat)):
                        for col in range(0, len(mat[0])):
                            b.rows[row][col].value = mat[row][col]

                    print("Stepping through: " + "\r\r\n{0}\n".format(b))

                    print(b)
                    print("\n")

                # recurse and break if solution found
                if helper(): break

                # solution is not found so revert algo
                solutions.pop()
                # uncover attempted solution row
                for sol_node in colLoop.left.loopLeft(excl=False):
                    # print("hellloooo")
                    if sol_node.col >= 0: self.uncover(sol_node)
            return self.solved

        helper()

        # recover solution values
        solution = [0] * 81
        for row in solutions:
            solution[int(row / 9)] = (row % 9) + 1

        # send to matrix form for return
        mat: list[list[int]] = [[0 for i in range(9)] for i in range(9)]
        for r in range(len(mat)):
            for c in range(len(mat[0])):
                mat[r][c] = solution[9*r + c]
        
        return mat