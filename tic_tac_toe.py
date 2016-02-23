"""
Monte Carlo Tic-Tac-Toe Player
"""

import math
import random
import ttt_gui
import ttt_board


# Constants for Monte Carlo simulator:
NTRIALS = 20       # Number of trials to run
SCORE_CURRENT = 1.0 # Score for squares played by the current player
SCORE_OTHER = 1.0   # Score for squares played by the other player



def mc_trial(board, player): 
    """
    Plays a game starting with the given player by 
    making random moves, alternating between
    players. Returns when the game is over. The 
    modified board will contain the state of 
    the game, so it doesn't return anything. 
    """
    winner = None
    while winner == None:
        # Make a move:
        board_dim = board.get_dim()
        row = random.randrange(0, board_dim)
        col = random.randrange(0, board_dim)
        board.move(row, col, player)

        # Update state:
        winner = board.check_win()
        player = ttt_board.switch_player(player)
    return

def mc_update_scores(scores, board, player): 
    """
    Takes a grid of scores (list of lists) with 
    the same dimensions as the Tic-Tac-Toe board, 
    a board from a completed game, and which player 
    the machine player is. Scores the completed 
    board and updates the scores grid. As the function 
    updates the scores grid directly, it does 
    not return anything.
    """
    winner = board.check_win()
    if winner != ttt_board.DRAW:
        if winner == player:
            score_good = SCORE_CURRENT
            score_bad = SCORE_OTHER
        else:
            score_good = SCORE_OTHER
            score_bad = SCORE_CURRENT
        
        board_dim = board.get_dim()
        for row_num in range(board_dim):
            for col_num in range(board_dim):
                sqr = board.square(row_num, col_num)
                if sqr != ttt_board.EMPTY:
                    if sqr == winner:
                        scores[row_num][col_num] += score_good
                    else:
                        scores[row_num][col_num] -= score_bad
    return


def get_best_move(board, scores): 
    """
    This function takes a current board 
    and a grid of scores. The function 
    should find all of the empty squares 
    with the maximum score and randomly 
    return one of them as a (row, column) tuple. 
    It is an error to call this function 
    with a board that has no empty squares 
    (there is no possible next move).
    """
    emp_sqs = board.get_empty_squares()
    max_so_far = emp_sqs[0]
    for tup in emp_sqs[1:]:
        if scores[tup[0]][tup[1]] > scores[max_so_far[0]][max_so_far[1]]:
            max_so_far = tup
    return max_so_far
        
    
    
                                
def mc_move(board, player, trials): 
    """
    Takes a current board, 
    which player the machine player is, 
    and the number of trials to run. Uses a 
    Monte Carlo simulation to return a move 
    for the machine player in the form of a 
    (row, column) tuple.
    """
    brd_dim = board.get_dim()
    scores = [[0 for dummy_col in range(brd_dim)] 
              for dummy_row in range(brd_dim)]
    
    for dummy_i in range(trials):
        trial_board = board.clone()
        mc_trial(trial_board, player)
        mc_update_scores(scores, trial_board, player)
    best_move = get_best_move(board, scores)
    return best_move
        
         
ttt_board.play_game(mc_move, NTRIALS, False)        
ttt_gui.run_gui(3, ttt_board.PLAYERX, mc_move, NTRIALS, False)