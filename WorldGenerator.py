# Created 5/25/22
# William Mori
# World Generator

from GameBase import Board
from GameBase import Tile
import random
import AISolver



PREDEFINED = Board({Tile({(0, 0), (0, 1)}, "+", 4),
                    Tile({(0, 2), (1, 2)}, "+", 3),
                    Tile({(0, 3), (1, 3)}, "-", 1),
                    Tile({(1, 0), (2, 0)}, "%", 2),
                    Tile({(1, 1)}, "=", 2),
                    Tile({(2, 1), (3, 1)}, "*", 12),
                    Tile({(2, 2), (2, 3)}, "-", 3),
                    Tile({(3, 2), (3, 3)}, "-", 1),
                    Tile({(3, 0)}, "=", 1)},
                   [[3, 1, 2, 4],
                    [4, 2, 1, 3],
                    [2, 3, 4, 1],
                    [1, 4, 3, 2]])


def genWorld(new: str, size: int) -> Board:
    if new == "True":
        # Steps for generating a board
        # Pick a random board permutation
        # Start dividing the board into tiles
        # Validate this division has a unique solution, if fail throw try placing tiles again

        # Generating a random board process
        # Place a digit in a random location for row 0
        # Then place the digit in a random legal location for row 1
        # Repeat until every row has this digit

        while True:
            try:
                board = [[0 for i in range(size)] for j in range(size)]
                for val in range(1, size+1):
                    usedIndices = []
                    for row in range(0, size):
                        indices = [index for index in range(size) if (board[row][index] == 0 and index not in usedIndices)]
                        loc = random.choice(indices)
                        board[row][loc] = val
                        usedIndices.append(loc)

                break
            except IndexError:
                pass


        # Dividing board process
        # TODO Figure out how max tile size, should probably be something like 1/2 + 1, but then in theory could
        #   have nasty boards that are 10x10 that have a size 6 tile which maybe is fine?
        # Pick a random tile, which some probability decide if this tile should expand
        #   If expanding, pick a direction to expand to
        # Choose operation, if tile has size > 2, operation cannot be subtraction or division, if division results in a
        #   float, then must use subtraction (subtraction will be ordered so that the dividend is always positive)
        # Repeat until no tiles remain
        #   at some point only isolated tiles will exist and they will be placed in noop tiles

        ungroupedTiles = set()
        for i in range(size):
            for j in range(size):
                ungroupedTiles.add((i, j))

        # TODO Change this to make tiles with size greater than 1 or 2, need to figure out how to do this though
        boardTileSet = set()
        while len(ungroupedTiles) != 0:
            startTile = ungroupedTiles.pop()

            # Check which way it's legal to make a move
            legalFollowUps = []
            if startTile[0] - 1 >= 0 and (startTile[0] - 1, startTile[1]) in ungroupedTiles:
                legalFollowUps.append((startTile[0] - 1, startTile[1]))
            if startTile[0] + 1 < size and (startTile[0] + 1, startTile[1]) in ungroupedTiles:
                legalFollowUps.append((startTile[0] + 1, startTile[1]))
            if startTile[1] - 1 >= 0 and (startTile[0], startTile[1] - 1) in ungroupedTiles:
                legalFollowUps.append((startTile[0], startTile[1] - 1))
            if startTile[1] + 1 < size and (startTile[0], startTile[1] + 1) in ungroupedTiles:
                legalFollowUps.append((startTile[0], startTile[1] + 1))

            if len(legalFollowUps) == 0:
                boardTileSet.add(Tile({startTile}, "=", board[startTile[0]][startTile[1]]))
            else:
                nextTile = random.choice(legalFollowUps)
                ungroupedTiles.remove(nextTile)

                operation = random.choice(["+", "-", "*", "%"])
                boardValStart = board[startTile[0]][startTile[1]]
                boardValNext = board[nextTile[0]][nextTile[1]]

                value = 0
                if operation == "%":
                    if boardValStart % boardValNext == 0:
                        value = int(boardValStart / boardValNext)
                    elif boardValNext % boardValStart == 0:
                        value = int(boardValNext % boardValStart)
                    else:
                        operation = random.choice(["+", "-", "*"])

                if operation == "+":
                    value = boardValStart + boardValNext
                elif operation == "-":
                    value = abs(boardValStart - boardValNext)
                elif operation == "*":
                    value = boardValStart * boardValNext
                else:
                    assert(1 == 0, "Failing operation elif")
                assert(value != 0, "Value still somehow 0")
                boardTileSet.add(Tile({startTile, nextTile}, operation, value))

        # Validating board process
        # Probably just use the AI and see what solutions the AI gives, if the AI gives more than one, then repeat
        #   If only 1 solution, then return this board
        retBoard = Board(boardTileSet, board)
        if len(AISolver.AISolver(retBoard)) > 1:
            print("Non unique solution")
        else:
            return retBoard

    else:
        return PREDEFINED
