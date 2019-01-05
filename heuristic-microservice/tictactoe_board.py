import struct, string, copy
from tictactoe_minimax import TicTacToeMinimax


def print_board(board):
    print(board[0][0] + "|" + board[1][0] + "|" + board[2][0])
    print(board[0][1] + "|" + board[1][1] + "|" + board[2][1])
    print(board[0][2] + "|" + board[1][2] + "|" + board[2][2])


def play(cpuX, abOn):
    minimax = TicTacToeMinimax()
    if cpuX:
        cpuval = 'X'
        humanval = 'O'
    else:
        humanval =  'X'
        cpuval = 'O'
    print_board(minimax.board)

    if cpuX:
        print("CPU Move")
        # make_simple_cpu_move(Board, cpuval)
        if abOn:
            action = minimax.ab_decision(cpuval)
        else:
            action = minimax.minimax_decision(cpuval)
        # do the action that is best
        minimax.play_square(action[0], action[1], action[2])
        print_board(minimax.board)
   
    while (minimax.full_board() is False) and (minimax.winner() == 'N'):
        row = int(input("your move, pick a row (0-2): "))
        col = int(input("your move, pick a col (0-2): "))

        if minimax.get_square(col, row) != 'N':
            print("square already taken!")
            continue
        else:
            minimax.play_square(col, row, humanval)
            if minimax.full_board() or minimax.winner() != 'N':
                break
            else:
                print("CPU Move")
                # make_simple_cpu_move(Board, cpuval)
                if abOn:
                    action = minimax.ab_decision(cpuval)
                else:
                    action = minimax.minimax_decision(cpuval)
                # do the action that is best
                minimax.play_square(action[0], action[1], action[2])
                print_board(minimax.board)

    print_board(minimax.board)
    if minimax.winner() == 'N':
        print("Cat game")
    elif minimax.winner() == humanval:
        print("You Win!")
    elif minimax.winner() == cpuval:
        print("CPU Wins!")


def main():
    cpuX = input("Is CPU playing as X? [y,n] ")
    abOn = input("Do you want alpha-beta pruning on? [y,n] ")
    if cpuX is 'y':
        if abOn is 'y':
            play(True, True)
        else:
            play(True, False)
    else:
        if abOn is 'y':
            play(False, True)
        else:
            play(False, False)


if __name__ == '__main__':
    main()
