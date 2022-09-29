import pygame

pygame.init()
pygame.font.init()

class Setting:
    def __init__(self):
        self.boardSize = 8
        self.windowIconSize = 30
        self.width = 1600
        self.height = 900
        self.resolution = (self.width, self.height)
        self.top_offset = 20
        self.spotSize = (self.height - self.top_offset) // self.boardSize
        self.horizontal_offset = self.width // 2 - (self.spotSize * (self.boardSize // 2))
        self.fps = 60
        self.CoordFont = pygame.font.SysFont("jaapokki", 18, bold=True)
        self.highlightOutline = 5
        self.themeIndex = -1
        # CHANGE THE AI DIFFICULTY
        self.AI_DEPTH = 3
        self.themes = [
            # CORAL THEME
            {"dark": (112, 162, 163), "light": (173, 228, 185), "outline": (0, 0, 0)},
            # DUSK THEME
            {"dark": (112, 102, 119), "light": (204, 183, 174), "outline": (0, 0, 0)},
            # MARINE THEME
            {"dark": (111, 115, 210), "light": (157, 172, 255), "outline": (0, 0, 0)},
            # WHEAT THEME
            {"dark": (187, 190, 100), "light": (234, 240, 206), "outline": (0, 0, 0)},
            # EMERALD THEME
            {"dark": (111, 143, 114), "light": (173, 189, 143), "outline": (0, 0, 0)},
            # SAND CASTLE THEME
            {"dark": (184, 139, 74), "light": (227, 193, 111), "outline": (0, 0, 0)},
            # CHESS.com THEME
            {"dark": (148, 111, 81), "light": (240, 217, 181), "outline": (0, 0, 0)},
            # GREEN THEME
            {"dark": (118, 148, 85), "light": (234, 238, 210), "outline": (0, 0, 0)},
        ]

class Sound:
    def __init__(self):
        self.capture_sound = pygame.mixer.Sound("./assets/sounds/capture_sound.mp3")
        self.castle_sound = pygame.mixer.Sound("./assets/sounds/castle_sound.mp3")
        self.check_sound = pygame.mixer.Sound("./assets/sounds/check_sound.mp3")
        self.checkmate_sound = pygame.mixer.Sound("./assets/sounds/checkmate_sound.mp3")
        self.game_over_sound = pygame.mixer.Sound("./assets/sounds/gameover_sound.mp3")
        self.game_start_sound = pygame.mixer.Sound("./assets/sounds/start_sound.mp3")
        self.move_sound = pygame.mixer.Sound("./assets/sounds/move_sound.mp3")
        self.stalemate_sound = pygame.mixer.Sound("./assets/sounds/stalemate_sound.mp3")
        self.pop = pygame.mixer.Sound("./assets/sounds/pop.mp3")

Config = Setting()
sounds = Sound()
