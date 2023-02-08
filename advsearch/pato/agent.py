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
    AGENT_COLOR =  state.player
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
        return __mixed_heuristic(state)

    value = float("-inf")
    for successor in state.legal_moves():
        value = max(value, min_move(state.next_state(successor), alpha, beta, depth+1))
        alpha = max(alpha, value)
        if alpha >= beta:
            break
    return alpha


def min_move(state: GameState, alpha: float, beta: float, depth=0):
    if depth >= MAX_DEPTH or state.is_terminal():
        return __mixed_heuristic(state)

    value = float("inf")
    for successor in state.legal_moves():
        value = min(value, max_move(state.next_state(successor), alpha, beta, depth+1))
        beta = min(beta, value)
        if beta <= alpha:
            break
    return beta

def __simple_points_heuristic(state: GameState) -> int:
    """
    Cálcula a heuristíca simplesmente pela quantidade de peças do jogador
    contra a quantidade de peças do inimigo.
    """
    black_count = 0
    white_count = 0
    for tile in state.board.tiles:
        for piece in tile:
            if piece == Board.BLACK:
                black_count += 1
            elif piece == Board.WHITE:
                white_count += 1

    result = black_count - white_count

    return result if AGENT_COLOR == Board.BLACK else -result

def __mobility_heuristic(state: GameState):
    if state.is_terminal():
        return 0.0
    else:
        player_move_total : int = len(state.board.legal_moves(AGENT_COLOR))
        opponent_move_total : int = len(state.board.legal_moves(Board.opponent(AGENT_COLOR)))
        return 100 * (player_move_total - opponent_move_total)/(player_move_total + opponent_move_total)


__POINT_MAP = [
    [120, -20, 20, 5, 5, 20, -20, 120],
    [-20, -40, -5, -5, -5, -5, -40, -20],
    [20, -5, 15, 3, 3, 15, -5, 20],
    [5, -5, 3, 3, 3, 3, -5, 5],
    [5, -5, 3, 3, 3, 3, -5, 5],
    [20, -5, 15, 3, 3, 15, -5, 20],
    [-20, -40, -5, -5, -5, -5, -40, -20],
    [120, -20, 20, 5, 5, 20, -20, 120],
]


def __point_map_heuristic(state: GameState):
    player_points = 0
    enemy_points = 0
    for x, tile in enumerate(state.board.tiles):
        for y, piece in enumerate(tile):
            if piece == AGENT_COLOR:
                player_points += __POINT_MAP[x][y]
            elif piece == Board.opponent(AGENT_COLOR):
                enemy_points += __POINT_MAP[x][y]

    return player_points - enemy_points


def __mixed_heuristic(state: GameState) -> int:
    if state.is_terminal():
        return __simple_points_heuristic(state)

    point_map_heuristic_result = __point_map_heuristic(state)
    mobility_heuristic_result = __mobility_heuristic(state)
    return point_map_heuristic_result * 0.4 + mobility_heuristic_result * 0.6