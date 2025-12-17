#Alpha-Beta pruning

import math

# ----- Game Setup -----

def print_board(board):
    for row in board:
        print(row)
    print()

def available_moves(board):
    moves = []
    for r in range(3):
        for c in range(3):
            if board[r][c] == " ":
                moves.append((r, c))
    return moves

def winner(board):
    # Rows
    for row in board:
        if row[0] != " " and row[0] == row[1] == row[2]:
            return row[0]

    # Columns
    for c in range(3):
        if board[0][c] != " " and board[0][c] == board[1][c] == board[2][c]:
            return board[0][c]

    # Diagonals
    if board[0][0] != " " and board[0][0] == board[1][1] == board[2][2]:
        return board[0][0]

    if board[0][2] != " " and board[0][2] == board[1][1] == board[2][0]:
        return board[0][2]

    return None

def is_terminal(board):
    return winner(board) is not None or len(available_moves(board)) == 0

# ----- Minimax -----

def minimax(board, is_maximizing):
    win = winner(board)
    if win == "X":
        return 1
    elif win == "O":
        return -1
    elif len(available_moves(board)) == 0:
        return 0

    if is_maximizing:
        best_score = -math.inf
        for (r, c) in available_moves(board):
            board[r][c] = "X"
            score = minimax(board, False)
            board[r][c] = " "
            best_score = max(best_score, score)
        return best_score
    else:
        best_score = math.inf
        for (r, c) in available_moves(board):
            board[r][c] = "O"
            score = minimax(board, True)
            board[r][c] = " "
            best_score = min(best_score, score)
        return best_score

# ----- Best Move for AI (X) -----

def best_move(board):
    best_score = -math.inf
    move = None
    for (r, c) in available_moves(board):
        board[r][c] = "X"
        score = minimax(board, False)
        board[r][c] = " "
        if score > best_score:
            best_score = score
            move = (r, c)
    return move

# ----- Example -----

board = [
    ["X", "O", "X"],
    [" ", "O", " "],
    [" ", " ", " "]
]

print_board(board)
print("Best move for X:", best_move(board))
