"""Illustration of tournament.

Authors:
    Alejandro Bellogin <alejandro.bellogin@uam.es>

"""

from __future__ import annotations  # For Python 3.7

import numpy as np

import random

from game import Player, TwoPlayerGameState, TwoPlayerMatch
from heuristic import simple_evaluation_function, original_evaluation_function, pesos_evaluation_function, finish_evaluation_function, dynamic_evaluation_function
from reversi import (
    Reversi,
    from_array_to_dictionary_board,
    from_dictionary_to_array_board,
)
from tournament import StudentHeuristic, Tournament

class Heuristic1(StudentHeuristic):

    def get_name(self) -> str:
        return "Mamadisimo Pesos"

    def evaluation_function(self, state: TwoPlayerGameState) -> float:
        # Use an auxiliary function.
        return pesos_evaluation_function(state)


class Heuristic2(StudentHeuristic):

    def get_name(self) -> str:
        return "Mamadisimo Finish"

    def evaluation_function(self, state: TwoPlayerGameState) -> float:
        return finish_evaluation_function(state)


class Heuristic3(StudentHeuristic):

    def get_name(self) -> str:
        return "Mamadisima Original"

    def evaluation_function(self, state: TwoPlayerGameState) -> float:
        return original_evaluation_function(state)


class Heuristic4(StudentHeuristic):

    def get_name(self) -> str:
        return "Mamadisima Dynamic"

    def evaluation_function(self, state: TwoPlayerGameState) -> float:
        # Use an auxiliary function.
        return dynamic_evaluation_function(state)


class Heuristic5(StudentHeuristic):

    def get_name(self) -> str:
        return "simple"

    def evaluation_function(self, state: TwoPlayerGameState) -> float:
        return simple_evaluation_function(state)


class Heuristic6(StudentHeuristic):

    def get_name(self) -> str:
        return "random"

    def evaluation_function(self, state: TwoPlayerGameState) -> float:
        return float(np.random.rand())

class Heuristic7(StudentHeuristic):

    def get_name(self) -> str:
        return "dummy"

    def evaluation_function(self, state: TwoPlayerGameState) -> float:
        # Use an auxiliary function.
        return self.dummy(123)

    def dummy(self, n: int) -> int:
        return n + 4

def create_match(player1: Player, player2: Player) -> TwoPlayerMatch:

    initial_board = None#np.zeros((dim_board, dim_board))
    initial_player = player1

    """game = TicTacToe(
        player1=player1,
        player2=player2,
        dim_board=dim_board,
    )"""

    initial_board = [
        ['........',
        '........',
        '........',
        '...WB...',
        '...BW...',
        '........',
        '........',
        '........']
    ]

    '''['........',
        '......W.',
        '...WWBB.',
        '..WBBB..',
        '.WWWWB..',
        '..BBBW..',
        '..B.....',
        '........'],

        ['........',
        '.WBBB...',
        'WBBBB...',
        '..BWWW..',
        '..BWWBB.',
        '.BWWW...',
        '........',
        '........'],

        ['........',
        '........',
        '........',
        '...WB...',
        '...BW...',
        '........',
        '........',
        '........'],

        ['........',
        '.WBBB...',
        '..BBB...',
        '..BBBW..',
        '..BBWW..',
        '.BBBW...',
        '........',
        '........'],
        ['........',
        '........',
        '....W...',
        '...WWWB.',
        '...BW...',
        '........',
        '........',
        '........'],
        ['........',
        '........',
        '...BW...',
        '...WWWB.',
        '...BW...',
        '........',
        '........',
        '........'],
        ['........',
        '....W...',
        '...BBBBB',
        '...WWBB.',
        '...BWB..',
        '........',
        '........',
        '........'],
        ['........',
        '....WB..',
        '....WBBB',
        '..WWWBB.',
        '..BBWB..',
        '...BW...',
        '........',
        '........'],
        ['.WB..BW.',
        '.WBBW...',
        'WBWBB...',
        '.W.WWW..',
        '.BBWBWB.',
        'BBWBB...',
        'WW.WWW..',
        '.BBWBWW.']
    '''

    num_board = random.randint(0,len(initial_board)-1)
    if initial_board is None:
        height, width = 8, 8
    else:
        height = len(initial_board)
        width = len(initial_board[0])
        try:
            initial_board = from_array_to_dictionary_board(initial_board[num_board])
        except ValueError:
            raise ValueError('Wrong configuration of the board')
        else:
            height=8
            #print("Successfully initialised board from array")

    game = Reversi(
        player1=player1,
        player2=player2,
        height=8,
        width=8
    )

    game_state = TwoPlayerGameState(
        game=game,
        board=initial_board,
        initial_player=initial_player,
    )

    return TwoPlayerMatch(game_state, max_seconds_per_move=1000, gui=False)


tour = Tournament(max_depth=3, init_match=create_match)
strats = {'opt1': [Heuristic3]}#, 'opt2': [Heuristic2],'opt3': [Heuristic3],'opt4': [Heuristic4],'opt5': [Heuristic5],'opt6': [Heuristic6], 'opt7': [Heuristi]}

n = 1
scores, totals, names = tour.run(
    student_strategies=strats,
    increasing_depth=False,
    n_pairs=n,
    allow_selfmatch=True,
)

'''print(
    'Results for tournament where each game is repeated '
    + '%d=%dx2 times, alternating colors for each player' % (2 * n, n),
)'''

# print(totals)
# print(scores)

'''print('\ttotal:', end='')
for name1 in names:
    print('\t%s' % (name1), end='')
print()
for name1 in names:
    print('%s\t%d:' % (name1, totals[name1]), end='')
    for name2 in names:
        if name1 == name2:
            print('\t---', end='')
        else:
            print('\t%d' % (scores[name1][name2]), end='')
    print()'''
