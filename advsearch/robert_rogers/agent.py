import random
from typing import Tuple
from advsearch.othello.board import Board

from advsearch.othello.gamestate import GameState

# Voce pode criar funcoes auxiliares neste arquivo
# e tambem modulos auxiliares neste pacote.
#
# Nao esqueca de renomear 'your_agent' com o nome
# do seu agente.

MAX_DEPTH = 4

def make_move(state: GameState) -> Tuple[int, int]:
    """
    Returns an Othello move
    :param state: state to make the move
    :return: (int, int) tuple with x, y coordinates of the move (remember: 0 is the first row/column)
    """
    # o codigo abaixo apenas retorna um movimento aleatorio valido para
    # a primeira jogada com as pretas.
    # Remova-o e coloque a sua implementacao da poda alpha-beta
    move = minimax(state)
    return move


def minimax(state: GameState) -> Tuple[int, int]:
    alpha = float("-inf")
    beta = float("inf")

    best_move = (-1, -1) # sem movimentos por padrão
    max_value = float("-inf")

    if len(state.legal_moves()) > 0:
        for successor in state.legal_moves():
            # chama o min para cada sucessor, inicializando aqui o primeiro max
            # assim é possível manter o track de qual sucessor possui o maior valor
            value_max_move = min_move(state.next_state(successor), alpha, beta)
            if value_max_move > max_value:
                max_value = value_max_move
                best_move = successor

    return best_move


def max_move(state: GameState, alpha: float, beta: float, depth=0):
    if depth >= MAX_DEPTH or state.is_terminal():
        return coin_parity(state)

    value = float("-inf")
    for successor in state.legal_moves():
        value = max(value, min_move(state.next_state(successor), alpha, beta, depth+1))
        alpha = max(alpha, value)
        if alpha >= beta:
            break
    return alpha


def min_move(state: GameState, alpha: float, beta: float, depth=0):
    if depth >= MAX_DEPTH or state.is_terminal():
        return coin_parity(state)

    value = float("inf")
    for successor in state.legal_moves():
        value = min(value, max_move(state.next_state(successor), alpha, beta, depth + 1))
        beta = min(beta, value)
        if beta <= alpha:
            break
    return beta


# Heuristicas baseadas em: https://courses.cs.washington.edu/courses/cse573/04au/Project/mini1/RUSSIA/Final_Paper.pdf
def coin_parity(state: GameState) -> float:
    max_player_sum : int = 0
    min_player_sum : int = 0
    
    for row in state.board.tiles:
        for tile in row:
            if tile == state.player:
                max_player_sum += 1
            elif tile != state.board.EMPTY:
                min_player_sum += 1
                
    return 100 * (max_player_sum - min_player_sum)/(max_player_sum + min_player_sum)




if __name__ == "__main__":
    state = GameState(Board(), Board.BLACK)
    move = minimax(state)
    print(move)
