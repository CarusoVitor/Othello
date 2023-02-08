from multiprocessing.pool import ThreadPool
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
    global AGENT_COLOR 
    AGENT_COLOR = state.player
    move = minimax(state)
    return move


def minimax(state: GameState) -> Tuple[int, int]:
    best_move = (-1, -1) # sem movimentos por padrão
    legal_moves = state.legal_moves()
    pool = ThreadPool(len(legal_moves))

    # inicia uma thread pra cada sucessor
    moves_values = pool.starmap(min_move, [(state.next_state(successor), float("-inf"), float("inf"), 1) for successor in legal_moves])
    pool.close()
    pool.join()

    max_value = float("-inf")
    # desempacota os valores, considerando que as threads retornam os valores na ordem original passada pra elas,
    for i, move_value in enumerate(moves_values):
        if move_value > max_value:
            max_value = move_value
            best_move = i

    return list(legal_moves)[best_move]

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
    max_player_sum : int = state.board.num_pieces(AGENT_COLOR)
    min_player_sum : int = state.board.num_pieces(Board.opponent(AGENT_COLOR))

    if max_player_sum - min_player_sum == 0:
        return 0.0

    return 100 * (max_player_sum - min_player_sum)/(max_player_sum + min_player_sum)


def corners_captured(state: GameState) -> float:
    max_player_corners : int = 0
    min_player_corners : int = 0
    common_player_corners : int = 0

    # Captured corners
    ul_corner = state.board.tiles[0][0]
    bl_corner = state.board.tiles[-1][0]
    ur_corner = state.board.tiles[0][-1]
    br_corner = state.board.tiles[-1][-1]

    if ul_corner == AGENT_COLOR:
        max_player_corners += 1
    elif ul_corner == Board.opponent(AGENT_COLOR):
        min_player_corners += 1

    if bl_corner == AGENT_COLOR:
        max_player_corners += 1
    elif bl_corner == Board.opponent(AGENT_COLOR):
        min_player_corners += 1

    if ur_corner == AGENT_COLOR:
        max_player_corners += 1
    elif ur_corner == Board.opponent(AGENT_COLOR):
        min_player_corners += 1

    if br_corner == AGENT_COLOR:
        max_player_corners += 1
    elif br_corner == Board.opponent(AGENT_COLOR):
        min_player_corners += 1
    
    # Potencial corners
    max_legal_moves : set = state.board.legal_moves(AGENT_COLOR)
    min_legal_moves : set = state.board.legal_moves(Board.opponent(AGENT_COLOR))
    
    if (0, 0) in max_legal_moves and (0, 0) in min_legal_moves:
        common_player_corners += 3
    if (0, 0) in max_legal_moves:
        max_player_corners += 1
    if (0, 0) in min_legal_moves:
        min_player_corners += 3

    if (7, 0) in max_legal_moves and (7, 0) in min_legal_moves:
        common_player_corners += 3
    if (7, 0) in max_legal_moves:
        max_player_corners += 1
    if (7, 0) in min_legal_moves:
        min_player_corners += 3
        
    if (0, 7) in max_legal_moves and (0, 7) in min_legal_moves:
        common_player_corners += 3
    if (0, 7) in max_legal_moves:
        max_player_corners += 1
    if (0, 7) in min_legal_moves:
        min_player_corners += 3
        
    if (7, 7) in max_legal_moves and (7, 7) in min_legal_moves:
        common_player_corners += 3
    if (7, 7) in max_legal_moves:
        max_player_corners += 1
    if (7, 7) in min_legal_moves:
        min_player_corners += 3
    
    numerator = max_player_corners - min_player_corners - common_player_corners
    denominator = max_player_corners + min_player_corners + common_player_corners
    
    if denominator == 0:
        return 0.0
    
    return 100 * numerator/denominator


def mobility(state: GameState):
    if state.is_terminal():
        return 0.0
    else:
        player_move_total : int = len(state.board.legal_moves(AGENT_COLOR))
        opponent_move_total : int = len(state.board.legal_moves(Board.opponent(AGENT_COLOR)))
        return 100 * (player_move_total - opponent_move_total)/(player_move_total + opponent_move_total)


def state_evaluation(state: GameState) -> float:
    # Estimate game progress in a range from [0, 10]
    game_progress = 100 * (1 - state.board.num_pieces(Board.EMPTY)/64)
    if game_progress > 90:
        coin_parity_w = 0.9
        mobility_w = 0.0
        corners_w = 0.1
    elif game_progress > 75:
        coin_parity_w = 0.4
        mobility_w = 0.1
        corners_w = 0.5
    else:
        coin_parity_w = 0.2
        mobility_w = 0.6
        corners_w = 0.2
    
    return coin_parity(state) * coin_parity_w + mobility(state) * mobility_w + corners_captured(state)*corners_w