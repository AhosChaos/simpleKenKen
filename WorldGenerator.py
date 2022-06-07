# Created 5/25/22
# William Mori
# World Generator

from collections import namedtuple

UNIQUETILEIDS = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
                 "u", "v", "w", "x", "y", "z",
                 "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "!", "@", "#", "$", "%", "^", "&", "*", "~", ")",
                 "-", "=", "+", "<", ">", "?",
                 "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
                 "U", "V", "W", "X", "Y", "Z"
                 ]


class Tile:
    def __init__(self, location: set, operation: str, value: int):
        self.location = location  # set of x,y tuples with 0,0 in the top left corner
        self.operation = operation  # operation of the tile, "no" operation is represented as "="
        self.value = value  # value the numbers in the tile must ultimately equal


class Board:
    def __init__(self, tiles: {Tile}, solution: [[int]]):
        self.tiles = tiles  # set of tiles creating an abstract view of the board
        # TODO Check if solution is redundant, or if it can be built from tiles, really depends on how boards are
        #  generated, size and dim can instead be passed as arguments if tiles is sufficient
        self.solution = solution  # true value of the tiles
        self.size = len(solution)
        self.dim = self.size - 1

        VisualTile = namedtuple("VisualTile", ["operation", "value", "order"])
        self.visualBoard = [[VisualTile(".", "0", ".") for i in range(self.size)] for j in range(self.size)]
        maxValue = 0  # Used for figuring out space for pretty printing
        tileId = 0
        for tileSet in self.tiles:
            for tileX, tileY in tileSet.location:
                self.visualBoard[tileX][tileY] = VisualTile(tileSet.operation, tileSet.value, UNIQUETILEIDS[tileId])
                if tileSet.value > maxValue:
                    maxValue = tileSet.value
            tileId += 1

        self.maxWidth = len(str(maxValue))

        self.userBoard = [[0 for i in range(self.size)] for j in range(self.size)]

    def printBoard(self):
        print('\t', end="")
        for i in range(self.size):
            print(i, end='\t')
        print()

        # TODO Update printing method for a prettier board method, current method relies on monospaced terminal output
        #   for the board to look nice.  Ideally each cell would be tab separated, but to generate a more visual board
        #   using tkinter or pygame, the visual board is enough and this method can eventually be ignored

        for i in range(self.size):
            print("\t", "-" * self.size * 4)    # Horizontal demarcation
            print(i, end="\t|")                 # Row number

            # Print the operation and tile value
            for j in range(self.size):
                charDiff = self.maxWidth - len(str(self.visualBoard[i][j].value))
                end = " " * charDiff + "|"
                print(str(self.visualBoard[i][j].operation) + str(self.visualBoard[i][j].value), end=end)
            print()

            # Print the order and user value
            print("", end="\t|")
            for j in range(self.size):
                if self.userBoard[i][j] != 0:
                    end = " " * (self.maxWidth - len(str(self.userBoard[i][j]))) + "|"
                    print(str(self.visualBoard[i][j].order) + str(self.userBoard[i][j]), end=end)
                else:
                    end = " " * self.maxWidth + "|"
                    print(str(self.visualBoard[i][j].order), end=end)
            print()


PREDEFINED = Board({Tile({(0, 0), (0, 1)}, "+", 4),
                    Tile({(0, 2), (1, 2)}, "+", 3),
                    Tile({(0, 3), (1, 3)}, "-", 1),
                    Tile({(1, 0), (2, 0)}, "/", 2),
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
        assert 1 == 0
    else:
        return PREDEFINED
