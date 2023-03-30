from cmath import inf
from operator import truediv
import random
import sys
import time
from collections import defaultdict as dd
# from turtle import *

#####################################################
# turtle graphic
#####################################################
# tracer(0,1)

BOK = 50
SX = -100
SY = 0
M = 8
MAX_DEPTH = 0
#weight of the evaluation function
A = 1  # a number of figures
BB = 161  # a number of occupied corners
C = 5  # a number of possible moves
D = 61  # a number of pawns connected with corner pieces
E = 1  # a number of glued blank fields
F = 1  # a number of pawns glued to empty fields
G = 1
# a=41
# b=180
# d=50


#####################################################

def initial_board():
    B = [[None] * M for i in range(M)]
    B[3][3] = 1
    B[4][4] = 1
    B[3][4] = 0
    B[4][3] = 0
    return B


class Board:
    dirs = [(0, 1), (1, 0), (-1, 0), (0, -1),
            (1, 1), (-1, -1), (1, -1), (-1, 1)]

    def __init__(self):
        self.board = initial_board()
        self.fields = set()
        self.move_list = []
        self.history = []
        self.l = [2, 2]
        for i in range(M):
            for j in range(M):
                if self.board[i][j] == None:
                    self.fields.add((j, i))

    def moves(self, player):
        res = []
        for (x, y) in self.fields:
            if any(self.can_beat(x, y, direction, player) for direction in Board.dirs):
                res.append((x, y))
        if not res:
            return [None]
        return res

    def can_beat(self, x, y, d, player):
        dx, dy = d
        x += dx
        y += dy
        cnt = 0
        while self.get(x, y) == 1-player:
            x += dx
            y += dy
            cnt += 1
        return cnt > 0 and self.get(x, y) == player

    def get(self, x, y):
        if 0 <= x < M and 0 <= y < M:
            return self.board[y][x]
        return None

    def do_move(self, move, player):
        self.history.append([x[:] for x in self.board])
        self.move_list.append(move)

        if move == None:
            return
        x, y = move
        x0, y0 = move
        self.board[y][x] = player
        self.l[player] += 1
        self.fields -= set([move])
        for dx, dy in self.dirs:
            x, y = x0, y0
            to_beat = []
            x += dx
            y += dy
            while self.get(x, y) == 1-player:
                to_beat.append((x, y))
                x += dx
                y += dy
            if self.get(x, y) == player:
                for (nx, ny) in to_beat:
                    self.board[ny][nx] = player
                    self.l[player] += 1
                    self.l[1 - player] -= 1

    def result(self):
        res = 0
        for y in range(M):
            for x in range(M):
                b = self.board[y][x]
                if b == 0:
                    res -= 1
                elif b == 1:
                    res += 1
        return res

    def terminal(self):
        if not self.fields:
            return True
        if len(self.move_list) < 2:
            return False
        return self.move_list[-1] == self.move_list[-2] == None

    def random_move(self, player):
        ms = self.moves(player)
        if ms:
            return random.choice(ms)
        return [None]

    def cut_off_tests(self, depth):
        if depth > MAX_DEPTH:
            return True
        return False

    def heuristics(self, mov, bit):
        # A - number of pieces on the board
        # number of corners occupied
        result = self.terminal()
        if result:
            if self.result() > 0:
                return inf
            if self.result() == 0:
                return 0
            if self.result() < 0:
                return -inf
        licz2_1 = 0
        licz2_2 = 0

        rog_1 = 0
        rog_2 = 0
        if self.board[0][0] == 0:
            licz2_1 += 1
            k = 1
            while k <= M - 1 and self.board[0][k] != 1 and self.board[0][k] != None:
                rog_1 += 1
                k += 1
            k = 1
            while k <= M - 1 and self.board[k][0] != 1 and self.board[k][0] != None:
                rog_1 += 1
                k += 1
        if self.board[0][0] == 1:
            licz2_2 += 1
            k = 1
            while k <= M - 1 and self.board[0][k] != 0 and self.board[0][k] != None:
                rog_2 += 1
                k += 1
            k = 1
            while k <= M - 1 and self.board[k][0] != 0 and self.board[k][0] != None:
                rog_2 += 1
                k += 1
        if self.board[0][M - 1] == 0:
            licz2_1 += 1
            k = M - 2
            while k >= 0 and self.board[0][k] != 1 and self.board[0][k] != None:
                rog_1 += 1
                k -= 1
            k = 1
            while k <= M - 1 and self.board[k][M - 1] != 1 and self.board[k][M - 1] != None:
                rog_1 += 1
                k += 1
        if self.board[0][M - 1] == 1:
            licz2_2 += 1
            k = M - 2
            while k >= 0 and self.board[0][k] != 0 and self.board[0][k] != None:
                rog_2 += 1
                k -= 1
            k = 1
            while k <= M - 1 and self.board[k][M - 1] != 0 and self.board[k][M - 1] != None:
                rog_2 += 1
                k += 1
        if self.board[M - 1][0] == 0:
            licz2_1 += 1
            k = M - 2
            while k >= 0 and self.board[k][0] != 1 and self.board[k][0] != None:
                rog_1 += 1
                k -= 1
            k = 1
            while k <= M - 1 and self.board[M - 1][k] != 1 and self.board[M - 1][k] != None:
                rog_1 += 1
                k += 1
        if self.board[M - 1][0] == 1:
            licz2_2 += 1
            k = M - 2
            while k >= 0 and self.board[k][0] != 0 and self.board[k][0] != None:
                rog_2 += 1
                k -= 1
            k = 1
            while k <= M - 1 and self.board[M - 1][k] != 0 and self.board[M - 1][k] != None:
                rog_2 += 1
                k += 1
        if self.board[M - 1][M - 1] == 0:
            licz2_1 += 1
            k = M - 2
            while k >= 0 and self.board[k][M - 1] != 1 and self.board[k][M - 1] != None:
                rog_1 += 1
                k -= 1
            k = M - 2
            while k >= 0 and self.board[M - 1][k] != 1 and self.board[M - 1][k] != None:
                rog_1 += 1
                k -= 1
        if self.board[M - 1][M - 1] == 1:
            licz2_2 += 1
            k = M - 2
            while k >= 0 and self.board[k][M - 1] != 0 and self.board[k][M - 1] != None:
                rog_2 += 1
                k -= 1
            k = M - 2
            while k >= 0 and self.board[M - 1][k] != 0 and self.board[M - 1][k] != None:
                rog_2 += 1
                k -= 1
        dicti1 = {}
        dicti2 = {}
        licz4_1 = 0
        licz4_2 = 0
        licz5_1 = 0
        licz5_2 = 0
        licz6_1 = 0
        licz6_2 = 0

        dire = [[1, 0], [-1, 0], [0, -1], [0, 1],
                [-1, -1], [-1, 1], [1, -1], [1, 1]]
        for i in range(0, M):
            for j in range(0, M):
                if self.board[i][j] == None:
                    stop2 = 1
                    stop1 = 1
                    for d in range(0, 4):
                        xx = i + dire[d][0]
                        yy = j + dire[d][1]
                        if xx >= 0 and xx <= M-1 and yy >= 0 and yy <= M-1:
                            if self.board[xx][yy] == 1:
                                if (xx, yy) not in dicti2:
                                    licz5_2 += 1
                                    dicti2[(xx, yy)] = 1
                                if stop2 == 1:
                                    licz4_2 += 1
                                    stop2 = 0
                            elif self.board[xx][yy] == 0:
                                if (xx, yy) not in dicti1:
                                    licz5_1 += 1
                                    dicti1[(xx, yy)] = 1
                                if stop1 == 1:
                                    licz4_1 += 1
                                    stop1 = 0
        return A*(self.l[1]-self.l[0]) + BB*(licz2_2 - licz2_1) + D*(rog_2 - rog_1) + E*(licz4_1 - licz4_2)

    def max_alpha_beta(self, alpha, beta, depth):
        maxv = -inf
        px = None
        py = None
        player = 1
        mov = self.moves(1)
        if mov != [None]:
            for i, j in mov:
                if self.board[j][i] == None:
                    x, y = (i, j)
                    x0, y0 = (i, j)
                    self.board[j][i] = 1
                    self.l[player] += 1
                    self.fields -= set([(i, j)])
                    to_beatt = []
                    # effects of placing in (j,i) pawn 1
                    for dx, dy in self.dirs:
                        x, y = x0, y0
                        to_beat = []
                        x += dx
                        y += dy
                        while self.get(x, y) == 1-player:
                            to_beat.append((x, y))
                            x += dx
                            y += dy
                        if self.get(x, y) == player:
                            for (nx, ny) in to_beat:
                                self.board[ny][nx] = player
                                to_beatt.append((nx, ny))
                                self.l[player] += 1
                                self.l[1-player] -= 1
                    # end of effects
                    m = self.heuristics(mov, 1)
                    if m > maxv:
                        maxv = m
                        px = i
                        py = j
                    # undo everything
                    for (nx, ny) in to_beatt:
                        self.board[ny][nx] = 1 - player
                        self.l[1 - player] += 1
                        self.l[player] -= 1
                    self.board[j][i] = None 
                    self.l[player] -= 1
                    self.fields.add((i, j))
                    # end undo

        else:
            return (-1, None, None)

        return (maxv, px, py)

    def min_alpha_beta(self, alpha, beta, depth, a, b, d):
        minv = inf
        player = 0
        qx = None
        qy = None
        result = self.terminal()
        if result:
            if self.result() > 0:
                return (inf, 0, 0)
            if self.result() == 0:
                return (0, 0, 0)
            if self.result() < 0:
                return (-inf, 0, 0)
        mov = self.moves(0)
        if self.cut_off_tests(depth):
            return (self.heuristics(mov, 0, a, b, d), 0, 0)
        if mov != [None]:
            for i, j in mov:
                if self.board[j][i] == None:
                    x, y = (i, j)
                    x0, y0 = (i, j)
                    self.board[j][i] = 0
                    self.l[player] += 1
                    self.fields -= set([(i, j)])
                    to_beatt = []
                    # effects of placing in (j,i) pawn 0
                    for dx, dy in self.dirs:
                        x, y = x0, y0
                        to_beat = []
                        x += dx
                        y += dy
                        while self.get(x, y) == 1-player:
                            to_beat.append((x, y))
                            x += dx
                            y += dy
                        if self.get(x, y) == player:
                            for (nx, ny) in to_beat:
                                self.board[ny][nx] = player
                                to_beatt.append((nx, ny))
                                self.l[player] += 1
                                self.l[1-player] -= 1
                    # end of effects
                    m = self.heuristics(mov, 0, a, b, d)
                    if m < minv:
                        minv = m
                        qx = i
                        qy = j
                    # undo everything
                    for (nx, ny) in to_beat:
                        self.board[ny][nx] = 1 - player
                        self.l[1 - player] += 1
                        self.l[player] -= 1
                    self.board[j][i] = None
                    self.l[player] -= 1
                    self.fields.add((i, j))
        else:
            (m, max_i, max_j) = self.max_alpha_beta(
                alpha, beta, depth + 1, a, b, d)
            if m < minv:
                minv = m

        return (minv, qx, qy)


player = 0
failure = 0
# a=41
# b=180
# d=50
start = time.time()
for it in range(0, 1000):
    B = Board()
    while True:
        if (player == 0):
            m = B.random_move(player)
            B.do_move(m, player)
        else:
            (m, qx, qy) = B.max_alpha_beta(-inf, inf, 0)
            if qx != None:
                B.do_move((qx, qy), player)
        player = 1-player
        if B.terminal():
            break
    if B.result() < 0:
        failure += 1


end = time.time()
print('Evaluation time: {}s'.format(round(end - start, 7)))
print("How many failures for my agent (out of 1000): " + str(failure))
sys.exit(0)
