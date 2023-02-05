import random
from typing import Tuple

from ..othello.gamestate import GameState

# Voce pode criar funcoes auxiliares neste arquivo
# e tambem modulos auxiliares neste pacote.
#
# Nao esqueca de renomear 'your_agent' com o nome
# do seu agente.

def make_move(state: GameState) -> Tuple[int, int]:
    """
    Returns an Othello move
    :param state: state to make the move
    :return: (int, int) tuple with x, y coordinates of the move (remember: 0 is the first row/column)
    """
    # o codigo abaixo apenas retorna um movimento aleatorio valido para
    # a primeira jogada com as pretas.
    # Remova-o e coloque a sua implementacao da poda alpha-beta
    return random.choice([(2, 3), (4, 5), (5, 4), (3, 2)])

### Heuristicas baseadas em: https://courses.cs.washington.edu/courses/cse573/04au/Project/mini1/RUSSIA/Final_Paper.pdf ###
def coin_parity(state: GameState) -> float:
    max_player_sum : int = 0
    min_player_sum : int = 0
    
    for row in state.board.tiles:
        for tile in row:
            if tile == state.player:
                max_player_sum =+ 1
            elif tile != state.board.EMPTY:
                min_player_sum =+ 1
                
    return 100 * (max_player_sum - min_player_sum)/(max_player_sum + min_player_sum)