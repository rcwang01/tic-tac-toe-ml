import random
import numpy as np
from tictactoe_dbop import TicTacToeDbOp
from tictactoe_minimax import TicTacToeMinimax
# import pickle
import json

matrix = np.array([['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9']])
matrix_tp = matrix.transpose()
num_matrix = ['1', '2', '3', '4', '5', '6', '7', '8', '9']


def generate_game_play(rounds, is_machine_x):
    random_move_first = True
    if is_machine_x:
        random_move_first = False
    for count in range(rounds):
        game_play = TicTacToeGamePlay()
        game_play.start_new_game(is_machine_x)
        while not game_play.game_over:
            # print('  Machine is ' + game_play.machine_mover + ' Game state is ' + str(game_play.game_state))
            game_play.get_next_move(TicTacToeRandom.get_next_move(random_move_first, game_play.game_state))
        dbop = TicTacToeDbOp()
        if game_play.game_state.get('winner') is None:
            dbop.write(json.dumps(game_play.game_state), '')
        else:
            dbop.write(json.dumps(game_play.game_state), game_play.game_state['winner'])
        print('Round: ' + str(count) + ' = ' + str(game_play.game_state))


class TicTacToeRandom:
    @staticmethod
    def get_next_move(is_max, game_state):
        next_mover = 'X'
        next_num_pos = ''
        found_winner_move = False
        if not is_max:
            next_mover = 'O'
        if len(game_state) >= 4:
            # Find any open move can become a winner
            for num_pos in range(len(num_matrix)):
                check_pos = num_matrix[num_pos]
                if game_state.get(check_pos) is None:
                    new_game_state = game_state.copy()
                    new_game_state.update({check_pos: [999, next_mover]})
                    for x_pos in range(3):
                        # Check horizontal alignments
                        p1 = new_game_state.get(matrix[x_pos, 0])
                        p2 = new_game_state.get(matrix[x_pos, 1])
                        p3 = new_game_state.get(matrix[x_pos, 2])
                        if p1 is not None and p2 is not None and p3 is not None:
                            if p1[1] == p2[1] and p2[1] == p3[1] and p3[1] == next_mover:
                                next_num_pos = check_pos
                                found_winner_move = True
                                break
                        # Check vertical alignments
                        p1 = new_game_state.get(matrix_tp[x_pos, 0])
                        p2 = new_game_state.get(matrix_tp[x_pos, 1])
                        p3 = new_game_state.get(matrix_tp[x_pos, 2])
                        if p1 is not None and p2 is not None and p3 is not None:
                            if p1[1] == p2[1] and p2[1] == p3[1] and p3[1] == next_mover:
                                next_num_pos = check_pos
                                found_winner_move = True
                                break
                    if not found_winner_move:
                        # Check diagonal alignments
                        p1 = new_game_state.get(matrix[0, 0])
                        p2 = new_game_state.get(matrix[1, 1])
                        p3 = new_game_state.get(matrix[2, 2])
                        if p1 is not None and p2 is not None and p3 is not None:
                            if p1[1] == p2[1] and p2[1] == p3[1] and p3[1] == next_mover:
                                next_num_pos = check_pos
                                found_winner_move = True
                                break
                        # Check transposed diagonal alignments
                        p1 = new_game_state.get(matrix_tp[0, 0])
                        p2 = new_game_state.get(matrix_tp[1, 1])
                        p3 = new_game_state.get(matrix_tp[2, 2])
                        if p1 is not None and p2 is not None and p3 is not None:
                            if p1[1] == p2[1] and p2[1] == p3[1] and p3[1] == next_mover:
                                next_num_pos = check_pos
                                found_winner_move = True
                                break

                if found_winner_move:
                    # Stop other available move search.
                    break

        if not found_winner_move:
            # Search '1' through '9' for open move
            open_position = []
            for num_position in range(len(num_matrix)):
                if game_state.get(str(num_position+1)) is None:
                    open_position.append(str(num_position+1))
            if len(open_position) > 0:
                next_num_pos = random.choice(open_position)
        return next_num_pos


class TicTacToeGamePlay:
    # this class only operate with TicTacToeMinimax class
    # game_state is to keep {position: [sequence, X/O]} format
    game_state = {}
    game_over = False
    minimax = None
    sequence = 0
    machine_mover = ''

    def __init__(self):
        return

    def start_new_game(self, is_machine_x):
        # erase current game state and start a new one
        start_position = ''
        # wipe out all previous game.
        self.minimax = TicTacToeMinimax()
        self.game_state.clear()
        self.game_over = False
        self.sequence = 0
        self.machine_mover = 'O'
        if is_machine_x:
            self.machine_mover = 'X'
            # action = self.minimax.ab_decision(self.machine_mover)
            # action = self.minimax.minimax_decision(self.machine_mover)
            # ------------------------------------------------------------
            # disable minimax initial move selection and make it random
            action = self.convert_to_coordinate(random.choice(num_matrix))
            # ------------------------------------------------------------
            self.minimax.play_square(action[0], action[1], self.machine_mover)
            start_position = self.convert_from_coordinate(action[0], action[1])
            self.sequence = 1
            self.game_state.update({start_position: [self.sequence, self.machine_mover]})
        return start_position

    def get_next_move(self, opponent_move):
        next_move = ''
        opponent_mover = 'X'
        if self.machine_mover == 'X':
            opponent_mover = 'O'
        if self.sequence < len(num_matrix):
            self.sequence += 1
            # ----------------------
            # record opponent's move
            self.game_state.update({opponent_move: [self.sequence, opponent_mover]})
            # ----------------------
            opponent_coordinate = self.convert_to_coordinate(opponent_move)
            self.minimax.play_square(opponent_coordinate[0], opponent_coordinate[1], opponent_mover)
        if self.minimax.full_board() is True and self.minimax.winner() == 'N':
            # No one wins - no need to record winner
            # ----------------------
            # record winner
            self.game_state.update({'winner': ''})
            # ----------------------
            self.game_over = True
        else:
            if self.minimax.winner() == opponent_mover:
                # ----------------------
                # record winner
                self.game_state.update({'winner': self.minimax.winner()})
                # ----------------------
                self.game_over = True
            else:
                action = self.minimax.ab_decision(self.machine_mover)
                # action = self.minimax.minimax_decision(self.machine_mover)
                self.minimax.play_square(action[0], action[1], action[2])
                next_move = self.convert_from_coordinate(action[0], action[1])
                self.sequence += 1
                # ----------------------
                # record machine's move
                self.game_state.update({next_move: [self.sequence, self.machine_mover]})
                # ----------------------
                if self.minimax.winner() == self.machine_mover:
                    # ----------------------
                    # record winner
                    self.game_state.update({'winner': self.minimax.winner()})
                    # ----------------------
                    self.game_over = True
        return next_move

    def convert_from_coordinate(self, col, row):
        return matrix[col, row]

    def convert_to_coordinate(self, num_position):
        col = -1
        row = -1
        for x in range(3):
            for y in range(3):
                if matrix[x, y] == num_position:
                    col = x
                    row = y
        coordinate = []
        coordinate.append(col)
        coordinate.append(row)
        return coordinate


if __name__ == '__main__':
    import sys
    if len(sys.argv) >= 3:
        is_machine_max = False
        if sys.argv[2].lower() == 'true':
            is_machine_max = True
        # DO NOT directly use bool() converter which is not working
        generate_game_play(int(sys.argv[1]), is_machine_max)
    elif len(sys.argv) == 2:
        generate_game_play(int(sys.argv[1]), False)
    else:
        print('Error: Please enter at least one argument')
