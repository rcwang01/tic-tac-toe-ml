import struct, string, copy


class TicTacToeMinimax:
    board = []

    def __init__(self):
        self.board = (['N']*3, ['N']*3, ['N']*3)

    def play_square(self, col, row, val):
        self.board[col][row] = val

    def get_square(self, col, row):
        return self.board[col][row]

    def full_board(self):
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 'N':
                    return False
        return True
    
    # if there is a winner this will return their symbol (either 'X' or 'O'),
    # otherwise it will return 'N'
    def winner(self):
        # check the cols
        for col in range(3):
            if self.board[col][0] != 'N' and self.board[col][0] == self.board[col][1] and self.board[col][0] == self.board[col][2]:
                return self.board[col][0]
        # check the rows
        for row in range(3):
             if self.board[0][row] != 'N' and self.board[0][row] == self.board[1][row] and self.board[0][row] == self.board[2][row]:
                return self.board[0][row]
        # check diagonals
        if self.board[0][0] != 'N' and self.board[0][0] == self.board[1][1] and self.board[0][0] == self.board[2][2]:
            return self.board[0][0]
        if self.board[2][0] != 'N' and self.board[2][0] == self.board[1][1] and self.board[2][0] == self.board[0][2]:
            return self.board[2][0]
        return 'N'

    def make_simple_cpu_move(self, cpuval):
        for i in range(3):
            for j in range(3):
                if self.get_square(i, j) == 'N':
                    self.play_square(i, j, cpuval)
                    return True
        return False

    def utility(self):
        winner = self.winner()
        if winner is 'X':
            return 1
        elif winner is 'O':
            return -1
        return 0

    def successors(self, val):
        boardlist = []
        for row in range(3):
            for col in range(3):
                if self.get_square(col, row) is 'N':
                    self.play_square(col, row, val)
                    boardlist.append(copy.deepcopy(self.board))
                    self.play_square(col, row, 'N')
        return boardlist

    def actions(self, val):
        # action is (col, row, val)
        actionlist = []
        for row in range(3):
            for col in range(3):
                if self.get_square(col, row) is 'N':
                    actionlist.append((col, row, val))
        return actionlist

    def min_value(self):
        if self.full_board() or self.winner() is not 'N':
            return self.utility()
        v = float("inf")
        success = self.successors('O')
        for state in success:
            v = min(v, self.max_value(state))
        return v

    def max_value(self):
        if self.full_board() or self.winner() is not 'N':
            return self.utility()
        v = float("-inf")
        for state in self.successors('X'):
            v = max(v, self.min_value(state))
        return v

    def minimax_decision(self, val):
        # returns an action (col, row, val)
        limit = 0
        if val is 'X':
            limit = float("-inf")
        else:
            limit = float("inf")
        currentMax = (None, limit)
        for action in self.actions(val):
            self.play_square(action[0], action[1], action[2])
            if val is 'X':
                v = self.min_value()
            else:
                v = self.max_value()
            self.play_square(action[0], action[1], 'N')
            if val is 'X':
                if v > currentMax[1]:
                    currentMax = (action, v)
            else:
                if v < currentMax[1]:
                    currentMax = (action, v)
        return currentMax[0]

    def ab(self, val, alpha=float("-inf"), beta=float("inf")):
        if self.full_board() or self.winner() is not 'N':
            return self.utility()
        children = self.actions(val)
        if val is 'X':
            for action in children:
                self.play_square(action[0], action[1], action[2])
                v = self.ab('O', alpha, beta)
                self.play_square(action[0], action[1], 'N')
                if v > alpha:
                    alpha = v
                if alpha >= beta:
                    return alpha
            return alpha
        else:
            for action in children:
                self.play_square(action[0], action[1], action[2])
                v = self.ab('X', alpha, beta)
                self.play_square(action[0], action[1], 'N')
                if v < beta:
                    beta = v
                if alpha >= beta:
                    return beta
            return beta

    def ab_decision(self, val):
        # returns an action (col, row, val)
        if val is 'X':
            limit = float("-inf")
        else:
            limit = float("inf")
        currentMax = (None, limit)
        for action in self.actions(val):
            self.play_square(action[0], action[1], action[2])
            if val is 'X':
                v = self.ab('O')
            else:
                v = self.ab('X')
            self.play_square(action[0], action[1], 'N')
            if val is 'X':
                if v > currentMax[1]:
                    currentMax = (action, v)
            else:
                if v < currentMax[1]:
                    currentMax = (action, v)
        return currentMax[0]
