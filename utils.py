import pygame
from setting import Config

highlight_size = (Config.spotSize + 5, Config.spotSize + 5)

white_highlight = pygame.image.load("./assets/images/highlighter.png")
blue_highlight = pygame.image.load("./assets/images/bluehighlighter.png")
green_highlight = pygame.image.load("./assets/images/greenhighlighter.png")
red_highlight = pygame.image.load("./assets/images/redhighlighter.png")
circle_highlight = pygame.image.load("./assets/images/circlehighlight.png")
outline_highlight = pygame.image.load("./assets/images/circleOutline.png")

wh = pygame.transform.smoothscale(white_highlight, highlight_size)
bh = pygame.transform.smoothscale(blue_highlight, highlight_size)
gh = pygame.transform.smoothscale(green_highlight, highlight_size)
rh = pygame.transform.smoothscale(red_highlight, highlight_size)
ch = pygame.transform.smoothscale(circle_highlight, highlight_size)
oh = pygame.transform.smoothscale(outline_highlight, highlight_size)


white_pawn = pygame.image.load("./assets/images/white_pawn.png")
white_bishop = pygame.image.load("./assets/images/white_bishop.png")
white_knight = pygame.image.load("./assets/images/white_knight.png")
white_rook = pygame.image.load("./assets/images/white_rook.png")
white_queen = pygame.image.load("./assets/images/white_queen.png")
white_king = pygame.image.load("./assets/images/white_king.png")

black_pawn = pygame.image.load("./assets/images/black_pawn.png")
black_bishop = pygame.image.load("./assets/images/black_bishop.png")
black_knight = pygame.image.load("./assets/images/black_knight.png")
black_rook = pygame.image.load("./assets/images/black_rook.png")
black_queen = pygame.image.load("./assets/images/black_queen.png")
black_king = pygame.image.load("./assets/images/black_king.png")

def translate(value, min1, max1, min2, max2):
    return min2 + (max2-min2) * ((value-min1)/(max1-min1))

def GetSprite(piece):
    sprite = None
    if piece.code == 'p':
        if piece.color == 0:
            sprite = white_pawn
        else:
            sprite = black_pawn
    elif piece.code == 'b':
        if piece.color == 0:
            sprite = white_bishop
        else:
            sprite = black_bishop
    elif piece.code == 'n':
        if piece.color == 0:
            sprite = white_knight
        else:
            sprite = black_knight
    elif piece.code == 'r':
        if piece.color == 0:
            sprite = white_rook
        else:
            sprite = black_rook
    elif piece.code == 'q':
        if piece.color == 0:
            sprite = white_queen
        else:
            sprite = black_queen
    else:
        if piece.color == 0:
            sprite = white_king
        else:
            sprite = black_king
    transformed = pygame.transform.smoothscale(sprite, (Config.spotSize, Config.spotSize))
    return transformed
