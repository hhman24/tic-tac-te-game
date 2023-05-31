from argparse import Action
from setting import*
import math

class board:
    def __init__(self, level):
        self.matrix = [[INF for j in range(level)] for i in range(level)]
        self.lev = level


    def isEmpty(self):
        return self.marked == 0

    def toMatrix(self, matrix):
        self.matrix =  matrix
        self.lev = len(matrix)

    def terminalTest(self):
        winer = None
        count = 0
        cell_1 = []
        cell_2 = [] # row, col

        if(len(self.matrix) == 3):
            legal = 3
        elif(len(self.matrix) == 5):
            legal = 4
        elif(len(self.matrix) == 7):
            legal = 5

        for i in range(len(self.matrix)):
            for j in range(len(self.matrix)):

                #horizon
                winer = self.matrix[i][j]
                cell_1 = [i, j]
                if winer != INF:
                    count = 0
                    for k in range(legal - 1):
                        if(j+k+1) < len(self.matrix):
                            if (winer == self.matrix[i][j+k+1]):
                                count += 1

                    if count == legal - 1:
                        cell_2 = [i, j + count]
                        return winer, cell_1, cell_2

                    count = 0
                    # vertica

                    for k in range(legal - 1):
                        if(i+k+1) < len(self.matrix):
                            if(winer == self.matrix[i+k+1][j]):
                                count += 1

                    if count == legal - 1:
                        cell_2 = [i + count, j]
                        return winer, cell_1, cell_2
                    # Diagonal 

                    count = 0
                    for k in range(legal -1):
                        if(i+k+1) < len(self.matrix) and (j+k+1) < len(self.matrix):
                            if(winer == self.matrix[i+k+1][j+k+1]):
                                count += 1

                    if count == legal - 1:
                        cell_2 = [i + count, j + count]
                        return winer, cell_1, cell_2

                    # - diagonal
                    count = 0
                    for k in range(legal - 1):
                        if (i+k+1) < len(self.matrix) and (j-k-1) >= 0:
                            if(winer == self.matrix[i+k+1][j-k-1]):
                                count += 1

                    if count == legal - 1:
                        cell_2 = [i + count, j - count]
                        return winer, cell_1, cell_2
                        
        return None, None, None

    def clearBoard(self):
        self.matrix = [[INF for j in range(self.level)] for i in range(self.level)]
        self.marked = 0

    def isEmptyCell(self, row, col):
        if(self.matrix[row][col] == INF):
            return True
        else:
            return False

    def get_empty_cells(self):
        empty = []
        for row in range(len(self.matrix)):
            for col  in range(len(self.matrix)):
                if(self.empty_cell(row, col)):
                    empty.append((row, col))
    
    def isfull(self):
        
        for i in self.matrix:
            for j in i:
                if j == INF:
                    return False
        return True
    
    def print(self):
        for m in self.matrix:
            print(m)

class XAT: # gan gia luon bang 1

    # cần qui định về action -> move để di chuyển

    def __init__(self, play, player):
        self.play = play
        self.player = player # đói tượng người chơi

    def action(self, action, _board): # action is move[x,y, utilityMove]
        x = action[0]
        y = action[1]
        _board.matrix[x][y] =  self.play

    def backAction(self, action, _board):
        x = action[0]
        y = action[1]
        _board.matrix[x][y] = INF

    def utility(self, _board):
        eval = 0.0
        middle = (_board.lev-1)/2
        for i  in range (_board.lev): 
            for j in range(_board.lev):
                if _board.matrix[i][j] == self.play:
                    eval += 1/(math.sqrt((middle-i)**2 + (middle-j)**2)+1)
                    if i==j or _board.lev-1-i == j or i == _board.lev-1-j:
                        eval+=0.15

                if _board.matrix[i][j] == self.player.play:
                    eval -= 1/(math.sqrt((middle-i)**2 + (middle-j)**2)+1)
                    if i==j or _board.lev-1-i == j or i == _board.lev-1-j:
                        eval-=0.15
                    
        return eval
    
    def possibleMoves(self, mark, _board):
        result = []
        winner = _board.terminalTest()[0]

        if(winner == None):
            for i in range(_board.lev):
                for j in range(_board.lev):
                    if(_board.isEmptyCell(i,j)):
                        action = [i, j, mark]
                        result.append(action)

        return result

    def minimaxAlgorithm(self, bot_XAT, depth, alpha, beta, _board):
        winner = _board.terminalTest()[0]
        
        if(depth == 0 or winner == self.play or winner == self.player.play or winner == None): # là thang thua, depth = 0, hoa
            if(winner == self.play):
                return float('inf')
            elif(winner == self.player.play):
                return float('-inf')
            elif(_board.isfull() and winner == None): 
                return self.utility(_board) # tính ra 
            elif(depth == 0):
                return self.utility(_board) # tính ra 

        if bot_XAT == True:
            max_value = float("-inf")
            result = self.possibleMoves(self.play, _board) #ressult rong thi sao ??
            for r in result:
                self.action(r, _board)
                v = self.minimaxAlgorithm(False, depth-1, alpha, beta, _board)
                self.backAction(r, _board)
                max_value = max(max_value, v)
                alpha = max(alpha, max_value)
                if beta <= alpha:
                    break
            return max_value
        else:
            min_value = float("inf")
            result = self.possibleMoves(self.player.play, _board)
            for r in result:
                self.player.action(r, _board)
                v = self.minimaxAlgorithm(True, depth-1, alpha, beta, _board)
                self.player.backAction(r, _board)
                min_value = min(min_value, v)
                beta = min(beta, min_value)
                if beta <= alpha:
                    break

            return min_value

class player: # gan gia tri lun bang -1
    def __init__(self, play):
        self.play = play

    def action(self, action, _board): # action is move[x,y, utilityMove]
        x = action[0]
        y = action[1]
        _board.matrix[x][y] =  self.play

    def backAction(self, action, _board):
        x = action[0]
        y = action[1]
        _board.matrix[x][y] = INF
