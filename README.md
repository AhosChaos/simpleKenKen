# simpleKenKen
A simple command line KenKen program.

usage: main.py [-h] (-m | -a | -d) size {True,False}

positional arguments:
  size             Size of the board to be played on
  {True,False}     If True a new a board will made, if False an existing board
                   will be used and size may be ignored

required optional arguments:
  -h, --help       show this help message and exit
  -m, --manual     Manual playing of a kenken game, automatically verbose
  -a, --automatic  AI will solve this world
  -d, --debug      AI will stop and show intermediate states
  
  
### Future changes and updates:
  - Improve AI to solve puzzles beyond trivially solvable puzzles.  This will improve the quality of puzzles that are generated as unless the puzzle is solvable by the AI, the puzzle with not be returned to the user to avoid multiple solution puzzles
  - Save generated boards and allow seeding for board generation.  This will allow puzzles to be replayable
 
### Project Status: Paused

  I have to decided to shift my time to other projects.  This project started as an in between type project, something I could work on and do while I was between bigger projects.  As such, this project is of a lower priority for me.
  
