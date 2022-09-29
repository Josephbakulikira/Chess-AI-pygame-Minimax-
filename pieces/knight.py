from pieces.base import Piece
from tools import OnBoard, Position
from setting import Config
from utils import GetSprite

class Knight(Piece):
    def __init__(self, position, color):
        super().__init__(position, color)
        self.code = "n"
        self.value = 30 if color == 0 else -30
        self.sprite = GetSprite(self)
        self.previousMove = None
        self.pieceMap = []

    def GetMoves(self, board):
        moves = []
        captures = []

        for i in range(-2, 3):
            if i != 0:
                for j in range(-2, 3):
                    if j != 0:
                        dx = self.position.x + i
                        dy = self.position.y + j
                        temp = Position(dx, dy)
                        if abs(i) != abs(j) and OnBoard(temp):
                            if board.grid[dx][dy] == None:
                                moves.append(temp.GetCopy())
                            else:
                                if board.grid[dx][dy].color != self.color:
                                    captures.append(temp.GetCopy())
        return moves, captures
