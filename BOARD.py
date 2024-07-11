import numpy
from math import inf
ROWS, COLS = 8, 8
class BOARD:
    def __init__(self,table=numpy.zeros((8,8)),evaluation=0,red_coins = [[0, 1], [0, 3], [0, 5], [0, 7],
                [1, 0], [1, 2], [1, 4], [1, 6],
                [2, 1], [2, 3], [2, 5], [2, 7]],
                blue_coins = [[5, 0], [5, 2], [5, 4], [5, 6],
                [6, 1], [6, 3], [6, 5], [6, 7],
                [7, 0], [7, 2], [7, 4], [7, 6]],is_current_blue=True):
        self.table = table
        self.red_coins = red_coins

        self.blue_coins = blue_coins
        self.evaluation = evaluation
        self.is_current_blue=is_current_blue
        self.next_moves=None

    def find_next_moves(self):
        ret=[]
        if self.is_current_blue:
            coins=self.blue_coins
        else:
            coins=self.red_coins
        mandatory_jump=False
        
        for i in coins:
            twos,threes=self.find_legal_moves(i[0],i[1])
            if twos==[] and threes==[]:
                continue
            if threes!=[]:
                mandatory_jump=True
                for j in threes:
                    new_board=BOARD(table=self.table.copy(),red_coins=self.red_coins.copy(),blue_coins=self.blue_coins.copy(),is_current_blue=self.is_current_blue)
                    new_board.move(i,j)
                    ret.append(new_board)
            if twos!=[] and not mandatory_jump:
                for j in twos:
                    new_board=BOARD(table=self.table.copy(),red_coins=self.red_coins.copy(),blue_coins=self.blue_coins.copy(),is_current_blue=self.is_current_blue)
                    new_board.move(i,j)
                    ret.append(new_board)
        return ret
    
    def get_next_moves(self):
        self.next_moves=self.find_next_moves()
        return self.next_moves





    def check(self):
        #complete this
        if 3 in self.table:
            return True
        return False

    def find_legal_moves(self, row, col):
        twos=[]
        threes=[]
        if self.is_current_blue:
            legal_moves = [(row - 1, col - 1), (row - 1, col + 1)]
            own_pieces=self.blue_coins
            opponent_pieces=self.red_coins
            bound=0
        else:
            legal_moves = [(row + 1, col - 1), (row + 1, col + 1)]
            own_pieces=self.red_coins
            opponent_pieces=self.blue_coins
            bound=8
        for legal_row, legal_col in legal_moves:
            if (0 <= legal_row < 8 and 0 <= legal_col < 8
                and [legal_row, legal_col] not in own_pieces ):
                
                if [legal_row, legal_col] not in opponent_pieces:
                    twos.append([legal_row,legal_col])
                else:
                    legal_row += 1 if bound else -1
                    legal_col += 1 if legal_col > col else -1
                    if (0 <= legal_row < 8 and 0 <= legal_col < 8 
                        and [legal_row, legal_col] not in own_pieces 
                        and [legal_row, legal_col] not in opponent_pieces ):
                        threes.append([legal_row,legal_col])
        return twos,threes
    
    def update_legal_moves(self, row, col):

        copy=self.table.copy()
        twos,threes=self.find_legal_moves(row, col)
        for i in twos:
            copy[i[0]][i[1]]=2
        for i in threes:
            copy[i[0]][i[1]]=3
        return copy

    def move(self, active_coin, destination):
        if self.is_current_blue:
            self.blue_coins.remove(active_coin)
            self.blue_coins.insert(0, destination)
            if abs(active_coin[0]-destination[0]) == 2:
                self.red_coins.remove([(active_coin[0]+destination[0])//2, (active_coin[1]+destination[1])//2])
        else:
            self.red_coins.remove(active_coin)
            self.red_coins.insert(0, destination)
            if abs(active_coin[0]-destination[0]) == 2:
                self.blue_coins.remove([(active_coin[0]+destination[0])//2, (active_coin[1]+destination[1])//2])
        
    
    def reset(self):
        self.table = numpy.zeros((8, 8))

    def evaluate_state(self):
        #needs update
        if(len(self.blue_coins)==0):
            return inf
        if (len(self.red_coins)==0):
            return -inf
        return len(self.red_coins) - len(self.blue_coins)

    def alpha_beta(self, depth, alpha, beta, max_player):# red is max player
        if depth == 0 or len(self.red_coins)==0 or len(self.blue_coins)==0:
            return self.evaluate_state()
        if max_player:
            max_evaluation = -inf
            for child in self.get_next_moves():
                eval = child.alpha_beta( depth - 1, alpha,
                                beta, False)
                max_evaluation = max(max_evaluation, eval)
                
                # self.evaluation=max_evaluation
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_evaluation
        else:
            min_evaluation = inf
            for child in self.get_next_moves():
                eval = child.alpha_beta( depth - 1, alpha,
                                beta, True)
                min_evaluation = min(min_evaluation, eval)
                # self.evaluation=min_evaluation
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_evaluation