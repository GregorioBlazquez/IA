"""Heuristics to evaluate board.

    Authors:
        Fabiano Baroni <fabiano.baroni@uam.es>,
        Alejandro Bellogin <alejandro.bellogin@uam.es>
        Alberto Suárez <alberto.suarez@uam.es>

"""


from __future__ import annotations  # For Python 3.7

from typing import Callable, Sequence

import numpy as np

from reversi import Reversi

from game import TwoPlayerGameState


class Heuristic(object):
    """Encapsulation of the evaluation fucnction."""

    def __init__(
        self,
        name: str,
        evaluation_function: Callable[[TwoPlayerGameState], float],
    ) -> None:
        """Initialize name of heuristic & evaluation function."""
        self.name = name
        self.evaluation_function = evaluation_function

    def evaluate(self, state: TwoPlayerGameState) -> float:
        """Evaluate a state."""
        # Prevent modifications of the state.
        # Deep copy everything, except attributes related
        # to graphical display.
        state_copy = state.clone()
        return self.evaluation_function(state_copy)

    def get_name(self) -> str:
        """Name getter."""
        return self.name


def simple_evaluation_function(state: TwoPlayerGameState) -> float:
    """Return a random value, except for terminal game states."""
    state_value = 2*np.random.rand() - 1

    if state.end_of_game:
        scores = state.scores
        # Evaluation of the state from the point of view of MAX

        assert iifnstance(scores, (Sequence, np.ndarray))
        score_difference = scores[0] - scores[1]

        if state.is_player_max(state.player1):
            state_value = score_difference
        elif state.is_player_max(state.player2):
            state_value = - score_difference
        else:
            raise ValueError('Player MAX not defined')

    return state_value



heuristic = Heuristic(
    name='Simple heuristic',
    evaluation_function=simple_evaluation_function,
)

