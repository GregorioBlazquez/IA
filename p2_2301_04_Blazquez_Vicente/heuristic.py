"""Heuristics to evaluate board.

    Authors:
        Fabiano Baroni <fabiano.baroni@uam.es>,
        Alejandro Bellogin <alejandro.bellogin@uam.es>
        Alberto Suárez <alberto.suarez@uam.es>

"""


from __future__ import annotations
from os import stat  # For Python 3.7

from typing import Callable, List, Sequence

import numpy as np

from reversi import Reversi, from_dictionary_to_array_board

from game import TwoPlayerGameState

import math

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

        assert isinstance(scores, (Sequence, np.ndarray))
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

def original_evaluation_function(state: TwoPlayerGameState) -> float:
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

    my_color=state.next_player.label
    if (my_color == 'B'):
        opp_color='W'
    else:
        opp_color='B'

    # Diferencia de piezas, discos de frontera y cuadrados de disco
    for i in range(1,9):
        for j in range(1,9):
            if (i,j) in state.board:
                if (state.board[(i,j)] == my_color):
                    d += V[i-1][j-1]
                    my_tiles+=1
                elif (state.board[(i,j)] == opp_color):
                    d -= V[i-1][j-1]
                    opp_tiles+=1

                if (state.board[(i,j)] == my_color or state.board[(i,j)] == opp_color):
                    for k in range(1,9):
                        x = i + X1[k-1]
                        y = j + Y1[k-1]
                        if (x,y) not in state.board:
                            if (x >= 0 and x < 8 and y >= 0 and y < 8):
                                if (state.board[(i,j)] == my_color): my_front_tiles+=1
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
    if (1,1) in state.board:
        if (state.board[(1,1)] == my_color):
            my_tiles+=1
        else: opp_tiles+=1

    if (1,8) in state.board:
        if (state.board[(1,8)] == my_color):
            my_tiles+=1
        else: opp_tiles+=1

    if (8,1) in state.board:
        if (state.board[(8,1)] == my_color):
            my_tiles+=1
        else: opp_tiles+=1
    
    if (8,8) in state.board:
        if (state.board[(8,8)] == my_color):
            my_tiles+=1
        else: opp_tiles+=1

    c = 25 * (my_tiles - opp_tiles)

    # Cercanía de esquina
    tablero=from_dictionary_to_array_board(state.board,8,8)

    my_tiles, opp_tiles = 0,0
    if (tablero[0][0] == '.' ):
        if (tablero[0][1] == my_color): my_tiles+=1
        elif (tablero[0][1] == opp_color): opp_tiles+=1
        if (tablero[1][1] == my_color): my_tiles+=1
        elif (tablero[1][1] == opp_color): opp_tiles+=1
        if (tablero[1][0] == my_color): my_tiles+=1
        elif (tablero[1][0] == opp_color): opp_tiles+=1
    if (tablero[ 0 ][ 7 ] == '.' ):
        if (tablero[0][6] == my_color): my_tiles+=1
        elif (tablero[0][6] == opp_color): opp_tiles+=1
        if (tablero[1][6] == my_color): my_tiles+=1
        elif (tablero[1][6] == opp_color): opp_tiles+=1
        if (tablero[1][7] == my_color): my_tiles+=1
        elif (tablero[1][7] == opp_color): opp_tiles+=1

    if (tablero[ 7 ][ 0 ] == '.' ):
        if (tablero[ 7 ][ 1 ] == my_color): my_tiles+=1
        elif (tablero[ 7 ][ 1 ] == opp_color): opp_tiles+=1
        if (tablero[ 6 ][ 1 ] == my_color): my_tiles+=1
        elif (tablero[ 6 ][ 1 ] == opp_color): opp_tiles+=1
        if (tablero[ 6 ][ 0 ] == my_color): my_tiles+=1
        elif (tablero[ 6 ][ 0 ] == opp_color): opp_tiles+=1
    
    if (tablero[ 7 ][ 7 ] == '.' ):
        if (tablero[ 6 ][ 7 ] == my_color): my_tiles+=1
        elif (tablero[ 6 ][ 7 ] == opp_color): opp_tiles+=1
        if (tablero[ 6 ][ 6 ] == my_color): my_tiles+=1
        elif (tablero[ 6 ][ 6 ] == opp_color): opp_tiles+=1
        if (tablero[ 7 ][ 6 ] == my_color): my_tiles+=1
        elif (tablero[ 7 ][ 6 ] == opp_color): opp_tiles+=1
    l = - 12.5 * (my_tiles - opp_tiles)
    

    # Movilidad
    m = state.game._choice_diff(state.board)
    if(state.next_player.label=='W'):
        m= -m  
    
    #puntaje ponderado final
    state_value = ( 10 * p) + ( 801.724 * c) + ( 382.026 * l) + ( 78.922 * m) + ( 74.396 * f) + ( 10 * d)

    if (state.is_player_max(state.next_player) is False):
        return -state_value

    return state_value


