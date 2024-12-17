import pygame
import settings as s
import os
from settings import log as l
from gen import Generate as ge
import saver as sa
from gui import gui as Gui
from gui import button as btn
import recipe as r

# pygame setup
pygame.init()
screen = pygame.display.set_mode((s.WINDOW_WIDTH, s.WINDOW_HEIGHT))
clock = pygame.time.Clock()
running = True

s.FONT = pygame.font.Font(None, 50)

START_X = s.START_X
START_Y = s.START_Y

script_dir = s.SCRIPT_DIR
l(s.DEBUG, "Script directory set to: " + script_dir)

def path(name, table=False):
    resolved_path = os.path.join(script_dir, "tables" if table else "sprites", name)
    l(s.DEBUG, f"Resolved path: {resolved_path}")
    return resolved_path

def render(grid):
    c_x = s.GRID_WIDTH // 2
    c_y = s.GRID_HEIGHT // 2

    tl_x = player.x - c_x
    tl_y = player.y - c_y

    for y in range(s.GRID_WIDTH):
        for x in range(s.GRID_HEIGHT):
            gx = tl_x + x
            gy = tl_y + y

            if 0 <= gx < len(grid) and 0 <= gy < len(grid[0]):
                image = grid[gx][gy].sprite()
                screen.blit(image, (128 * x, 72 * y))
            else:
                screen.fill((0, 0, 0), (128 * x, 72 * y, 128, 72))

    screen.blit(player.sprite(), (128 * c_x, 72 * c_y))

def walls(grid, x, y, crack_grid, level):
    mat = grid[x][y]
    l(s.DEBUG, f"Checking tile at ({x}, {y})")
    if mat == Air:
        return True, grid, crack_grid
    else:
        min_level = mat.LEVEL
        if min_level <= level:
            diff = (level + 1) - min_level
            pow = diff * diff
            if crack_grid[x][y] + pow >= 100:
                crack_grid[x][y] = 0
                grid[x][y] = Air
                l(s.INFO, f"Wall at ({x}, {y}) broken")
                return False, grid, crack_grid
            else:
                crack_grid[x][y] += pow
                l(s.DEBUG, f"Wall at ({x}, {y}) cracked further")
        return False, grid, crack_grid

def gravity(grid, x, y):
    if not grid[x][y + 1].SOLID:
        l(s.DEBUG, f"Applying gravity at ({x}, {y})")
        return gravity(grid, x, y + 1)
    return x, y

# MATERIALS

Air = s.Object(s.TEST_SPRITE_PATH)
Dirt = s.Object(path("Dirt.png"), True, 1, False, True, TABLE=path("Dirt.json", table=True))
Stone = s.Object(path("Stone.png"), True, 2, False, True, TABLE=path("Stone.json", table=True))
l(s.INFO, "Materials initialized")

# ITEMS
"""
stone_dust = s.item("Stone Dust", "A Small Amount of Stone Tastes Like Stone", True, 1, 3, True, 1, 10000, 0)
stone_chunk = s.item("Stone Chunk", "A Piece Of bigger Stone", True, 5, 7, True, 2, 10000, 0)
stone_cube = s.item("Stone Cube", "A Solid Cube of Stone", True, 25, 30, True, 3, 10000, 0)
"""

GAME_GRID = [[Air for _ in range(s.GRID_HEIGHT)] for _ in range(s.GRID_WIDTH)]
l(s.INFO, "Game grid initialized")

class Player:
    def __init__(self, X, Y):
        self.x = X
        self.KEY_DELAY = 0
        self.y = Y
        self.SPRITE = pygame.image.load(path("Player.png")).convert_alpha()
        self.MINING_LEVEL = 100
        l(s.INFO, f"Player initialized at ({X}, {Y})")

    def Get_input(self, GAME_GRID, state, CRACK_GRID):
        if self.KEY_DELAY == s.KEY_DELAY_MAX:
            k = pygame.key.get_pressed()

            if k[s.KEYBINDS["up"]]:
                can, GAME_GRID, CRACK_GRID = walls(GAME_GRID, self.x, self.y - 1, CRACK_GRID, self.MINING_LEVEL)
                if can:
                    self.y -= 1
                    l(s.INFO, "Player moved up")
            if k[s.KEYBINDS["down"]]:
                can, GAME_GRID, CRACK_GRID = walls(GAME_GRID, self.x, self.y + 1, CRACK_GRID, self.MINING_LEVEL)
                if can:
                    self.y += 1
                    l(s.INFO, "Player moved down")
            if k[s.KEYBINDS["left"]]:
                can, GAME_GRID, CRACK_GRID = walls(GAME_GRID, self.x - 1, self.y, CRACK_GRID, self.MINING_LEVEL)
                if can:
                    self.x -= 1
                    l(s.INFO, "Player moved left")
            if k[s.KEYBINDS["right"]]:
                can, GAME_GRID, CRACK_GRID = walls(GAME_GRID, self.x + 1, self.y, CRACK_GRID, self.MINING_LEVEL)
                if can:
                    self.x += 1
                    l(s.INFO, "Player moved right")
            if k[s.KEYBINDS["load"]]:
                self.x = START_X
                self.y = START_Y
                GAME_GRID, CRACK_GRID = sa.load()
                l(s.INFO, "Game state loaded")
            if k[s.KEYBINDS["save"]]:
                sa.save(GAME_GRID, CRACK_GRID)
                l(s.INFO, "Game state saved")
            if k[s.KEYBINDS["menu"]]:
                state = "menu"
                l(s.INFO, "Player opened the menu")

            self.KEY_DELAY = 0
        else:
            self.KEY_DELAY += 1

        return GAME_GRID, state, CRACK_GRID

    def sprite(self):
        return self.SPRITE 
    
    def set_mining_level(self, num):
        self.MINING_LEVEL = num
        l(s.INFO, f"Player mining level set to {num}")

g = ge()
g.start(air=Air)
g.mass([Dirt, Stone])
GAME_GRID, CRACK_GRID = g.get()
l(s.INFO, "Game grid generated")

player = Player(START_X, START_Y)
GAME_GRID[START_X][START_Y] = Air
state = "game"
gui = Gui()
l(s.INFO, "Game initialized")

if __name__ == "__main__":
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                l(s.INFO, "Game quit event received")

        screen.fill("purple")
        render(GAME_GRID)
        GAME_GRID, state, CRACK_GRID = player.Get_input(GAME_GRID, state, CRACK_GRID)
        if state == "menu":
            option = gui.menu(screen=screen, button=btn)
            if option == "quit":
                running = False
                l(s.INFO, "Player chose to quit from menu")
            elif option == "game":
                state = "game"
                l(s.INFO, "Player resumed the game from menu")

        pygame.display.flip()
        clock.tick(60)
