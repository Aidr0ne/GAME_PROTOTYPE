import os
import time
import logging
import pygame

# LOGGING CONFIG

logging.basicConfig(
     format="{asctime} - {levelname} - {message}",
     style="{",
     datefmt="%Y-%m-%d %H:%M",
     filename="app.log",
     encoding="utf-8",
     filemode="a",
)

DEBUG = logging.DEBUG
INFO = logging.INFO
WARNING = logging.WARNING
ERROR = logging.ERROR
CRITICAL = logging.CRITICAL

FILE_LOG_LEVEL = INFO
PRINT_LOG_LEVEL = DEBUG

logging.basicConfig(level=FILE_LOG_LEVEL)

###############
###CONSTANTS###
###############

WINDOW_WIDTH = 1152
WINDOW_HEIGHT = 648

GRID_HEIGHT = 9
GRID_WIDTH = 9

START_X = 10
START_Y = 3

COLOUR_1 = (200, 200, 200)
COLOUR_2 = (0, 0, 0)
COLOUR_3 = (0, 0, 255)
COLOUR_4 = (173, 126, 230)

FONT = None

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

KEY_DELAY_MAX = 5

MINE_DEPTH = 1000
MINE_WIDTH = 25

NUMBER_OF_MINES = 1

TEST_SPRITE_PATH = SCRIPT_DIR + "/sprites/Test(128, 72).png"

KEYBINDS = {
    "up": pygame.K_w,
    "down": pygame.K_s,
    "left": pygame.K_a,
    "right": pygame.K_d,
    "save": pygame.K_p,
    "load": pygame.K_o,
    "menu": pygame.K_ESCAPE
}

def log(level, message):
    # TODO: Fix this 
    pre = f"{time.asctime()} -- {logging.getLevelName(level)} -- {message}" 
    if level == 10:
        logging.debug(message)
    elif level == 20:
        logging.info(message)
    elif level == 30:
        logging.warning(message)
    elif level == 40:
        logging.error(message)
    elif level == 50:
        logging.critical(message)

    if level <= 10:
        print(pre)
    elif level <= 20:
        print(pre)
    elif level <= 30:
        print(pre)
    elif level <= 40:
        print(pre)
    elif level <= 50:
        print(pre)

class Object:
    def __init__(self, 
                 SPRITE_PATH= SCRIPT_DIR + "/sprites/Test(128, 72).png",
                 SOLID = False,
                 LEVEL = 0,
                 LIGHT_SOURCE = False,
                 MINEABLE = False,
                 TABLE = SCRIPT_DIR +  "/tables/test.json",
                 ):
        self.SPRITE_PATH = SPRITE_PATH
        self.SPRITE = pygame.image.load(self.SPRITE_PATH).convert_alpha()
        self.SOLID = SOLID
        self.LEVEL = LEVEL
        self.LIGHT_SOURCE = LIGHT_SOURCE
        self.MINEABLE = MINEABLE
        self.TABLE = TABLE
        log(DEBUG, f"Object Loaded with Sprite path {self.SPRITE_PATH}, And Table Path {self.TABLE}")

    def sprite(self):
        return self.SPRITE
    
    def table(self):
        return self.TABLE
    
    def unload(self):
        self.SPRITE = None

    def reload(self):
        self.SPRITE = pygame.image.load(self.SPRITE_PATH).convert_alpha()

    def __getstate__(self):
        state = self.__dict__.copy()
        state["SPRITE"] = None  # Exclude the non-serializable surface
        return state
    
    def __setstate__(self, state):
        self.__dict__ = state
        self.reload()  # Reload the sprite from the path

# TODO: FINISH item CLASS
class item:
    def __init__(self,
                 name,
                 description,
                 obtainable,
                 sell_price,
                 buy_price,
                 sellable,
                 recipe_no,
                 stack,
                 amount,
                 ):
        self.obtainable = obtainable
        self.name = name
        self.description = description
        self.sell_price = sell_price
        self.buy_price = buy_price
        self.sellable = sellable
        self.recipe_no = recipe_no
        self.stack = stack
        self.amount = amount

    def __str__(self):
        return self.name