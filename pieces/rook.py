from pieces.base import Piece
from tools import OnBoard, Position
from setting import Config
from utils import GetSprite

class Rook(Piece):
    def __init__(self, position, color):
        super().__init__(position, color)
        self.code = "r"
        self.value = 50 if color == 0 else -50
        self.sprite = GetSprite(self)
        self.previousMove = None
        self.pieceMap = []

    def GetMoves(self, board):
        moves, captures = self.VertHorzMoves(board)
        return moves, captures

    def VertHorzMoves(self, board):
        patterns = ((-1, 0), (1, 0), (0, 1), (0, -1))
        return self.GetPatternMoves(board, patterns)
