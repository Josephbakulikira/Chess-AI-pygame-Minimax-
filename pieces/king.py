from pieces.base import Piece
from tools import OnBoard, Position
from setting import Config
from utils import GetSprite

class King(Piece):
    def __init__(self, position, color):
        super().__init__(position, color)
        self.code = "k"
        # self.value = 100 if color == 0 else -100
        self.sprite = GetSprite(self)
        self.previousMove = None
        self.pieceMap = []
        self.value = 900 if color == 0 else -900

    def CanCastle(piece):
        return piece != None and piece.previousMove == None

    def Castle(self, board):
        castles = []
        rightRook = board.grid[7][self.position.y]
        leftRook = board.grid[0][self.position.y]

        # check if the king hasn't moved
        # check if there is no piece between the rooks
        # and the king
        if self.previousMove == None:
            # CASTLE LEFT
            if (board.grid[1][self.position.y] == None and board.grid[2][self.position.y] == None \
                and board.grid[3][self.position.y] == None) and King.CanCastle(leftRook):
                castles.append(Position(2, self.position.y))
            # CASTLE RIGHT
            if (board.grid[5][self.position.y] == None and board.grid[6][self.position.y] == None) \
                and King.CanCastle(rightRook):
                castles.append(Position(6, self.position.y))

        return castles

    def GetMoves(self, board):
        moves = []
        captures = []
        castles = self.Castle(board)

        for x in range(-1, 2):
            for y in range(-1, 2):
                dx = self.position.x + x
                dy = self.position.y + y
                temp = Position(dx, dy)
                if (x != 0 or y != 0) and OnBoard(temp):
                    if board.grid[dx][dy] == None:
                        moves.append(temp.GetCopy())
                    else:
                        if board.grid[dx][dy].color != self.color:
                            captures.append(temp.GetCopy())
        moves += castles
        return moves, captures
