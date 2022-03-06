import time
from game import (
    TwoPlayerGameState,
)
from tournament import (
    StudentHeuristic,
)

class SolutionMamadisimo(StudentHeuristic):
  def get_name(self) -> str:
    return "Mamadisimo"
  def evaluation_function(self, state: TwoPlayerGameState) -> float:
    """Devuelve un valor dado por la ponderación de varios aspectos que afectan al juego. 
       En particular pondera: """

    my_tiles, opp_tiles, my_front_tiles, opp_front_tiles = 0,0,0,0
    p, c, l, m, f, d = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
 
    X1 = [- 1 , - 1 , 0 , 1 , 1 , 1 , 0 , - 1 ]
    Y1 = [ 0 , 1 , 1 , 1 , 0 , - 1 , - 1 , - 1 ]
 
    V = [[ 20 , - 3 , 11 , 8 , 8 , 11 , - 3 , 20 ],[- 3 , - 7 , - 4 , 1 , 1 , - 4 , - 7 , - 3 ],
    [ 11 , - 4 , 2 , 2 , 2 , 2 , - 4 , 11 ],[ 8 , 1 , 2 , - 3 , - 3 , 2 , 1 , 8 ],
    [8 , 1 , 2 , - 3 , - 3 , 2 , 1 , 8 ],[ 11 , - 4 , 2 , 2 , 2 , 2 , - 4 , 11 ],
    [- 3 , - 7 , - 4 , 1 , 1 , - 4 , - 7 , - 3 ],[ 20 , - 3 , 11 , 8 , 8 , 11 , - 3 , 20 ]]
    '''
    // Diferencia de piezas, discos de frontera y cuadrados de disco
    for i in range(8):
      for (j= 0 ; j< 8 ; j++) {
    if (cuadrícula[i][j] == mi_color) {
    d += V[i][j];
    mis_fichas++;
    } else  if (cuadrícula[i][j] == color_opp) {
    d -= V[i][j];
    opp_tiles++;
    }
    if (cuadrícula[i][j] != ' - ' ) {
    para (k= 0 ; k< 8 ; k++) {
    x = yo + X1[k]; y = j + Y1[k];
    if (x >= 0 && x < 8 && y >= 0 && y < 8 && rejilla[x][y] == ' - ' ) {
    if (grid[i][j] == my_color) my_front_tiles++;
    más opp_front_tiles++;
    romper ;
    }
    }
    }
    }
    if (my_tiles > opp_tiles)
    p = ( 100.0 * my_tiles)/(my_tiles + opp_tiles);
    si no ( my_tiles < opp_tiles)
    p = -( 100.0 * opp_tiles)/(my_tiles + opp_tiles);
    si no p = 0 ;

    if (my_front_tiles > opp_front_tiles)
    f = -( 100.0 * my_front_tiles)/(my_front_tiles + opp_front_tiles);
    otra cosa  si (my_front_tiles < opp_front_tiles)
    f = ( 100.0 * opp_front_tiles)/(my_front_tiles + opp_front_tiles);
    si no f = 0 ;

    // Ocupación de esquina
    my_tiles = opp_tiles = 0 ;
    if (grid[ 0 ][ 0 ] == my_color) my_tiles++;
    else  if (grid[ 0 ][ 0 ] == opp_color) opp_tiles++;
    if (grid[ 0 ][ 7 ] == my_color) my_tiles++;
    else  if (grid[ 0 ][ 7 ] == opp_color) opp_tiles++;
    if (grid[ 7 ][ 0 ] == my_color) my_tiles++;
    else  if (grid[ 7 ][ 0 ] == opp_color) opp_tiles++;
    if (grid[ 7 ][ 7 ] == my_color) my_tiles++;
    else  if (grid[ 7 ][ 7 ] == opp_color) opp_tiles++;
    c = 25 * (my_tiles - opp_tiles);

    // Cercanía de esquina
    my_tiles = opp_tiles = 0 ;
    si (cuadrícula[ 0 ][ 0 ] == ' - ' ) {
    if (grid[ 0 ][ 1 ] == my_color) my_tiles++;
    else  if (grid[ 0 ][ 1 ] == opp_color) opp_tiles++;
    if (grid[ 1 ][ 1 ] == my_color) my_tiles++;
    else  if (grid[ 1 ][ 1 ] == opp_color) opp_tiles++;
    if (grid[ 1 ][ 0 ] == my_color) my_tiles++;
    else  if (grid[ 1 ][ 0 ] == opp_color) opp_tiles++;
    }
    si (cuadrícula[ 0 ][ 7 ] == ' - ' ) {
    if (grid[ 0 ][ 6 ] == my_color) my_tiles++;
    else  if (grid[ 0 ][ 6 ] == opp_color) opp_tiles++;
    if (grid[ 1 ][ 6 ] == my_color) my_tiles++;
    else  if (grid[ 1 ][ 6 ] == opp_color) opp_tiles++;
    if (grid[ 1 ][ 7 ] == my_color) my_tiles++;
    else  if (grid[ 1 ][ 7 ] == opp_color) opp_tiles++;
    }
    si (cuadrícula[ 7 ][ 0 ] == ' - ' ) {
    if (grid[ 7 ][ 1 ] == my_color) my_tiles++;
    else  if (grid[ 7 ][ 1 ] == opp_color) opp_tiles++;
    if (grid[ 6 ][ 1 ] == my_color) my_tiles++;
    else  if (grid[ 6 ][ 1 ] == opp_color) opp_tiles++;
    if (grid[ 6 ][ 0 ] == my_color) my_tiles++;
    else  if (grid[ 6 ][ 0 ] == opp_color) opp_tiles++;
    }
    si (cuadrícula[ 7 ][ 7 ] == ' - ' ) {
    if (grid[ 6 ][ 7 ] == my_color) my_tiles++;
    else  if (grid[ 6 ][ 7 ] == opp_color) opp_tiles++;
    if (grid[ 6 ][ 6 ] == my_color) my_tiles++;
    else  if (grid[ 6 ][ 6 ] == opp_color) opp_tiles++;
    if (grid[ 7 ][ 6 ] == my_color) my_tiles++;
    else  if (grid[ 7 ][ 6 ] == opp_color) opp_tiles++;
    }
    l = - 12.5 * (my_tiles - opp_tiles);

    // Movilidad
    my_tiles = num_valid_moves (my_color, opp_color, grid);
    opp_tiles = num_valid_moves (opp_color, my_color, grid);
    if (my_tiles > opp_tiles)
    m = ( 100.0 * my_tiles)/(my_tiles + opp_tiles);
    si no ( my_tiles < opp_tiles)
    m = -( 100.0 * opp_tiles)/(my_tiles + opp_tiles);
    si no m = 0 ;
    '''
    #puntaje ponderado final
    state_value = ( 10 * p) + ( 801.724 * c) + ( 382.026 * l) + ( 78.922 * m) + ( 74.396 * f) + ( 10 * d);

    return state_value

class Solution2(StudentHeuristic):
  def get_name(self) -> str:
    return "solution2"
  def evaluation_function(self, state: TwoPlayerGameState) -> float:
    print("sleeping")
    time.sleep(3)
    print("awake")
    return 2
