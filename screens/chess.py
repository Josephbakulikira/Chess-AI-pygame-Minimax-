import pygame
import sys
import time

from setting import Config, sounds
from tools import OnBoard, Position
from utils import bh, oh, ch
from board import Board
from Minimax.chessAI import Minimax
import ui

class Chess:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.gameOver = False
        self.board = Board()
        self.animateSpot = 1;
        self.selectedPiece = None
        self.selectedPieceMoves = None
        self.selectedPieceCaptures = None
        self.draggedPiece = None
        self.CanBeReleased = False
        self.AdjustedMouse = Position(0, 0)
        self.gameOverBackground = pygame.image.load("./assets/images/gameOver.jpg")
        self.gameOverBackground = pygame.transform.smoothscale(self.gameOverBackground, Config.resolution)
        self.gameOverHeader = ui.TextUI(self.screen, "GAME OVER", Config.width//2, Config.height//6, 140, (255, 255, 255))
        self.gameOverHeader.centered = True
        self.winnerText = ui.TextUI(self.screen, "White Won the game", Config.width//2, Config.height//2, 200, (190, 255, 180))
        self.winnerText.centered = True

        # Minimax(depht, chess_board, activate_alpha_beta_pruning = Default(true))
        self.ComputerAI = Minimax(Config.AI_DEPTH, self.board, True, True)

    def GetFrameRate(self):
        return self.clock.get_fps()

    def vsComputer(self):
        pygame.event.clear()
        sounds.game_start_sound.play()
        while not self.gameOver:
            self.clock.tick(Config.fps)
            self.screen.fill((0, 0, 0))
            self.getMousePosition()
            # update window caption
            pygame.display.set_caption("Chess : VS Computer " + str(int(self.GetFrameRate())))
            self.display()
            self.ComputerMoves(1)
            if self.gameOver == False:
                if self.animateSpot >= Config.spotSize:
                    self.HandleEvents()
                    self.IsGameOver()


    def multiplayer(self):
        pygame.event.clear()
        sounds.game_start_sound.play()
        while not self.gameOver:
            self.clock.tick(Config.fps)
            self.screen.fill((0, 0, 0))
            self.getMousePosition()
            # update window caption
            pygame.display.set_caption("Chess : Multiplayer " + str(int(self.GetFrameRate())))
            self.display()
            if self.animateSpot >= Config.spotSize:
                self.HandleEvents()
            self.IsGameOver()

    def display(self):
        self.Render()
        pygame.display.update()

    def HandleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.gameOver = True
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    self.board.Forfeit()
                    self.gameOver = True
                if event.key == pygame.K_UP:
                    if Config.themeIndex < len(Config.themes) -1 :
                        Config.themeIndex += 1
                    else:
                        Config.themeIndex = 0
                if event.key == pygame.K_DOWN:
                    if Config.themeIndex > 0:
                        Config.themeIndex -= 1
                    else:
                        Config.themeIndex = len(Config.themes) -1
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # print(self.AdjustedMouse)
                    self.HandleOnLeftMouseButtonDown()
                elif event.button == 3:
                    pass
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.HandleOnLeftMouseButtonUp()
    def ComputerMoves(self, player):
        if self.board.player == player:
            piece, bestmove = self.ComputerAI.Start(0)
            # print(bestmove)
            self.board.Move(piece, bestmove)
            if self.board.pieceToPromote != None:
                self.board.PromotePawn(self.board.pieceToPromote, 0)

            if bestmove:
                if self.board.GetPiece(bestmove) != None:
                    sounds.move_sound.play()
                else:
                    self.move_sound.play()


    def HandleOnLeftMouseButtonUp(self):
        self.draggedPiece = None
        if self.selectedPiece:
            if self.selectedOrigin != self.AdjustedMouse:
                if self.AdjustedMouse in self.selectedPieceCaptures:
                    self.board.Move(self.selectedPiece, self.AdjustedMouse)
                    # play sounds
                    sounds.capture_sound.play()
                elif self.AdjustedMouse in self.selectedPieceMoves :
                    self.board.Move(self.selectedPiece, self.AdjustedMouse)
                    # play sound
                    sounds.move_sound.play()
                self.ReleasePiece()
            elif self.CanBeReleased:
                self.ReleasePiece()
            else:
                self.CanBeReleased = True

    def SelectPiece(self,piece):
        if piece != None and piece.color == self.board.player:
            self.selectedPiece = piece
            self.draggedPiece = piece
            self.selectedPieceMoves, self.selectedPieceCaptures = self.board.GetAllowedMoves(self.selectedPiece)
            # self.selectedPieceMoves, self.selectedPieceCaptures = piece.GetMoves(self.board)
            self.selectedOrigin = self.AdjustedMouse


    def HandleOnLeftMouseButtonDown(self):
        if self.board.pieceToPromote != None and self.AdjustedMouse.x == self.board.pieceToPromote.position.x:
            choice = self.AdjustedMouse.y
            if choice <= 3 and self.board.player == 0:
                # promote pawn
                self.board.PromotePawn(self.board.pieceToPromote, choice)
                # refresh screen
                self.display()
            elif choice > 3 and self.board.player == 1:
                # promote pawn
                self.board.PromotePawn(self.board.pieceToPromote, 7-choice)
                # refresh screen
                self.display()
        else:
            if OnBoard(self.AdjustedMouse):
                piece = self.board.grid[self.AdjustedMouse.x][self.AdjustedMouse.y]
                if self.selectedPiece == piece:
                    self.draggedPiece = piece
                else:
                    self.SelectPiece(piece)

    def getMousePosition(self):
        x, y = pygame.mouse.get_pos()
        x = (x - Config.horizontal_offset) // Config.spotSize
        y = (y - Config.top_offset//2) // Config.spotSize
        self.AdjustedMouse = Position(x, y)

    def IsGameOver(self):
        if self.board.winner != None:
            self.gameOver = True
            # print("the game is over")
            self.display()
            self.gameOverWindow()

    def ReleasePiece(self):
        self.selectedPiece = None
        self.selectedPieceMoves = None
        self.selectedPieceCaptures = None
        self.draggedPiece = None
        self.selectedOrigin = None

    def Render(self):
        self.DrawChessBoard()
        if self.animateSpot >= Config.spotSize:
            self.DrawPieces()
        self.DrawHighlight()

    def DrawChessBoard(self):
        # drawing the empty chess board grid
        if self.animateSpot < Config.spotSize:
            self.animateSpot += 2
        for i in range(Config.boardSize):
            for j in range(Config.boardSize):
                x = i * Config.spotSize + Config.horizontal_offset
                y = j * Config.spotSize + Config.top_offset // 2
                if (i + j) % 2 == 0:
                    pygame.draw.rect(self.screen, Config.themes[Config.themeIndex]["light"], [x, y, self.animateSpot, self.animateSpot])
                else:
                    pygame.draw.rect(self.screen, Config.themes[Config.themeIndex]["dark"], [x, y, self.animateSpot, self.animateSpot])

    def DrawChessCoordinate(self):
        # drawing the chess coordinates
        for i in range(Config.boardSize):
            _x = 0.05 * Config.spotSize + Config.horizontal_offset
            _y = 0.05 * Config.spotSize + Config.top_offset + i * Config.spotSize
            color = Config.themes[Config.themeIndex]['dark'] if i % 2 == 0 else Config.themes[Config.themeIndex]['light']

            fontRenderer = Config.CoordFont.render(str(8-i), True, color)
            self.screen.blit(fontRenderer, (_x, _y))

            _x = 0.9 * Config.spotSize + Config.horizontal_offset + i * Config.spotSize
            _y = (Config.boardSize - 1) * Config.spotSize + Config.top_offset + Config.spotSize * 0.75
            color = Config.themes[Config.themeIndex]['light'] if i % 2 == 0 else Config.themes[Config.themeIndex]['dark']

            fontRenderer = Config.CoordFont.render(chr(ord("a")+ i), True, color)
            self.screen.blit(fontRenderer, (_x, _y))

    def DrawPieces(self):
        # draw previous position
        nPosition, oldPosition = self.board.RecentMovePositions()
        if oldPosition and nPosition:
            x1 = oldPosition.x * Config.spotSize + Config.horizontal_offset
            y1 = oldPosition.y * Config.spotSize + Config.top_offset // 2
            x2 = nPosition.x * Config.spotSize + Config.horizontal_offset
            y2 = nPosition.y * Config.spotSize + Config.top_offset // 2
            pygame.draw.rect(self.screen, (235, 100, 100), [x1, y1, Config.spotSize, Config.spotSize])
            pygame.draw.rect(self.screen, (225, 120, 120), [x2, y2, Config.spotSize, Config.spotSize])
        for x in range(Config.boardSize):
            for y in range(Config.boardSize):
                x_pos = x * Config.spotSize + Config.horizontal_offset
                y_pos = y * Config.spotSize + Config.top_offset // 2
                if self.board.grid[x][y] != None:
                    self.screen.blit(self.board.grid[x][y].sprite, (x_pos, y_pos))

    def RenderPromoteWindow(self):
        if self.board.pieceToPromote:
            if self.board.pieceToPromote.color == 0:
                x = self.board.pieceToPromote.position.x * Config.spotSize + Config.horizontal_offset
                y = self.board.pieceToPromote.position.y * Config.spotSize + Config.top_offset // 2
                pygame.draw.rect(self.screen, (200, 200, 200), [x, y, Config.spotSize , Config.spotSize * 4])
                for i in range(4):
                    piece = self.board.whitePromotions[i]
                    self.screen.blit(piece.sprite, (x, i * Config.spotSize + Config.top_offset //2 ))
                    bottomY = i * Config.spotSize - 1
                    pygame.draw.rect(self.screen, (0, 0, 0), [x, bottomY, Config.spotSize , 2])
            else:
                x = self.board.pieceToPromote.position.x * Config.spotSize + Config.horizontal_offset
                y = (self.board.pieceToPromote.position.y - 3) * Config.spotSize + Config.top_offset // 2
                pygame.draw.rect(self.screen, (200, 200, 200), [x, y, Config.spotSize , Config.spotSize * 4])
                for i in range(4):
                    piece = self.board.blackPromotions[i]
                    self.screen.blit(piece.sprite, (x, (i+4) * Config.spotSize + Config.top_offset //2 ))
                    bottomY = (i + 4) * Config.spotSize - 1
                    pygame.draw.rect(self.screen, (0, 0, 0), [x, bottomY, Config.spotSize , 2])


    def DrawHighlight(self):
        # highlight selected piece
        if self.selectedPiece != None:
            x = self.selectedPiece.position.x * Config.spotSize + Config.horizontal_offset
            y = self.selectedPiece.position.y * Config.spotSize + Config.top_offset // 2
            pygame.draw.rect(self.screen, (190, 200, 222), [x, y, Config.spotSize, Config.spotSize])
            # self.screen.blit(oh, (x, y))
            if self.draggedPiece == None:
                self.screen.blit(self.selectedPiece.sprite, (x, y))

        # draw selectedPiece possible moves
        if self.selectedPiece and self.selectedPieceMoves:
            for move in self.selectedPieceMoves:
                x = move.x * Config.spotSize + Config.horizontal_offset
                y = move.y * Config.spotSize + Config.top_offset // 2

                pygame.draw.rect(self.screen, (40, 130, 210), [x, y, Config.spotSize, Config.spotSize], Config.highlightOutline)

        # draw selected piece possible captures
        if self.selectedPiece and self.selectedPieceCaptures:
            for capturing in self.selectedPieceCaptures:
                x = capturing.x * Config.spotSize + Config.horizontal_offset
                y = capturing.y * Config.spotSize + Config.top_offset // 2
                self.screen.blit(ch, (x, y))

                # pygame.draw.rect(self.screen, (210, 211, 190), [x, y, Config.spotSize, Config.spotSize], Config.highlightOutline)
        # draw dragged piece
        if self.draggedPiece != None:
            x = self.AdjustedMouse.x * Config.spotSize + Config.horizontal_offset
            y = self.AdjustedMouse.y * Config.spotSize + Config.top_offset // 2
            self.screen.blit(self.draggedPiece.sprite, (x, y))


        # highlight if in Check
        # white king in check
        if self.board.checkWhiteKing:
            x = self.board.WhiteKing.position.x * Config.spotSize + Config.horizontal_offset
            y = self.board.WhiteKing.position.y * Config.spotSize + Config.top_offset // 2
            pygame.draw.rect(self.screen, (240, 111, 150), [x, y, Config.spotSize, Config.spotSize])
            self.screen.blit(self.board.WhiteKing.sprite, (x, y))
        # black king in check
        elif self.board.checkBlackKing:
            x = self.board.BlackKing.position.x * Config.spotSize + Config.horizontal_offset
            y = self.board.BlackKing.position.y * Config.spotSize + Config.top_offset // 2
            pygame.draw.rect(self.screen, (240, 111, 150), [x, y, Config.spotSize, Config.spotSize])
            self.screen.blit(self.board.BlackKing.sprite, (x, y))

        if self.animateSpot >= Config.spotSize:
            self.DrawChessCoordinate()

        self.RenderPromoteWindow()

    def gameOverWindow(self):
        if self.board.winner >= 0:
            sounds.game_over_sound.play()
        else:
            sounds.stalemate_sound.play()
        time.sleep(2)
        self.screen.blit(self.gameOverBackground, (0, 0))
        self.gameOverHeader.Draw()
        if self.board.winner  == 0:
            self.winnerText.text = "White Won"
            self.screen.blit(self.board.WhiteKing.sprite, (Config.width//2 - Config.spotSize // 2, Config.height//3))
        elif self.board.winner == 1:
            self.winnerText.text = "Black Won"
            self.screen.blit(self.board.BlackKing.sprite, (Config.width//2 - Config.spotSize // 2, Config.height//3))
        else:
            self.winnerText.text = "DRAW"

        self.gameOverHeader.Draw()
        self.winnerText.Draw()
        pygame.display.update()
        time.sleep(3)
        self.board = Board()
        self.animateSpot = 1