def finish_evaluation_function(state: TwoPlayerGameState) -> float:
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

    my_color=state.next_player.label
    if (my_color == 'B'):
        opp_color='W'
    else:
        opp_color='B'
    
    # Diferencia de piezas, discos de frontera y cuadrados de disco
    for i in range(1,9):
        for j in range(1,9):
            if (i,j) in state.board:
                if (state.board[(i,j)] == my_color):
                    d += V[i-1][j-1]
                    my_tiles+=1
                elif (state.board[(i,j)] == opp_color):
                    d -= V[i-1][j-1]
                    opp_tiles+=1
            
                if (state.board[(i,j)] == my_color or state.board[(i,j)] == opp_color):
                    for k in range(1,9):
                        x = i + X1[k-1]
                        y = j + Y1[k-1]
                        if (x,y) not in state.board:
                            if (x >= 0 and x < 8 and y >= 0 and y < 8):
                                if (state.board[(i,j)] == my_color): my_front_tiles+=1
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

    '''c = state.game._corner_diff(state.board)

    if(state.next_player.label=='W'):
        c= -c '''
    
    my_tiles = opp_tiles = 0
    if (1,1) in state.board:
        if (state.board[(1,1)] == my_color):
            my_tiles+=1
        else: opp_tiles+=1

    if (1,8) in state.board:
        if (state.board[(1,8)] == my_color):
            my_tiles+=1
        else: opp_tiles+=1

    if (8,1) in state.board:
        if (state.board[(8,1)] == my_color):
            my_tiles+=1
        else: opp_tiles+=1
    
    if (8,8) in state.board:
        if (state.board[(8,8)] == my_color):
            my_tiles+=1
        else: opp_tiles+=1

    c = 25 * (my_tiles - opp_tiles)

    # Cercanía de esquina
    tablero=from_dictionary_to_array_board(state.board,8,8)

    my_tiles, opp_tiles = 0,0
    if (tablero[0][0] == '.' ):
        if (tablero[0][1] == my_color): my_tiles+=1
        elif (tablero[0][1] == opp_color): opp_tiles+=1
        if (tablero[1][1] == my_color): my_tiles+=1
        elif (tablero[1][1] == opp_color): opp_tiles+=1
        if (tablero[1][0] == my_color): my_tiles+=1
        elif (tablero[1][0] == opp_color): opp_tiles+=1
    if (tablero[ 0 ][ 7 ] == '.' ):
        if (tablero[0][6] == my_color): my_tiles+=1
        elif (tablero[0][6] == opp_color): opp_tiles+=1
        if (tablero[1][6] == my_color): my_tiles+=1
        elif (tablero[1][6] == opp_color): opp_tiles+=1
        if (tablero[1][7] == my_color): my_tiles+=1
        elif (tablero[1][7] == opp_color): opp_tiles+=1

    if (tablero[ 7 ][ 0 ] == '.' ):
        if (tablero[ 7 ][ 1 ] == my_color): my_tiles+=1
        elif (tablero[ 7 ][ 1 ] == opp_color): opp_tiles+=1
        if (tablero[ 6 ][ 1 ] == my_color): my_tiles+=1
        elif (tablero[ 6 ][ 1 ] == opp_color): opp_tiles+=1
        if (tablero[ 6 ][ 0 ] == my_color): my_tiles+=1
        elif (tablero[ 6 ][ 0 ] == opp_color): opp_tiles+=1
    
    if (tablero[ 7 ][ 7 ] == '.' ):
        if (tablero[ 6 ][ 7 ] == my_color): my_tiles+=1
        elif (tablero[ 6 ][ 7 ] == opp_color): opp_tiles+=1
        if (tablero[ 6 ][ 6 ] == my_color): my_tiles+=1
        elif (tablero[ 6 ][ 6 ] == opp_color): opp_tiles+=1
        if (tablero[ 7 ][ 6 ] == my_color): my_tiles+=1
        elif (tablero[ 7 ][ 6 ] == opp_color): opp_tiles+=1
    l = - 12.5 * (my_tiles - opp_tiles)
    

    # Movilidad
    m = state.game._choice_diff(state.board)
    if(state.next_player.label=='W'):
        m=-m  
    
    finish=0
    if (len(state.board)%2==0):
        finish=100

    #puntaje ponderado final
    state_value = ( 10 * p) + ( 801.724 * c) + ( 382.026 * l) + ( 78.922 * m) + ( 74.396 * f) + ( 10 * d) + finish*500

    if (state.is_player_max(state.next_player) is False):
        return -state_value

    return state_value

