"""
An AI player for Othello.
"""

import random
import sys
import time
# You can use the functions in othello_shared to write your AI
from othello_shared import find_lines, get_possible_moves, get_score, play_move
from agent import compute_heuristic
# hashmap for caching
cache = {}


def eprint(*args, **kwargs):  # you can use this for debugging, as it will print to sterr and not stdout
    print(*args, file=sys.stderr, **kwargs)


# Method to compute utility value of terminal state
def compute_utility(board, color):
    score = get_score(board)
    return score[0] - score[1] if color == 1 else score[1] - score[0]


# Method to compute opponent
def opponent(color: int) -> int:
    return int(2 / color)


# Function to sort nodes
def sortnodes(board, possible_moves, color):
    against = opponent(color)
    res = []
    dic = {}
    for move in possible_moves:
        (col, row) = move
        new_board = play_move(board, against, col, row)
        utility = compute_heuristic(new_board, color)
        if utility in dic and dic[utility] != [move]:
            dic[utility].append(move)
        else:
            dic[utility] = [move]
    sorted_util = sorted(list(dic.keys()), reverse=True)
    for util in sorted_util:
        res += dic[util]
    return res


# --------------------- MINIMAX ---------------------
def minimax_min_node(board, color, limit, caching=0):
    str_board = str(board)
    if caching and str_board in cache:
        return cache[str_board]
    possible_moves = get_possible_moves(board, opponent(color))
    best_move = None

    if len(possible_moves) == 0 or limit == 0:
        result = (None, compute_heuristic(board, color))
        return result

    min_utility = float("inf")
    for p_move in possible_moves:
        (col, row) = p_move
        new_board = play_move(board, opponent(color), col, row)
        new_str_board = str(new_board)
        _, utility = minimax_max_node(new_board, color, limit - 1, caching)
        if caching:
            cache[new_str_board] = (p_move, utility)
        if utility < min_utility:
            best_move = p_move
            min_utility = utility

    return best_move, min_utility


def minimax_max_node(board, color, limit, caching=0):  # returns highest possible utility
    str_board = str(board)
    if caching and str_board in cache:
        return cache[str_board]
    possible_moves = get_possible_moves(board, color)
    best_move = None
    if len(possible_moves) == 0 or limit == 0:
        result = (None, compute_heuristic(board, color))
        return result

    max_utility = -float("inf")
    for p_move in possible_moves:
        (col, row) = p_move
        new_board = play_move(board, color, col, row)
        new_str_board = str(new_board)
        _, utility = minimax_min_node(new_board, color, limit - 1, caching)
        if caching:
            cache[new_str_board] = (p_move, utility)
        if utility > max_utility:
            best_move = p_move
            max_utility = utility

    return best_move, max_utility


def select_move_minimax(board, color, limit, caching=0):
    """
    Given a board and a player color, decide on a move.
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.

    Note that other parameters are accepted by this function:
    If limit is a positive integer, your code should enfoce a depth limit that is equal to the value of the parameter.
    Search only to nodes at a depth-limit equal to the limit.  If nodes at this level are non-terminal return a heuristic
    value (see compute_utility)
    If caching is ON (i.e. 1), use state caching to reduce the number of state evaluations.
    If caching is OFF (i.e. 0), do NOT use state caching to reduce the number of state evaluations.
    """
    cache.clear()
    move, _ = minimax_max_node(board, color, limit, caching)
    return move


# --------------------- ALPHA-BETA PRUNING ---------------------
def alphabeta_min_node(board, color, alpha, beta, limit, caching=0, ordering=0):
    possible_moves = get_possible_moves(board, opponent(color))
    best_move = (None, None) if len(possible_moves) == 0 else possible_moves[0]
    if len(possible_moves) == 0 or limit == 0:
        result = (None, None), compute_heuristic(board, color)
        return result

    min_utility = float("inf")
    for p_move in possible_moves:
        (col, row) = p_move
        new_board = play_move(board, opponent(color), col, row)
        new_str_board = str(new_board)
        if caching and new_str_board in cache:
            utility = cache[new_str_board]
        else:
            _, utility = alphabeta_max_node(new_board, color, alpha, beta, limit - 1, caching)
            if caching:
                cache[new_str_board] = utility
        if utility < min_utility:
            best_move = p_move
            min_utility = utility
        # alpha-beta pruning
        beta = min(beta, utility)
        if beta <= alpha:
            break

    return best_move, min_utility


