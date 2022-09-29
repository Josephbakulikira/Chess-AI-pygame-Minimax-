import pygame
from pieces import *
from setting import Config, sounds
from tools import Position, OnBoard
import math
from Fen import *

class Board:
    def __init__(self):
        # 0 -> white , 1 -> Black
        self.player = 0
        self.historic = []
        self.moveIndex = 1
        self.font = pygame.font.SysFont("Consolas", 18, bold=True)
        self.grid = FEN("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR")
        self.WhiteKing = None
        self.BlackKing = None
        for pieces in self.grid:
            for piece in pieces:
                if piece != None:
                    if piece.color == 0 and piece.code == "k":
                        self.WhiteKing = piece
                    elif piece.color == 1 and piece.code == "k":
                        self.BlackKing = piece

        # place pieces on the chess board
        # -- place all the pawns
        # for x in range(Config.boardSize):
        #     for y in range(Config.boardSize):
        #         if y == 1:
        #             # place black pawns
        #             self.grid[x][y] = Pawn(Position(x, y), 1)
        #
        #         elif y == 6:
        #             # place white pawns
        #             self.grid[x][y] = Pawn(Position(x, y), 0)

        # self.WhiteKing = King(Position(4, 7), 0)
        # self.BlackKing = King(Position(4, 0), 1)
        self.checkWhiteKing = False
        self.checkBlackKing = False

        # -- black pieces
        # self.grid[0][0] = Rook(Position(0, 0), 1)
        # self.grid[7][0] = Rook(Position(7, 0), 1)
        # self.grid[1][0] = Knight(Position(1, 0), 1)
        # self.grid[6][0] = Knight(Position(6, 0), 1)
        # self.grid[2][0] = Bishop(Position(2, 0), 1)
        # self.grid[5][0] = Bishop(Position(5, 0), 1)
        # self.grid[3][0] = Queen(Position(3, 0), 1)
        # self.grid[4][0] = self.BlackKing
        # -- white pieces
        # self.grid[0][7] = Rook(Position(0, 7), 0)
        # self.grid[7][7] = Rook(Position(7, 7), 0)
        # self.grid[1][7] = Knight(Position(1, 7), 0)
        # self.grid[6][7] = Knight(Position(6, 7), 0)
        # self.grid[2][7] = Bishop(Position(2, 7), 0)
        # self.grid[5][7] = Bishop(Position(5, 7), 0)
        # self.grid[3][7] = Queen(Position(3, 7), 0)
        # self.grid[4][7] = self.WhiteKing

        self.winner = None
        self.pieceToPromote = None

        self.whitePromotions = [Queen(Position(0, 0), 0), Bishop(Position(0, 1), 0), Knight(Position(0, 2), 0), Rook(Position(0, 3), 0)]
        self.blackPromotions = [Rook(Position(0, 7), 1), Knight(Position(0, 6), 1), Bishop(Position(0, 5), 1), Queen(Position(0, 4), 1)]

    def Forfeit(self):
        # resign
        pass

    def GetPiece(self, coord):
        return self.grid[coord.x][coord.y]

    def SetPiece(self, position, piece):
        self.grid[position.x][position.y] = piece

    def SwitchTurn(self):
        # switch between 0 and 1
        # (0 + 1) * -1 + 2 = 1
        # (1 + 1) * -1 + 2 = 0
        self.player = (self.player + 1 ) * -1 + 2
        # CHECK IF THE PLAYER LOST OR NOT
        self.IsCheckmate()

    def RecentMove(self):
        return None if not self.historic else self.historic[-1]

    def RecentMovePositions(self):
        if not self.historic or len(self.historic) <= 1:
            return None, None
        pos = self.historic[-1][3]
        oldPos = self.historic[-1][4]

        return pos.GetCopy(), oldPos.GetCopy()

    def AllowedMoveList(self, piece, moves, isAI):
        allowed_moves = []
        for move in moves:
            if self.VerifyMove(piece, move.GetCopy(), isAI):
                allowed_moves.append(move.GetCopy())
        return allowed_moves

    def GetAllowedMoves(self, piece, isAI=False):
        moves, captures = piece.GetMoves(self)
        allowed_moves = self.AllowedMoveList(piece, moves.copy(), isAI)
        allowed_captures = self.AllowedMoveList(piece, captures.copy(), isAI)
        return allowed_moves, allowed_captures

    def Move(self, piece, position):
        if position != None:
            position = position.GetCopy()
            # print(position)
            if self.isCastling(piece, position.GetCopy()):
                self.CastleKing(piece, position.GetCopy())
            elif self.isEnPassant(piece, position.GetCopy()):
                self.grid[position.x][piece.position.y] = None
                self.MovePiece(piece, position)
                self.historic[-1][2] = piece.code + " EP"
            else:
                self.MovePiece(piece, position)
            # check for promotion
            if type(piece) == Pawn and (piece.position.y == 0 or piece.position.y == 7):
                self.pieceToPromote = piece
            else:
                self.SwitchTurn()
            self.Check()

    def MovePiece(self, piece, position):
        position = position.GetCopy()
        self.grid[piece.position.x][piece.position.y] = None
        old_position = piece.position.GetCopy()
        piece.updatePosition(position)
        self.grid[position.x][position.y] = piece
        self.historic.append([self.moveIndex, piece.color, piece.code, old_position, piece.position, piece])
        piece.previousMove = self.moveIndex
        self.moveIndex += 1
        self.checkBlackKing = False
        self.checkWhiteKing = False

    def VerifyMove(self, piece, move, isAI):
        # verify the move by going through all the possible outcomes
        # This function will return False if the opponent will reply by capturing the king
        position = move.GetCopy()
        oldPosition = piece.position.GetCopy()
        captureEnPassant = None
        # print(f"new: {move}, old: {oldPosition}")
        capturedPiece = self.grid[position.x][position.y]
        if self.isEnPassant(piece, position):
            captureEnPassant = self.grid[position.x][oldPosition.y]
            self.grid[position.x][oldPosition.y] = None

        self.grid[oldPosition.x][oldPosition.y] = None
        self.grid[position.x][position.y] = piece
        # print(f"pos: {position}, old: {oldPosition}")
        piece.updatePosition(move)
        EnemyCaptures = self.GetEnemyCaptures(self.player)
        if self.isCastling(piece, oldPosition):
            if math.fabs(position.x - oldPosition.x) == 2 and not self.VerifyMove(piece, Position(5, position.y), isAI) \
                or math.fabs(position.x - oldPosition.x) == 3 and not self.VerifyMove(piece, Position(3, position.y), isAI) \
                or self.IsInCheck(piece):
                self.UndoMove(piece, capturedPiece, oldPosition, position)
                return False

        for pos in EnemyCaptures:
            if (self.WhiteKing.position == pos and piece.color == 0) \
                or (self.BlackKing.position == pos and piece.color == 1):
                self.UndoMove(piece, capturedPiece, oldPosition, position)
                if captureEnPassant != None:
                    self.grid[position.x][oldPosition.y] = captureEnPassant
                return False
        self.UndoMove(piece, capturedPiece, oldPosition, position)
        if captureEnPassant != None:
            self.grid[position.x][oldPosition.y] = captureEnPassant
        return True

    def UndoMove(self, piece, captured, oldPos, pos):
        self.grid[oldPos.x][oldPos.y] = piece
        self.grid[pos.x][pos.y] = captured
        piece.updatePosition(oldPos)

    def GetEnemyCaptures(self, player):
        captures = []
        for pieces in self.grid:
            for piece in pieces:
                if piece != None and piece.color != player:
                    moves, piececaptures = piece.GetMoves(self)
                    captures = captures + piececaptures
        return captures

    def isCastling(self,king, position):
        return type(king) == King and abs(king.position.x - position.x) > 1

    def isEnPassant(self, piece, newPos):
        if type(piece) != Pawn:
            return False
        moves = None
        if piece.color == 0:
            moves = piece.EnPassant(self, -1)
        else:
            moves = piece.EnPassant(self, 1)
        return newPos in moves

    def IsInCheck(self, piece):
        return type(piece) == King and \
                ((piece.color == 0 and self.checkWhiteKing) or (piece.color == 1 and self.checkBlackKing))

    def CastleKing(self, king, position):
        position = position.GetCopy()
        # print("castled")
        # print(position)
        if position.x == 2 or position.x == 6:
            if position.x == 2:
                rook = self.grid[0][king.position.y]
                self.MovePiece(king, position)
                self.grid[0][rook.position.y] = None
                rook.position.x = 3
                # print("black castled")
            else:
                rook = self.grid[7][king.position.y]
                self.MovePiece(king, position)
                self.grid[7][rook.position.y] = None
                rook.position.x = 5
                # print("white castled")

            rook.previousMove = self.moveIndex - 1
            self.grid[rook.position.x][rook.position.y] = rook
            self.historic[-1][2] = king.code + " C"
            sounds.castle_sound.play()

    def PromotePawn(self, pawn, choice):
        if choice == 0:
            self.grid[pawn.position.x][pawn.position.y] = Queen(pawn.position.GetCopy(), pawn.color)
        elif choice == 1:
            self.grid[pawn.position.x][pawn.position.y] = Bishop(pawn.position.GetCopy(), pawn.color)
        elif choice == 2:
            self.grid[pawn.position.x][pawn.position.y] = Knight(pawn.position.GetCopy(), pawn.color)
        elif choice == 3:
            self.grid[pawn.position.x][pawn.position.y] = Rook(pawn.position.GetCopy(), pawn.color)

        self.SwitchTurn()
        self.Check()
        self.pieceToPromote = None

    def MoveSimulation(self, piece, next_pos):
        if self.grid[next_pos.x][next_pos.y] == None:
            self.grid[piece.position.x][piece.position.y] = None
            piece.position = next_pos.GetCopy()
            self.grid[next_pos.x][next_pos.y] = piece
            return None
        else:
            prev_piece = self.grid[next_pos.x][next_pos.y]
            self.grid[piece.position.x][piece.position.y] = None
            piece.position = next_pos.GetCopy()
            self.grid[next_pos.x][next_pos.y] = piece
            return prev_piece

    def Check(self):
        if self.player == 0:
            king = self.WhiteKing
        else:
            king = self.BlackKing

        for pieces in self.grid:
            for piece in pieces:
                if piece != None and piece.color != self.player:
                    moves, captures = self.GetAllowedMoves(piece)
                    if king.position in captures:
                        if self.player == 1:
                            self.checkBlackKing = True
                            return
                        else:
                            self.checkWhiteKing = True
                            return

    def IsCheckmate(self):
        for pieces in self.grid:
            for piece in pieces:
                if piece != None and piece.color == self.player:
                    moves, captures = self.GetAllowedMoves(piece)
                    # if there's any legal move left
                    # then it's not checkmate
                    if moves or captures:
                        return False
        self.Check()
        if self.checkWhiteKing:
            # black won
            self.winner = 1
        elif self.checkBlackKing:
            # white won
            self.winner = 0
        else:
            # it's a draw
            self.winner = -1
        return True