def pesos_evaluation_function(state: TwoPlayerGameState) -> float:
    """Devuelve un valor dado por la ponderación de varios aspectos que afectan al juego. 
       En particular pondera: """
    d = 0
 
    V = [[ 4, -3, 2, 2, 2, 2, -3 , 4],
        [ -3, -4, -1, -1, -1, -1, -4, -3],
        [ 2, -1 ,1 , 0 , 0 , 1 , -1 , 2],
        [ 2, -1 , 0 , 1 , 1 , 0 , -1 , 2],
        [ 2, -1 , 0 , 1 , 1 , 0 , -1 , 2],
        [ 2, -1 , 1 , 0 , 0 , 1 , -1 , 2],
        [-3, -4 , -1 , -1 , -1 , -1 , -4, -3],
        [ 4, -3, 2, 2, 2, 2, -3, 4]]


    my_color=state.next_player.label

    if (my_color == 'B'):
        opp_color='W'
    else:
        opp_color='B'
    
    p=0
    # Diferencia de piezas teniendo en cuenta el peso del tablero
    for i in range(1,9):
        for j in range(1,9):
            if (i,j) in state.board:
                if (state.board[(i,j)] == my_color):
                    p+=1
                    d += V[i-1][j-1]
                elif (state.board[(i,j)] == opp_color):
                    p-=1
                    d -= V[i-1][j-1]

    state_value = d
    if (len(state.board)>=58):
        state_value+=p

    if (state.is_player_max(state.next_player) is False):
        return -state_value

    return state_value


