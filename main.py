# Created 5/25/22
# William Mori
# Main

import argparse
import WorldGenerator

def queryIntInput(varName: str, varRange: (int, int), inputMsg: str) -> int:
    while True:
        try:
            retVal = int(input(inputMsg))
            if retVal >= varRange[0] and retVal <= varRange[1]:
                return retVal
            print("Invalid input for", varName, "enter a number in range", varRange)

        except ValueError:
            print("Invalid input for", varName, "enter a number in range", varRange)


if __name__ == "__main__":
    # TODO Change this to be a more comprehensive completion check ie check the that all of the tile constraints are met
    #   Move this function into world gen since it will be used to validate a newly created board is unique
    def checkCompletion(solution, progress):
        return all(solution[i][j] == progress[i][j] for i in range(len(solution)) for j in range(len(solution)))


    def runManual(board):
        board.printBoard()

        while not checkCompletion(board.solution, board.userBoard):
            userXVal = queryIntInput("x coordinate", (0, board.dim), "Enter a value for the x coordinate:")
            userYVal = queryIntInput("y coordinate", (0, board.dim), "Enter a value for the y coordinate:")
            userVal = queryIntInput("value", (1, board.size), "Enter a to place at the coordinate:")

            board.userBoard[userYVal][userXVal] = userVal
            board.printBoard()

        print("PUZZLE COMPLETE!")

    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-m", "--manual", help="Manual playing of a kenken game, automatically verbose", action="store_true")
    group.add_argument("-a", "--automatic", help="AI will solve this world", action="store_true")
    group.add_argument("-d", "--debug", help="AI will stop and show intermediate states", action="store_true")
    parser.add_argument("size", type=int)
    parser.add_argument("new", choices=["True", "False"], help="If True a new a board will made, if False an existing board will be used")

    args = parser.parse_args()

    board = WorldGenerator.genWorld(args.new, args.size)

    if args.manual is True:
        runManual(board)
    elif args.automatic is True:
        #runAuto()
        pass
    else:
        #runDebug()
        pass
    #print(args)



