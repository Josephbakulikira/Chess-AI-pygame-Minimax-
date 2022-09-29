from pieces.base import Piece
from pieces.rook import Rook
from pieces.bishop import Bishop
from tools import OnBoard, Position
from setting import Config
from utils import GetSprite

class Queen(Bishop, Rook, Piece):
    def __init__(self, position, color):
        super().__init__(position, color)
        self.code = "q"
        self.value = 90 if color == 0 else -90
        self.sprite = GetSprite(self)
        self.previousMove = None
        self.pieceMap = []

    def GetMoves(self, board):
        diagonal_moves, diagonal_captures = self.DiagonalMoves(board)
        r_moves, r_captures = self.VertHorzMoves(board)
        moves = diagonal_moves + r_moves
        captures = diagonal_captures + r_captures

        return moves, captures
