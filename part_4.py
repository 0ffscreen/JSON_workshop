"""
Tic-Tac-Toe Game

By this point, you have already gone over everything you need to know to implement JSON in Python.

This is a little practical exercise where you can try building your very own Tic-Tac-Toe (or XOX) game to test your knowledge
so far.

You are provided with three premade functions:
1. print_board(board)
   - Takes in the current board and displays it.
2. gStatus(board)
   - Takes in the current board and returns its status.
   - Possible outputs: "X", "O", "Draw", "No winner".
3. xox_api(request)
   - Takes in a JSON string and returns a JSON string.
   - Acts as your opponent in the game.

   The request must follow this structure:
   {
       "board": [".", ".", ".", ".", ".", ".", ".", ".", "."],
       "player": "X",
       "level": 2
   }

   board  : The current state of the board.
            "." represents an empty square.

   player : The player the bot should play as (X or O).

   level  : The difficulty of the bot (optional).
            0 = Random moves.
            1 = Most possible winning paths.
            2 = Strategic moves (default).

   The response will look something like this:

   {"move": 4}

   The move represents the index of the square chosen by the bot.
   It will be null if the game has already ended.

Remember:
    - X always goes first.
    - Board indexes range from 0 to 8.
    - print_board() displays empty squares as 1 to 9.
    - You cannot place a symbol in an occupied square.

Your goal is to build a playable Tic-Tac-Toe game using the functions provided and what you have learned so far.

Feel free to experiment with different difficulty levels, game modes or even make two bots play against each other.

Good luck!
"""

import json
from files.testing import run_game
from files.xox_api import xox_api
from files.tic_graph import print_board, gStatus

board = [
    ".", ".", ".",
    ".", ".", ".",
    ".", ".", "."
]

# Your code goes here!






























#the code below is an example of how it could look upon finish 
#from files.testing import run_game
#run_game()