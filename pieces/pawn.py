from pieces.base import Piece
from tools import OnBoard, Position
from setting import Config
from utils import GetSprite

class Pawn(Piece):
    def __init__(self, position, color):
        super().__init__(position, color)
        self.code = "p"
        self.value = 10 if color == 0 else -10
        self.sprite = GetSprite(self)
        self.previousMove = None
        self.pieceMap = []

    def EnPassant(self, board, change):
        moves = []
        for i in (-1, 1):
            temp_pos = Position(self.position.x + i, self.position.y)
            if OnBoard(temp_pos):
                pieceToCapture = board.grid[temp_pos.x][temp_pos.y]
                if type(pieceToCapture) == Pawn and self.color != pieceToCapture.color:
                    previousmove = board.RecentMove()
                    if previousmove != None and previousmove[2] == self.code and previousmove[4].x == self.position.x + i\
                        and abs(previousmove[4].y - previousmove[3].y) == 2:
                        moves.append(Position(self.position.x + i, self.position.y + change))

        return moves

    def GetMoves(self, board):
        moves = []
        captures = []
        if self.color == 0:
            offset = -1
        else:
            offset = 1
        dy = self.position.y + offset
        # all the possible moves of a pawn
        if OnBoard(Position(self.position.x, dy)) and board.grid[self.position.x][dy] == None :
            moves.append(Position(self.position.x, dy))
            if self.previousMove == None:
                dy += offset
                if board.grid[self.position.x][dy] == None:
                    moves.append(Position(self.position.x, dy))

        dy = self.position.y + offset
        # diagonal captures
        for i in (-1, 1):
            dx = self.position.x + i
            if OnBoard(Position(dx, dy)) and board.grid[dx][dy] != None:
                if board.grid[dx][dy].color != self.color:
                    captures.append(Position(dx, dy))
        # EN PASSANT CAPTURES
        special_moves = self.EnPassant(board, offset)
        captures += special_moves
        return moves, captures