def mamadisima_evaluation_function(state: TwoPlayerGameState) -> float:
    """Devuelve un valor dado por la ponderación de varios aspectos que afectan al juego. 
       En particular pondera: """

    my_tiles = 0
    opp_tiles = 0
    my_front_tiles = 0
    opp_front_tiles = 0
    p = 0.0
    c = 0.0
    l = 0.0
    m = 0.0
    f = 0.0
    d = 0.0
 
    X1 = [- 1 , - 1 , 0 , 1 , 1 , 1 , 0 , - 1 ]
    Y1 = [ 0 , 1 , 1 , 1 , 0 , - 1 , - 1 , - 1 ]
 
    V = [[ 20 , - 3 , 11 , 8 , 8 , 11 , - 3 , 20 ],[- 3 , - 7 , - 4 , 1 , 1 , - 4 , - 7 , - 3 ],
    [ 11 , - 4 , 2 , 2 , 2 , 2 , - 4 , 11 ],[ 8 , 1 , 2 , - 3 , - 3 , 2 , 1 , 8 ],
    [8 , 1 , 2 , - 3 , - 3 , 2 , 1 , 8 ],[ 11 , - 4 , 2 , 2 , 2 , 2 , - 4 , 11 ],
    [- 3 , - 7 , - 4 , 1 , 1 , - 4 , - 7 , - 3 ],[ 20 , - 3 , 11 , 8 , 8 , 11 , - 3 , 20 ]]
    
    # Diferencia de piezas, discos de frontera y cuadrados de disco
    for i in range(8):
        for j in range(8):
            if (i,j) in state.board:
                #print(state.board[(i,j)])
                if (state.board[(i,j)] == state.player1.label):
                    d += V[i][j]
                    my_tiles+=1
                elif (state.board[(i,j)] == state.player2.label):
                    d -= V[i][j]
                    opp_tiles+=1
            
                if (state.board[(i,j)] == state.player1.label or state.board[(i,j)] == state.player2.label):
                    for k in range(8):
                        x = i + X1[k]
                        y = j + Y1[k]
                        if (x,y) not in state.board:
                            if (x >= 0 and x < 8 and y >= 0 and y < 8):
                                if (state.board[(i,j)] == state.player1.label): my_front_tiles+=1
                                else: opp_front_tiles+=1
                                break
    
    if (my_tiles > opp_tiles):
        p = ( 100.0 * my_tiles)/(my_tiles + opp_tiles)
    elif ( my_tiles < opp_tiles):
        p = -( 100.0 * opp_tiles)/(my_tiles + opp_tiles)
    else: p = 0

    if (my_front_tiles > opp_front_tiles):
        f = -( 100.0 * my_front_tiles)/(my_front_tiles + opp_front_tiles)
    elif (my_front_tiles < opp_front_tiles):
        f = ( 100.0 * opp_front_tiles)/(my_front_tiles + opp_front_tiles)
    else: f = 0
    
    # Ocupación de esquina
    my_tiles = opp_tiles = 0
    if (0,0) in state.board:
        if (state.board[(0,0)] == state.player1.label): my_tiles+=1
        elif (state.board[(0,0)] == state.player2.label): opp_tiles+=1

    if (0,7) in state.board:
        if (state.board[(0,7)] == state.player1.label): my_tiles+=1
        elif (state.board[(0,7)] == state.player2.label): opp_tiles+=1

    if (7,0) in state.board:
        if (state.board[(7,0)] == state.player1.label): my_tiles+=1
        elif (state.board[(7,0)] == state.player2.label): opp_tiles+=1
    
    if (7,7) in state.board:
        if (state.board[(7,7)] == state.player1.label): my_tiles+=1
        elif (state.board[(7,7)] == state.player2.label): opp_tiles+=1

    c = 25 * (my_tiles - opp_tiles)

    
    
    '''
    // Cercanía de esquina
    my_tiles = opp_tiles = 0 ;
    if (state.board[ 0 ][ 0 ] == ' - ' ) {
    if (state.board[(0,1 ] == state.player1.label) my_tiles++;
    elif (state.board[(0,1 ] == state.player2.label) opp_tiles++;
    if (state.board[ 1 ][ 1 ] == state.player1.label) my_tiles++;
    elif (state.board[ 1 ][ 1 ] == state.player2.label) opp_tiles++;
    if (state.board[ 1 ][ 0 ] == state.player1.label) my_tiles++;
    elif (state.board[ 1 ][ 0 ] == state.player2.label) opp_tiles++;
    }
    if (state.board[ 0 ][ 7 ] == ' - ' ) {
    if (state.board[(0,6 ] == state.player1.label) my_tiles++;
    elif (state.board[(0,6 ] == state.player2.label) opp_tiles++;
    if (state.board[ 1 ][ 6 ] == state.player1.label) my_tiles++;
    elif (state.board[ 1 ][ 6 ] == state.player2.label) opp_tiles++;
    if (state.board[ 1 ][ 7 ] == state.player1.label) my_tiles++;
    elif (state.board[ 1 ][ 7 ] == state.player2.label) opp_tiles++;
    }
    if (state.board[ 7 ][ 0 ] == ' - ' ) {
    if (state.board[ 7 ][ 1 ] == state.player1.label) my_tiles++;
    elif (state.board[ 7 ][ 1 ] == state.player2.label) opp_tiles++;
    if (state.board[ 6 ][ 1 ] == state.player1.label) my_tiles++;
    elif (state.board[ 6 ][ 1 ] == state.player2.label) opp_tiles++;
    if (state.board[ 6 ][ 0 ] == state.player1.label) my_tiles++;
    elif (state.board[ 6 ][ 0 ] == state.player2.label) opp_tiles++;
    }
    if (state.board[ 7 ][ 7 ] == ' - ' ) {
    if (state.board[ 6 ][ 7 ] == state.player1.label) my_tiles++;
    elif (state.board[ 6 ][ 7 ] == state.player2.label) opp_tiles++;
    if (state.board[ 6 ][ 6 ] == state.player1.label) my_tiles++;
    elif (state.board[ 6 ][ 6 ] == state.player2.label) opp_tiles++;
    if (state.board[ 7 ][ 6 ] == state.player1.label) my_tiles++;
    elif (state.board[ 7 ][ 6 ] == state.player2.label) opp_tiles++;
    }
    l = - 12.5 * (my_tiles - opp_tiles);
    

    # Movilidad
    my_tiles = len(state.generate_successors(state))
    opp_tiles = len(state.generate_successors(state))
    if (my_tiles > opp_tiles):
        m = ( 100.0 * my_tiles)/(my_tiles + opp_tiles)
    elif ( my_tiles < opp_tiles):
        m = -( 100.0 * opp_tiles)/(my_tiles + opp_tiles)
    else: m = 0
    '''
    #puntaje ponderado final
    state_value = ( 10 * p) + ( 801.724 * c) + ( 382.026 * l) + ( 78.922 * m) + ( 74.396 * f) + ( 10 * d)

    return state_value

heuristica_mamadisima = Heuristic(
    name='Heuristic mamadisima',
    evaluation_function = mamadisima_evaluation_function,
)