def dynamic_evaluation_function(state: TwoPlayerGameState) -> float:
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

    #print(state.is_player_max(state.player1))

    my_color=state.next_player.label

    if (my_color == 'B'):
        opp_color='W'
    else:
        opp_color='B'
    
    total_d=0
    # Diferencia de piezas, discos de frontera y cuadrados de disco
    for i in range(1,9):
        for j in range(1,9):
            if (i,j) in state.board:
                #print(state.board[(i,j)])
                if (state.board[(i,j)] == my_color):
                    d += V[i-1][j-1]
                    total_d+=abs(V[i-1][j-1])
                    my_tiles+=1
                elif (state.board[(i,j)] == opp_color):
                    d -= V[i-1][j-1]
                    total_d+=abs(V[i-1][j-1])
                    opp_tiles+=1

                if (state.board[(i,j)] == my_color or state.board[(i,j)] == opp_color):
                    for k in range(1,9):
                        x = i + X1[k-1]
                        y = j + Y1[k-1]
                        if (x,y) not in state.board:
                            if (x >= 0 and x < 8 and y >= 0 and y < 8):
                                if (state.board[(i,j)] == my_color): my_front_tiles+=1
                                else: opp_front_tiles+=1
                                break
    
    d=100*d/total_d

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
    c = state.game._corner_diff(state.board)
    if(state.next_player.label=='W'):
        c= -c 

     
    # Cercanía de esquina
    tablero=from_dictionary_to_array_board(state.board,8,8)   
    my_tiles, opp_tiles = 0,0
    if (tablero[0][0] == '.' ):
        if (tablero[0][1] == my_color): my_tiles+=1
        elif (tablero[0][1] == opp_color): opp_tiles+=1
        if (tablero[1][1] == my_color): my_tiles+=1
        elif (tablero[1][1] == opp_color): opp_tiles+=1
        if (tablero[1][0] == my_color): my_tiles+=1
        elif (tablero[1][0] == opp_color): opp_tiles+=1
    if (tablero[ 0 ][ 7 ] == '.' ):
        if (tablero[0][6] == my_color): my_tiles+=1
        elif (tablero[0][6] == opp_color): opp_tiles+=1
        if (tablero[1][6] == my_color): my_tiles+=1
        elif (tablero[1][6] == opp_color): opp_tiles+=1
        if (tablero[1][7] == my_color): my_tiles+=1
        elif (tablero[1][7] == opp_color): opp_tiles+=1

    if (tablero[ 7 ][ 0 ] == '.' ):
        if (tablero[ 7 ][ 1 ] == my_color): my_tiles+=1
        elif (tablero[ 7 ][ 1 ] == opp_color): opp_tiles+=1
        if (tablero[ 6 ][ 1 ] == my_color): my_tiles+=1
        elif (tablero[ 6 ][ 1 ] == opp_color): opp_tiles+=1
        if (tablero[ 6 ][ 0 ] == my_color): my_tiles+=1
        elif (tablero[ 6 ][ 0 ] == opp_color): opp_tiles+=1
    
    if (tablero[ 7 ][ 7 ] == '.' ):
        if (tablero[ 6 ][ 7 ] == my_color): my_tiles+=1
        elif (tablero[ 6 ][ 7 ] == opp_color): opp_tiles+=1
        if (tablero[ 6 ][ 6 ] == my_color): my_tiles+=1
        elif (tablero[ 6 ][ 6 ] == opp_color): opp_tiles+=1
        if (tablero[ 7 ][ 6 ] == my_color): my_tiles+=1
        elif (tablero[ 7 ][ 6 ] == opp_color): opp_tiles+=1
    if ((my_tiles + opp_tiles)!=0):
        l = 100 * (my_tiles - opp_tiles)/(my_tiles + opp_tiles)
    else: l=0
    
    # Movilidad
    m = state.game._choice_diff(state.board)
    if(state.next_player.label=='W'):
        m= -m 

    #calculo exponencial para la ponderacion de numero de fichas que come
    x=len(state.board)
    f_p=0.00010178124*math.exp(0.2206950568365*x)
    f_m=100*math.exp(-(x-30)*(x-30)/10)
    print("VALORES IMPORTANTES:")
    print("x="+str(x)+"/nf_p="+str(f_p)+"/nf_m="+str(f_m))
    #puntaje ponderado final
    state_value = f_p*p + 90*c + 40*l + f_m*m + 50*f + 50*d
    print("VALOR GLOBAL")
    print("f_p*p="+str(f_p*p)+"/n90*c="+str(90*c)+"/n40*l="+str(40*l)+"/nf_m*m="+str(f_m*m)+"/n50*f="+str(50*f)+"/n50*d="+str(50*d))


    if (state.is_player_max(state.next_player) is False):
        print(str(-state_value))
        return -state_value

    print(str(state_value))
    return state_value

heuristica_original = Heuristic(
    name='Heuristic original',
    evaluation_function = original_evaluation_function,
)

heuristica_pesos = Heuristic(
    name='Heuristic pesos',
    evaluation_function = pesos_evaluation_function,
)

heuristica_dynamic = Heuristic(
    name='Heuristic dinámica',
    evaluation_function = dynamic_evaluation_function,
)

heuristica_finish = Heuristic(
    name='Heuristic finish',
    evaluation_function = finish_evaluation_function,
)