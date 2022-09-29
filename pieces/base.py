from setting import Config
from utils import *
from tools import Position, OnBoard

class Piece:
    def __init__(self, position, color):
        # 0 -> White, 1 -> Black
        self.position = position
        self.color = color
        self.previousMove = None
        self.code = None

    def updatePosition(self, position):
        self.position.x = position.x
        self.position.y = position.y

    def GetPatternMoves(self, board, patterns):
        moves = []
        captures = []
        for pattern in patterns:
            m, c = self.generator(board, pattern[0], pattern[1])
            moves =  moves+ m
            captures = captures+ c
        return moves, captures

    def generator(self, board, dx, dy):
        moves = []
        captures = []
        pos = Position(self.position.x + dx, self.position.y + dy)

        while OnBoard(pos) and board.grid[pos.x][pos.y] == None:
            moves.append(pos.GetCopy())
            pos.x = pos.x + dx
            pos.y = pos.y + dy
        if OnBoard(pos) and board.grid[pos.x][pos.y] != None and board.grid[pos.x][pos.y].color != self.color:
            captures.append(pos.GetCopy())

        # print(moves)

        return moves, captures
