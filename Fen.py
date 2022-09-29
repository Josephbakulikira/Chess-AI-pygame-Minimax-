from pieces import *
from utils import *
from setting import Config
from tools import Position

def GetFenPieces(character, x, y):
    FenPieces = {
    "K": King(Position(x, y), 0),
    "Q": Queen(Position(x, y), 0),
    "B": Bishop(Position(x, y), 0),
    "N": Knight(Position(x, y), 0),
    "R": Rook(Position(x, y), 0),
    "P": Pawn(Position(x, y), 0),

    "k": King(Position(x, y), 1),
    "q": Queen(Position(x, y), 1),
    "b": Bishop(Position(x, y), 1),
    "n": Knight(Position(x, y), 1),
    "r": Rook(Position(x, y), 1),
    "p": Pawn(Position(x, y), 1),
    }

    if character in FenPieces:
        return FenPieces[character]
    else:
        return None

# The fen notation function return a grid of the formated Position
def FEN(positionstring):
    # initialize empty grid
    boardGrid = [[None for i in range(Config.boardSize)] for j in range(Config.boardSize)]
    # handle first field , placement of pieces
    row = 0
    col = 0
    for character in positionstring:
        piece = GetFenPieces(character, row, col)
        if piece:
            boardGrid[row][col] = piece
            row +=1
        elif character.isnumeric():
            row += int(character)
        elif character == "/":
            col += 1
            row = 0
    # This fen function does not take into account the player turn
    # this Fen function is not complete
    # usually a fen function take into consideration all the 6 field of FEN notation
    # but for this we only need the first field for the position
    return boardGrid

# FEN("")
