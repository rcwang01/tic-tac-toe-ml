import pickle
import random
from tictactoe_dbop import TicTacToeDbOp


def generate_game_play(rounds, is_machine_x):
    for count in range(rounds):
        game_play = TicTacToeGamePlay()
        game_play.start_new_game(is_machine_x)
        while not game_play.game_over:
            game_play.get_next_move(TicTacToeRandom.get_next_move(game_play.game_state))

        dbop = TicTacToeDbOp()
        dbop.write(game_play.game_state)
        print('Round: ' + str(count) + ' = ' + str(game_play.game_state))


class TicTacToeRandom:
    seed = 1.0

    @staticmethod
    def get_next_move(game_state):
        open_position = []
        for num_position in range(9):
            if not game_state[num_position]:
                open_position.append(num_position)
        return random.choice(open_position)


class TicTacToeGamePlay:
    # this class only operate with TicTacToeMinimax class
    # game_state is to keep {position: [sequence, X/O]} format
    game_state = {}
    game_over = False

    def __init__(self):
        # do nothing yet
        return

    def write_current_state(self):
        # serialize the game's current state
        return

    def read_current_state(self):
        # load the game's current state
        return

    def start_new_game(self, is_machine_x):
        # erase current game state and start a new one
        self.game_state.clear()
        start_position = 0
        if is_machine_x:
            # TODO: call titactoe_minimax method to get the first move
            start_position = 1
        return start_position

    def get_next_move(self, opponent_move):
        # input the opponent's move and determine the new move
        return

    def convert_from_coordinate(self, position):
        return

    def convert_to_coordinate(self, num_position):
        return


if __name__ == '__main__':
    import sys
    if len(sys.argv) >= 2:
        generate_game_play(int(sys.argv[0]), bool(sys.argv[1]))
    elif len(sys.argv) == 1:
        generate_game_play(int(sys.argv[0]), False)
    else:
        print('Error: Please enter at least one argument')
