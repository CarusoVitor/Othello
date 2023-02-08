from multiprocessing.pool import ThreadPool
from typing import Tuple
from advsearch.othello.board import Board
from advsearch.othello.gamestate import GameState
from numpy import argmax

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
    best_move = (-1, -1) # sem movimentos por padrão
    legal_moves = state.legal_moves()
    pool = ThreadPool(len(legal_moves))

    # inicia uma thread pra cada sucessor
    moves = pool.starmap(min_move, [(state.next_state(successor), float("-inf"), float("inf"), 1) for successor in legal_moves])
    pool.close()
    pool.join()

    # desempacota os valores, considerando que as threads retornam os valores na ordem original passada pra elas,
    if len(moves) > 0:
        best_move = list(legal_moves)[argmax(moves)]
    return best_move

def max_move(state: GameState, alpha: float, beta: float, depth=0):
    if depth >= MAX_DEPTH or state.is_terminal():
        return state_evaluation(state)

    value = float("-inf")
    for successor in state.legal_moves():
        value = max(value, min_move(state.next_state(successor), alpha, beta, depth+1))
        alpha = max(alpha, value)
        if alpha >= beta:
            break
    return alpha


def min_move(state: GameState, alpha: float, beta: float, depth=0):
    if depth >= MAX_DEPTH or state.is_terminal():
        return state_evaluation(state)

    value = float("inf")
    for successor in state.legal_moves():
        value = min(value, max_move(state.next_state(successor), alpha, beta, depth+1))
        beta = min(beta, value)
        if beta <= alpha:
            break
    return beta


# Heuristicas baseadas em: https://courses.cs.washington.edu/courses/cse573/04au/Project/mini1/RUSSIA/Final_Paper.pdf
def coin_parity(state: GameState) -> float:
    if state.is_terminal():
        return 0.0

    max_player_sum : int = state.board.piece_count[state.player]
    min_player_sum : int = state.board.piece_count[Board.opponent(state.player)]

    if max_player_sum - min_player_sum == 0:
        return 0.0

    return 100 * (max_player_sum - min_player_sum)/(max_player_sum + min_player_sum)


def corners_captured(state: GameState) -> float:
    max_player_corners : int = 0
    min_player_corners : int = 0

    ul_corner = state.board.tiles[0][0]
    bl_corner = state.board.tiles[-1][0]
    ur_corner = state.board.tiles[0][-1]
    br_corner = state.board.tiles[-1][-1]

    if ul_corner == state.player:
        max_player_corners += 1
    elif ul_corner != state.board.EMPTY:
        min_player_corners += 1

    if bl_corner == state.player:
        max_player_corners += 1
    elif bl_corner != state.board.EMPTY:
        min_player_corners += 1

    if ur_corner == state.player:
        max_player_corners += 1
    elif ur_corner != state.board.EMPTY:
        min_player_corners += 1

    if br_corner == state.player:
        max_player_corners += 1
    elif br_corner != state.board.EMPTY:
        min_player_corners += 1
    
    if max_player_corners + min_player_corners == 0:
        return 0.0
    
    return 100 * (max_player_corners - min_player_corners)/(max_player_corners + min_player_corners)


def mobility(state: GameState):
    if state.is_terminal():
        return 0.0
    else:
        player_move_total = state.board.piece_count[state.player]
        opponent_move_total = state.board.piece_count[Board.opponent(state.player)]
        return 100 * (player_move_total - opponent_move_total)/(player_move_total + opponent_move_total)


def state_evaluation(state: GameState) -> float:
    return coin_parity(state)*0.3+mobility(state)*0.5+corners_captured(state)*0.2



if __name__ == "__main__":
    state = GameState(Board(), Board.BLACK)
    move = minimax(state)
    print(move)
