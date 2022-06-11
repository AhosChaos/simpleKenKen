# Cretated 6/8/2022
# William Mori
# AISolver
from typing import List

from GameBase import Board
from GameBase import Tile


# Should this be a class, or can it just be left as a collection of functions

def AISolver(Board) -> [[[int]]]:
    """
    :param Board: Input board to be solved, complete with Tiles
    :return: List of 2D matrices of valid solutions to the board
    """

    # Steps to solve a board
    # Set constraints for each tile including legal remaining tiles and legal values to be placed
    # Fill in all single value tiles
    #

    return


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
            if board[startTile[0]][startTile[1]] % board[nextTile[0]][nextTile[1]] != 0 and \
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

    referenceSet = set([i for i in range(1, len(board)+1)])
    return all(referenceSet == i for i in rowColSets)
