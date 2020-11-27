"""
Tic Tac Toe Player
"""

import math
import copy
import itertools

X = "X"
O = "O"
EMPTY = None
OO = 2


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    turn = 0
    for i in range(len(board)):
        for j in range(len(board[0])):
            turn += (board[i][j] != EMPTY)
    return X if (turn % 2 == 0) else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_moves = []
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == EMPTY:
                possible_moves.append((i, j))
    return possible_moves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    new_board = copy.deepcopy(board)
    if new_board[action[0]][action[1]] == EMPTY:
        new_board[action[0]][action[1]] = player(board)
    else:
        raise NameError("Invalid move")
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    global X
    rows = [0] * 3
    cols = [0] * 3
    main_diagonal = [0] * 5
    rev_diagonal = [0] * 5

    def update_cell(_i, _j, _val):
        rows[_i] += _val
        cols[_j] += _val
        main_diagonal[_i - _j + 2] += _val
        rev_diagonal[_i + j] += _val

    for i in range(3):
        for j in range(3):
            value = 1 if board[i][j] == X else -1 if board[i][j] == O else 0
            update_cell(i, j, value)

    for val in itertools.chain(rows, cols, main_diagonal, rev_diagonal):
        if val == 3:
            return X
        if val == -3:
            return O
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return True
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                return False
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    winner_player = winner(board)
    return 0 if winner_player is None else 1 if winner_player == X else -1


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    return maximize(board)[1] if player(board) == X else minimize(board)[1]




def maximize(_board, beta=OO):
    """
       Return tuple(max_score_for_x,action=> best_move_for_x)
       return score,None in case of terminal board
    """
    if terminal(_board):
        return utility(_board), None

    score = -OO
    best_action = None
    for action in actions(_board):
        # Alpha-beta pruning
        if beta <= score:
            return score, best_action

        new_score, act = minimize(result(_board, action), score)
        if new_score > score:
            score = new_score
            best_action = action
    return score, best_action


def minimize(_board, alpha=-OO):
    """
       Return tuple(min_score_for_O,action=> best_move_for_O)
       return score,None in case of terminal board
    """
    if terminal(_board):
        return utility(_board), None

    score = OO
    best_action = None
    for action in actions(_board):
        # Alpha-beta pruning
        if alpha >= score:
            return score, best_action

        new_score, act = maximize(result(_board, action), score)
        if new_score < score:
            score = new_score
            best_action = action

    return score, best_action