def alphabeta_max_node(board, color, alpha, beta, limit, caching=0, ordering=0):
    # IMPLEMENT (and replace the line below)
    possible_moves = get_possible_moves(board, color)
    best_move = (None, None) if len(possible_moves) == 0 else possible_moves[0]
    if len(possible_moves) == 0 or limit == 0:
        result = (None, None), compute_heuristic(board, color)
        return result
    if ordering:
        possible_moves = sortnodes(board, possible_moves, color)
    max_utility = -float("inf")
    for p_move in possible_moves:
        new_board = play_move(board, color, p_move[0], p_move[1])
        new_str_board = str(new_board)
        if caching and new_str_board in cache:
            utility = cache[new_str_board]
        else:
            _, utility = alphabeta_min_node(new_board, color, alpha, beta, limit - 1, caching)
            if caching:
                cache[new_str_board] = utility
        if utility > max_utility:
            best_move = p_move
            max_utility = utility
        # alpha-beta pruning
        alpha = max(alpha, utility)
        if beta <= alpha:
            break

    return best_move, max_utility


def select_move_alphabeta(board, color, limit, caching=0, ordering=0):
    """
    Given a board and a player color, decide on a move.
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.

    Note that other parameters are accepted by this function:
    If limit is a positive integer, your code should enfoce a depth limit that is equal to the value of the parameter.
    Search only to nodes at a depth-limit equal to the limit.  If nodes at this level are non-terminal return a heuristic
    value (see compute_utility)
    If caching is ON (i.e. 1), use state caching to reduce the number of state evaluations.
    If caching is OFF (i.e. 0), do NOT use state caching to reduce the number of state evaluations.
    If ordering is ON (i.e. 1), use node ordering to expedite pruning and reduce the number of state evaluations.
    If ordering is OFF (i.e. 0), do NOT use node ordering to expedite pruning and reduce the number of state evaluations.
    """
    cache.clear()
    move, _ = alphabeta_max_node(board, color, -float('inf'), float('inf'), limit, caching, ordering)
    return move


# --------------------------------------------------------------------
def run_ai():
    """
    This function establishes communication with the game manager.
    It first introduces itself and receives its color.
    Then it repeatedly receives the current score and current board state
    until the game is over.
    """
    print("Othello AI++")  # First line is the name of this AI
    arguments = input().split(",")

    color = int(arguments[0])  # Player color: 1 for dark (goes first), 2 for light.
    limit = int(arguments[1])  # Depth limit
    minimax = int(arguments[2])  # Minimax or alpha beta
    caching = int(arguments[3])  # Caching
    ordering = int(arguments[4])  # Node-ordering (for alpha-beta only)

    if (minimax == 1):
        eprint("Running MINIMAX")
    else:
        eprint("Running ALPHA-BETA")

    if (caching == 1):
        eprint("State Caching is ON")
    else:
        eprint("State Caching is OFF")

    if (ordering == 1):
        eprint("Node Ordering is ON")
    else:
        eprint("Node Ordering is OFF")

    if (limit == -1):
        eprint("Depth Limit is OFF")
    else:
        eprint("Depth Limit is ", limit)

    if (minimax == 1 and ordering == 1): eprint("Node Ordering should have no impact on Minimax")

    while True:  # This is the main loop
        # Read in the current game status, for example:
        # "SCORE 2 2" or "FINAL 33 31" if the game is over.
        # The first number is the score for player 1 (dark), the second for player 2 (light)
        next_input = input()
        status, dark_score_s, light_score_s = next_input.strip().split()
        dark_score = int(dark_score_s)
        light_score = int(light_score_s)

        if status == "FINAL":  # Game is over.
            print
        else:
            board = eval(input())  # Read in the input and turn it into a Python
            # object. The format is a list of rows. The
            # squares in each row are represented by
            # 0 : empty square
            # 1 : dark disk (player 1)
            # 2 : light disk (player 2)

            # Select the move and send it to the manager
            if (minimax == 1):  # run this if the minimax flag is given
                movei, movej = select_move_minimax(board, color, limit, caching)
            else:  # else run alphabeta
                movei, movej = select_move_alphabeta(board, color, limit, caching, ordering)

            print("{} {}".format(movei, movej))


if __name__ == "__main__":
    run_ai()
