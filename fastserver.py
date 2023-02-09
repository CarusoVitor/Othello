from server import Server
import os
import time
import argparse
import datetime
from tqdm import tqdm
from typing import NamedTuple
import matplotlib.pyplot as plt
from advsearch.othello.board import Board
from advsearch.othello.gamestate import GameState
import advsearch.timer as timer

class MatchData(NamedTuple):
    match_status : int
    p1_score : int
    p2_score : int
    match_time : float
    elapsed_avg : int
    disqualified : bool

    def __str__(self) -> str:
        if self.match_status == 0:
            status = 'P1 WINS'
        elif self.match_status == 1:
            status = 'P2 WINS'
        else:
            status = 'DRAW'

        if self.disqualified:
            status += ' (DISQUALIFICATION)'

        return f'{status} - p1: {self.p1_score} p2: {self.p2_score} time: {str(self.match_time)} avg_time: {self.elapsed_avg}'

# Server sem prints e mais funcionalidades para simulação
# de múltiplas partidas. Não dá tempo adicional a jogador humano
class FastServer(Server):

    def __init__(self, p1_dir, p2_dir, delay, output, pace=0, matches=1):

        p1_module = os.path.normpath(p1_dir).replace(os.sep, '.')
        p2_module = os.path.normpath(p2_dir).replace(os.sep, '.')
        self.p1_name = p1_module
        self.p2_name = p2_module

        super().__init__(p1_dir, p2_dir, delay, 'ignore.txt', output, pace)

        self.matches_left = matches
        self.l_match_data = []

    def __del__(self):
        self.history_file.close()
        # Preguiça
        os.remove('ignore.txt')

    def run_multiple(self):
        print(f'Rodando {self.matches_left} partidas...')
        for i in tqdm(range(self.matches_left)):
            self.state = GameState(Board(), Board.BLACK)
            match_result = self.run()
            self.l_match_data.append(match_result)
        print("Fim da simulação")

    def run(self):
        self.start = time.localtime()

        illegal_count = {Board.BLACK: 0, Board.WHITE: 0}  # counts the number of illegal move attempts

        elapsed_avg = []
        while True:  # runs until endgame
            # creates auxiliary variables for better readability
            current_player = self.state.player
            # calculates scores
            p1_score = self.state.board.num_pieces(Board.BLACK) 
            p2_score = self.state.board.num_pieces(Board.WHITE) 

            # checks whether both players don't have available moves (end of game)
            if self.state.is_terminal():

                result = 0 if p1_score > p2_score else 1 if p2_score > p1_score else 2
                finish = time.localtime()
                
                return MatchData(result, p1_score, p2_score, finish, sum(elapsed_avg) / len(elapsed_avg), False)
            
            # disqualify player if it attempts illegal moves 5 times in a row
            if illegal_count[current_player] >= 5:
                result = 0 if current_player == Board.WHITE else 1
                finish = time.localtime()

                return MatchData(result, p1_score, p2_score, finish, sum(elapsed_avg) / len(elapsed_avg), True)

            # if this player is moving twice, shows a message that the opponent has no legal moves
            if self.last_player == current_player:
                time.sleep(self.pace)

            # creates a copy of the state, so that player can do whathever it wants
            state_copy = self.state.copy()

            # calls current player's make_move function with the specified timeout
            start = time.time()
            function_call = timer.FunctionTimer(self.player_modules[current_player].make_move, (state_copy,))  # argument must be a 1-element tuple
            
            move = function_call.run(self.delay)
                
            elapsed = time.time() - start
            elapsed_avg.append(elapsed)
            if move is None:  # detects timeout
                illegal_count[current_player] += 1
                continue

            move_x, move_y = move

             # checks for move validity
            if not isinstance(move_x, int) or not isinstance(move_y, int):
                move_x = move_y = -1  # -1 is my code for type error
                #illegal_count[current_player] += 1


            if self.state.is_legal_move(move):   
                self.last_player = current_player
                self.state = self.state.next_state(move)  

            else:
                illegal_count[current_player] += 1

            # waits the remaining time, if needed
            if self.pace - elapsed > 0:
                time.sleep(self.pace - elapsed)


    def write_output(self, show=True):
        p1 = 0
        p2 = 0
        draw = 0
        with open(self.output_file, 'a') as f:
            f.write(f'{datetime.datetime.now()}\n')
            f.write(f'P1: {self.p1_name}\n')
            f.write('VS\n')
            f.write(f'P2: {self.p2_name}\n')
            f.write('--------------------------\n')
            for i, match_data in enumerate(self.l_match_data):
                f.write(f'Match {i}:\n {match_data}\n')
            if match_data.match_status == 0:
                p1 += 1
            elif match_data.match_status == 1:
                p2 += 1
            else:
                draw += 1    
            f.write('\n\n\n')

        plt.bar(['P1', 'P2', 'DRAW'], [p1, p2, draw])
        plt.savefig(f'{self.p1_name}_vs_{self.p2_name}'.replace('.','_') + '.png')
        if show:
            plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Fast Othello server.')
    parser.add_argument('players', metavar='player', type=str, nargs=2,
                        help='Path to player directory')
    parser.add_argument('-d', '--delay', type=float, metavar='delay',
                        default=5.0,
                        help='Time allocated for players to make a move.')

    parser.add_argument('-p', '--pace', type=float,
                        default=0,
                        help='Pace of the match: time to wait to display a move '
                             '(if a player returns a move before the delay/timeout).')

    parser.add_argument('-o', '--output-file', type=str, dest='output',
                        default='results.txt', metavar='output-file',
                        help='File to save game details (includes history)')
    
    parser.add_argument('-m', '--matches', type=int, metavar='matches',
                        default=10,
                        help='How many matches are simulated.')

    args = parser.parse_args()
    p1, p2 = args.players

    s = FastServer(p1, p2, args.delay, args.output, args.pace, args.matches)
    s.run_multiple()
    s.write_output()