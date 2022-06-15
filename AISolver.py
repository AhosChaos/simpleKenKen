# Cretated 6/8/2022
# William Mori
# AISolver
from typing import List

from GameBase import Board
from GameBase import Tile

VERBOSE = False
DEBUG = False

class AISolver:
    class PossibleValue:
        def __init__(self, location: (int, int), value):
            self.location = location
            self.value = value

    class SolutionTile:
        def __init__(self, tile: Tile):
            self.tile = tile
            self.tileOrder = sorted(list(self.tile.location))  # Assign tiles an order based on their coordinates
            self.solutions = []  # List of possible legal solutions for this tile

    def __init__(self, board: Board):
        self.board = board
        self.locToTile = {}
        for tile in self.board.tiles:
            for loc in tile.location:
                self.locToTile[loc] = tile

        self.csBoard = [[set() for i in range(self.board.size)] for j in range(self.board.size)]  # Constraint Board

    def solve(self) -> [[[int]]]:
        """
        :return: List of possible solutions to the problem
        """
        # Steps to solve a board
        # Set constraints for each tile including legal remaining tiles and legal values to be placed
        # Fill in all single value tiles
        # Build CSP search tree?

        for i in self.board.tiles:
            if len(i.location) == 1:
                tileLoc = next(iter(i.location))
                self.board.userBoard[tileLoc[0]][tileLoc[1]] = i.value
        if VERBOSE: print("Finished assigning defaults")
        if DEBUG:  self.board.printBoard()
        self._genLegalVals()
        for i in self.csBoard:
            if DEBUG: print(i)

        # At this point the first "iteration is done"
        # Repeat doing these iterations until there are no more single legal value squares
        # Can begin a search tree from there

        while True:
            updatedVal = False
            for row in range(self.board.size):
                for col in range(self.board.size):
                    if len(self.csBoard[row][col]) == 1:
                        self.board.userBoard[row][col] = self.csBoard[row][col].pop()
                        updatedVal = True
            if updatedVal is True:
                self._genLegalVals()
            else:
                if DEBUG: self.board.printBoard()
                for i in self.csBoard:
                    if DEBUG: print(i)
                break



        if all(self.board.userBoard[row][col] != 0 for row in range(self.board.size) for col in range(self.board.size)):
            return [self.board.userBoard]
        else:
            if DEBUG: print("Giving up on the world")
            return [False, False]

    def _genSolTiles(self):
        pass

    def _checkConsistent(self, coord: (int, int), value: int):
        """
        Checks if a given location and value are consistent with the board state
        :param coord: Location of the value to be checked
        :param value: Integer value for the square
        :return: Boolean True if consistent, False otherwise
        """
        for i in self.board.userBoard:
            if i[coord[1]] == value:
                return False

        for i in self.board.userBoard[coord[0]]:
            if i == value:
                return False

        return True

    def _genLegalVals(self):
        """
        Generates every legal value for each square initially ignoring the tile constraints then filters down
        :return:
        """
        fullLegalSet = set([i for i in range(1, self.board.size + 1)])
        rowSets = {}
        colSets = {}

        for i in range(self.board.size):
            rowSets[i] = set(self.board.userBoard[i])
        for i in range(self.board.size):
            colSets[i] = set([self.board.userBoard[j][i] for j in range(self.board.size)])

        for row in range(self.board.size):
            for col in range(self.board.size):
                self.csBoard[row][col] = fullLegalSet.difference(rowSets[row]).difference(colSets[col])

        # TODO Constraint matching with the Tile value
        #   How can I denote that certain values are bound to each other?
        #   Maybe I just don't and "resolve" everytime I fill something in, the math is trivial, but ideally
        #   Solving 1 value in a tile would immediately let us know the other values in the tile
        #   If have squares A and B, can reduce the legal values in A by seeing if there are values in B that
        #   can legally complete the operation, for A, B, and C, then check if combination of values in B and C work?

        for i in self.csBoard:
            if DEBUG: print(i)

        # Filter out the values based on tile now
        # For each square, load the tile
        # For each legal value in the square, see if the operation can be completed with a value from the other
        #   side of the tile, if it can, do nothing, otherwise remove this value from the square
        # (Operations are treated as symmetric, arranged so the result is a positive integer)
        for row in range(self.board.size):
            for col in range(self.board.size):
                values = self.csBoard[row][col]
                tile = self.locToTile[(row, col)]
                valsToRemove = set()
                for i in values:
                    if len(tile.location) > 1:
                        neighbor = tile.location.difference({(row, col)}).pop()
                        neighborValues = self.csBoard[neighbor[0]][neighbor[1]]
                        otherHalf = self._evalOperation(tile.operation, i, tile.value)

                        if all([val not in neighborValues for val in otherHalf]):
                            valsToRemove.add(i)
                    else:
                        values = set()  # Set this to an empty set for cleanup later?

                self.csBoard[row][col] = values.difference(valsToRemove)

    # TODO This evaluate is ignorant of the other "legal" values in the tile and assumes that the tile has size 2
    #   to fix this, make a function that takes in the left value, and a list of squares with legal values
    def _evalOperation(self, op: str, left: int, val: int) -> [int]:
        """
        Finds the number to complete the tile
        :param op: Operation used in the tile
        :param left: Value that is known
        :param val: Value that is the goal to equate to
        :return: Integer that when combined with left via the operation results in val
        """

        if op == "+":
            return [val - left]
        elif op == "-":
            # Can trim this down to prevent values that are outside of the legal range, but these will be pruned
            #   regardless in the next step
            retVals = []
            retVals.append(left + val)
            retVals.append(left - val)

            return retVals

        elif op == "*":
            if val % left != 0:
                return [-1]
            return [val // left]

        elif op == "%":
            retVals = []
            # Not very happy with this, there should be a non iterative way to get both potential integers for
            #   division
            # TODO Make this look a little nicer, can rearrange booleans to make this cleaner
            for i in range(1, self.board.size+1):
                if left % val == 0 and left / val == i:
                    retVals.append(i)
                if val % left == 0 and val / left == i:
                    retVals.append(i)
                if i % left == 0 and (i / left == val or left / i == val):
                    retVals.append(i)
                if left * i == val:
                    retVals.append(i)

            if len(retVals) == 0:
                retVals.append(-1)
            return retVals

        return [-1]


def verifySolution(tileSet: {Tile}, board: [[int]]) -> bool:
    """
    :param tileSet: Set of Tiles that comprise the board
    :param board: Solution board to be verified
    :return: boolean value whether the solution board satisfies the tile constraints
    """
    # Two steps in verifying a solution
    #   Check that every tile is satisfied
    #   Check that the overall board state is consistent

    # Check constraints of tiles, maybe make this a function by itself
    for tile in tileSet:
        # Not too happy having to cast the location set to a list everytime, but it'll have to do for now
        tileLocs = list(tile.location)
        startTile = tileLocs[0]
        if tile.operation == "=":
            if board[startTile[0]][startTile[1]] != tile.value:
                return False

        if tile.operation == "+":
            total = 0
            for loc in tile.location:
                total += board[loc[0]][loc[1]]
            if total != tile.value:
                return False

        if tile.operation == "*":
            product = 1
            for loc in tile.location:
                product *= board[loc[0]][loc[1]]
            if product != tile.value:
                return False

        if tile.operation == "-":
            nextTile = tileLocs[1]
            if abs(board[startTile[0]][startTile[1]] - board[nextTile[0]][nextTile[1]]) != tile.value:
                return False

        if tile.operation == "%":
            nextTile = tileLocs[1]
            if board[startTile[0]][startTile[1]] != 0 and board[nextTile[0]][nextTile[1]] != 0 and \
                    board[startTile[0]][startTile[1]] % board[nextTile[0]][nextTile[1]] != 0 and \
                    board[nextTile[0]][nextTile[1]] % board[startTile[0]][startTile[1]] != 0:
                return False

    # Quick and dirty way to evaluate the board state is consistent is to turn all rows and columns into sets
    #   duplicate values will be ignored and the resultant sets can be compared to a valid reference set

    rowColSets = []
    for row in board:
        rowColSets.append(set(row))

    for col in range(len(board)):
        colSet = set()
        for row in board:
            colSet.add(row[col])
        rowColSets.append(colSet)

    referenceSet = set([i for i in range(1, len(board) + 1)])
    return all(referenceSet == i for i in rowColSets)
