import json
from files.xox_api import xox_api
from files.tic_graph import print_board, gStatus
def run_game():
    board = [
        ".",".",".",
        ".",".",".",
        ".",".","."
         ]

    while True:
        try:
            level = int(input("Select difficulty (0-2): "))

            if level in (0, 1, 2):
                break

            print("Difficulty must be between 0 and 2.")

        except ValueError:
            print("Please enter a valid number.")


    while gStatus(board) == "No winner":

        print_board(board)

        try:
            move = int(input("Your move (1-9): ")) - 1
        except ValueError:
            print("Please enter a valid number.")
            continue

        if not 0 <= move <= 8:
            print("Please enter a number between 1 and 9.")
            continue

        if board[move] != ".":
            print("That square is already occupied.")
            continue

        board[move] = "X"

        if gStatus(board) != "No winner":
            break

        request = {
            "board": board,
            "player": "O",
            "level": level
        }

        request_json = json.dumps(request)

        response_json = xox_api(request_json)

        response = json.loads(response_json)

        bot_move = response["move"]

        print("Bot selected:", bot_move + 1)

        board[bot_move] = "O"

    print_board(board)
    print("Game result:", gStatus(board))