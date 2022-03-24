import math

from game import (
    TwoPlayerGameState,
)
from tournament import (
    StudentHeuristic,
)
from reversi import (
    from_dictionary_to_array_board
)

class SolutionMamadisimo_Original(StudentHeuristic):
  def get_name(self) -> str:
    return "Mamadisimo_Original"
  def evaluation_function(self, state: TwoPlayerGameState) -> float:
    """
    Devuelve un valor dado por la ponderación de varios aspectos que afectan al juego. 
    En particular pondera: el numero de fichas (p), la ocupacion de esquinas (c), la 
    ocupación de las posiciones más cercanas a las esquinas (l), la libertad de movimientos
    o movilidad (m), la situcaion de las fichas de cada jugador respecto al rival, es decir,
    si estan rodeadas por fichas rivales tienen una situacion desfavorable (f) y una 
    valoracion de las posiciones del tablero dandole a cada posicion un valor estrategico (d).
    """

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

    my_color=state.player1.label
    opp_color=state.player2.label

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
    c = state.game._corner_diff(state.board)

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
    
    #puntaje ponderado final
    state_value = ( 10 * p) + ( 801.724 * c) + ( 382.026 * l) + ( 78.922 * m) + ( 74.396 * f) + ( 10 * d)

    if ((state.is_player_max(state.player1) and (state.next_player.label=='W'))
    or (not state.is_player_max(state.player2) and (state.next_player.label=='B'))):
        return state_value

    return -state_value


class SolutionMamadisimo_Pesos(StudentHeuristic):
  def get_name(self) -> str:
    return "Mamadisimo_Pesos"
  def evaluation_function(self, state: TwoPlayerGameState) -> float:
    """
    Devuelve una valoracion de las posiciones del tablero dandole a cada posicion un valor 
    estrategico y en las ultimas jugadas tiene tambien en cuenta el numero de fichas que come
    para tratar de comer todo lo posible en las ultimas jugadas.
    """
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

class SolutionMamadisimo_Dynamic(StudentHeuristic):
  def get_name(self) -> str:
    return "Mamadisimo_Dynamic"
  def evaluation_function(self, state: TwoPlayerGameState) -> float:
    """
    Devuelve un valor dado por la ponderación dinamica de varios aspectos que afectan al juego. 
    En particular pondera: el numero de fichas (p), la ocupacion de esquinas (c), la libertad 
    de movimientos o movilidad (m), y una valoracion de las posiciones del tablero dandole a 
    cada posicion un valor estrategico (d).

    La ponderacion dinamica consiste en:
     -no valorar el numero de fichas que comemos hasta el final de la partida cuando adquieren
     gran importancia (para esto utilizamos una funcion exponencial).
     -valorar la movilidad de las fichas de la partida a mitad de partida y no al principio y 
     al final (para esto utilizamos una funcion normal)
     -valorar estaticamente la ocupacion de esquinas y de las posiciones del tablero.
    """

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

    my_color=state.player1.label
    opp_color=state.player2.label
    
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
    
    # Ocupación de esquina
    c = state.game._corner_diff(state.board)

     
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

    # Calculo exponencial y normal para la ponderacion 
    # de numero de fichas que come y de la movilidad
    x=len(state.board)
    f_p=0.00010178124*math.exp(0.2206950568365*x)
    f_m=100*math.exp(-(x-30)*(x-30)/400)
    state_value = f_p*p + 90*c + f_m*m + 50*d

    if ((state.is_player_max(state.player1) and (state.next_player.label=='W'))
    or (not state.is_player_max(state.player2) and (state.next_player.label=='B'))):
        return state_value

    return -state_value