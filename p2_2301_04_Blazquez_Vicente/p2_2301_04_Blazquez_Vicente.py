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
    
    # Diferencia de piezas, discos de frontera y cuadrados de disco
    for i in range(1,9):
        for j in range(1,9):
            if (i,j) in state.board:
                #print(state.board[(i,j)])
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


    #print(state.board)
    
    # Ocupación de esquina
    my_tiles = opp_tiles = 0
    if (1,1) in state.board:
        if (state.board[(1,1)] == my_color):
            #print('ESQUINA1')
            my_tiles+=1
        else: opp_tiles+=1

    if (1,8) in state.board:
        if (state.board[(1,8)] == my_color):
            #print('ESQUINA2')
            my_tiles+=1
        else: opp_tiles+=1

    if (8,1) in state.board:
        if (state.board[(8,1)] == my_color):
            #print('ESQUINA3')
            my_tiles+=1
        else: opp_tiles+=1
    
    if (8,8) in state.board:
        if (state.board[(8,8)] == my_color):
            #print('ESQUINA4')
            my_tiles+=1
        else: opp_tiles+=1

    c = 25 * (my_tiles - opp_tiles)
    
    tablero=from_dictionary_to_array_board(state.board,8,8)

    
    # Cercanía de esquina
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
    '''
    # Movilidad
    my_tiles = len(state.game.generate_successors(state))
    opp_tiles = len(state.game.generate_successors(state))
    if (my_tiles > opp_tiles):
        m = ( 100.0 * my_tiles)/(my_tiles + opp_tiles)
    elif ( my_tiles < opp_tiles):
        m = -( 100.0 * opp_tiles)/(my_tiles + opp_tiles)
    else: m = 0
    '''
    #print("Ocupación de esquinas: "+str(801.724*c))
    #puntaje ponderado final
    state_value = ( 10 * p) + ( 801.724 * c) + ( 382.026 * l) + ( 78.922 * m) + ( 74.396 * f) + ( 10 * d)
    #state_value = 100000 * c
    
    '''print("Next Player Max: "+str(state.is_player_max(state.next_player)))
    print("Next Player Label: "+str(my_color))'''

    if (state.is_player_max(state.next_player) is False):
        # print("Negativo")
        return -state_value

    return state_value

class SolutionMamadisimo_Corners(StudentHeuristic):
  def get_name(self) -> str:
    return "Mamadisimo_Corners"
  def evaluation_function(self, state: TwoPlayerGameState) -> float:
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
    
    # Diferencia de piezas, discos de frontera y cuadrados de disco
    for i in range(1,9):
        for j in range(1,9):
            if (i,j) in state.board:
                #print(state.board[(i,j)])
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


    #print(state.board)
    
    # Ocupación de esquina
    my_tiles = opp_tiles = 0
    if (1,1) in state.board:
        if (state.board[(1,1)] == my_color):
            #print('ESQUINA1')
            my_tiles+=1
        else: opp_tiles+=1

    if (1,8) in state.board:
        if (state.board[(1,8)] == my_color):
            #print('ESQUINA2')
            my_tiles+=1
        else: opp_tiles+=1

    if (8,1) in state.board:
        if (state.board[(8,1)] == my_color):
            #print('ESQUINA3')
            my_tiles+=1
        else: opp_tiles+=1
    
    if (8,8) in state.board:
        if (state.board[(8,8)] == my_color):
            #print('ESQUINA4')
            my_tiles+=1
        else: opp_tiles+=1

    c = 25 * (my_tiles - opp_tiles)
    
    tablero=from_dictionary_to_array_board(state.board,8,8)

    
    # Cercanía de esquina
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
    '''
    # Movilidad
    my_tiles = len(state.game.generate_successors(state))
    opp_tiles = len(state.game.generate_successors(state))
    if (my_tiles > opp_tiles):
        m = ( 100.0 * my_tiles)/(my_tiles + opp_tiles)
    elif ( my_tiles < opp_tiles):
        m = -( 100.0 * opp_tiles)/(my_tiles + opp_tiles)
    else: m = 0
    '''
    #print("Ocupación de esquinas: "+str(801.724*c))
    #puntaje ponderado final
    state_value = ( 10 * p) + ( 10000 * c) + ( 382.026 * l) + ( 78.922 * m) + ( 74.396 * f) + ( 10 * d)
    #state_value = 100000 * c
    
    '''print("Next Player Max: "+str(state.is_player_max(state.next_player)))
    print("Next Player Label: "+str(my_color))'''

    if (state.is_player_max(state.next_player) is False):
        # print("Negativo")
        return -state_value

    return state_value


class SolutionMamadisimo_Movilidad(StudentHeuristic):
  def get_name(self) -> str:
    return "Mamadisimo_Movilidad"
  def evaluation_function(self, state: TwoPlayerGameState) -> float:
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
    
    # Diferencia de piezas, discos de frontera y cuadrados de disco
    for i in range(1,9):
        for j in range(1,9):
            if (i,j) in state.board:
                #print(state.board[(i,j)])
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


    #print(state.board)
    
    # Ocupación de esquina
    my_tiles = opp_tiles = 0
    if (1,1) in state.board:
        if (state.board[(1,1)] == my_color):
            #print('ESQUINA1')
            my_tiles+=1
        else: opp_tiles+=1

    if (1,8) in state.board:
        if (state.board[(1,8)] == my_color):
            #print('ESQUINA2')
            my_tiles+=1
        else: opp_tiles+=1

    if (8,1) in state.board:
        if (state.board[(8,1)] == my_color):
            #print('ESQUINA3')
            my_tiles+=1
        else: opp_tiles+=1
    
    if (8,8) in state.board:
        if (state.board[(8,8)] == my_color):
            #print('ESQUINA4')
            my_tiles+=1
        else: opp_tiles+=1

    c = 25 * (my_tiles - opp_tiles)
    
    tablero=from_dictionary_to_array_board(state.board,8,8)

    
    # Cercanía de esquina
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
    my_tiles = len(state.game.generate_successors(state))
    opp_tiles = len(state.game.generate_successors(state))
    if (my_tiles > opp_tiles):
        m = ( 100.0 * my_tiles)/(my_tiles + opp_tiles)
    elif ( my_tiles < opp_tiles):
        m = -( 100.0 * opp_tiles)/(my_tiles + opp_tiles)
    else: m = 0

    #print("Ocupación de esquinas: "+str(801.724*c))
    #puntaje ponderado final
    state_value = ( 10 * p) + ( 801.724 * c) + ( 382.026 * l) + ( 78.922 * m) + ( 74.396 * f) + ( 10 * d)
    #state_value = 100000 * c
    
    '''print("Next Player Max: "+str(state.is_player_max(state.next_player)))
    print("Next Player Label: "+str(my_color))'''

    if (state.is_player_max(state.next_player) is False):
        # print("Negativo")
        return -state_value

    return state_value
