import pygame
import settings as s
import os
from settings import log as l
from gen import Generate as ge
import saver as sa
import gui
from gui import button as btn
from gui import text as txt
import recipe as r
from inventory import get, set

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
    # Calculate the center of the screen in grid coordinates
    c_x = s.GRID_WIDTH // 2
    c_y = s.GRID_HEIGHT // 2

    # Calculate the top-left corner of the visible grid based on the player's position
    tl_x = player.x - c_x
    tl_y = player.y - c_y

    # Iterate over each tile in the visible grid area
    for y in range(s.GRID_WIDTH):
        for x in range(s.GRID_HEIGHT):
            # Calculate the actual grid coordinates for the current tile
            gx = tl_x + x
            gy = tl_y + y

            # Check if the current tile is within the bounds of the grid
            if 0 <= gx < len(grid) and 0 <= gy < len(grid[0]):
                # Get the sprite for the current tile and draw it on the screen
                image = grid[gx][gy].sprite()
                screen.blit(image, (128 * x, 72 * y))
            else:
                # If the tile is out of bounds, fill the area with black
                screen.fill((0, 0, 0), (128 * x, 72 * y, 128, 72))

    # Draw the player's sprite at the center of the screen
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
                grid[x][y].mine()
                crack_grid[x][y] = 0
                grid[x][y] = Air
                l(s.INFO, f"Wall at ({x}, {y}) broken")
                return False, grid, crack_grid
            else:
                crack_grid[x][y] += pow
                l(s.DEBUG, f"Wall at ({x}, {y}) cracked further")
        return False, grid, crack_grid

def gravity(grid, x, y): # TODO: IMPLEMENT THIS IN PLAYER MOVEMENT
    if not grid[x][y + 1].SOLID:
        l(s.DEBUG, f"Applying gravity at ({x}, {y})")
        return gravity(grid, x, y + 1)
    return x, y

# ITEMS
# s.item(Name, Description, Obtainable, sell price, buy price, sellable,
#  craftable, recipe_loc, stack, amount, a, b, c, d)
global dirt, water, paste, stone_dust, stone_chunk, stone_cube, coal, coal_furnace, copper_dust, copper_chunk, copper_bar

dirt = s.item("Dirt", "Dirt", True, 0, 0, False, False, None, 10000, 0)
water = s.item("Water", "A Liquid That could be drunken", True, 1, 5, True, False, None, 10000, 100)
paste = s.item("Paste", "A Wet Paste Used To Glue Ingredients", True, 0, 1, False, 
               True, r.r4, 10000, 0, dirt, water)
stone_dust = s.item("Stone Dust", "A Small Amount of Stone Tastes Like Stone", True, 1, 3, True, 
                    False, None, 10000, 0)
stone_chunk = s.item("Stone Chunk", "A Piece Of bigger Stone", True, 5, 7, True, 
                     True, r.r1, 10000, 0, stone_dust, paste)
stone_cube = s.item("Stone Cube", "A Solid Cube of Stone", True, 25, 30, True, 
                    True, r.r2, 10000, 0, stone_chunk, paste)
coal = s.item("Coal", "Used in a furnacce", True, 5, 10, True, 
              False, None, 10000, 0)
coal_furnace = s.item("Coal Furnace", "A Basic Machine That Uses Coal", True, 250, 550, True, 
                      True, r.r6, 100, 0, stone_cube, coal, paste, water)
copper_dust = s.item("Copper Dust", "A Small Amount of Copper", True, 5, 12, True, 
                     False, None, 10000, 0)
copper_chunk = s.item("Copper Chunk", "A bigger Piece of Copper", True, 40, 50, True, 
                      True, r.r3, 10000, 0, copper_dust, water)
copper_bar = s.item("Copper Bar", "A Starters best freind", True, 150, 230, True, 
                    True, r.r5, 10000, 0, copper_chunk, paste, coal_furnace, coal)
pure_copper_dust = None
pure_copper_chunk = None
pure_copper_bar = None

print(f"setting")
set([dirt, water, 
    paste, stone_dust, 
    stone_chunk, stone_cube, 
    copper_dust, copper_chunk,
    coal, coal_furnace, 
    copper_bar, ])


# MATERIALS
Air = s.Object(s.TEST_SPRITE_PATH)
Dirt = s.Object(path("Dirt.png"), True, 1, False, True, path("Dirt.json", table=True), True, dirt, 4)
Stone = s.Object(path("Stone.png"), True, 2, False, True, path("Stone.json", table=True), True, stone_dust, 4)
Copper_ore = s.Object(path("Copper_ore.png"), True, 2, False, True, path("Copper_ore.json", table=True), True, copper_dust, 3)
Iron_ore = s.Object(path("Iron_ore.png"), True, 2, False, True, path("Iron_ore.json", table=True), False)
"""
Lithium_ore = s.Object(path("Lithium_ore.png"), True, 4, False, True, TABLE=path("Lithium_ore.json", table=True))
Cobolt_ore = s.Object(path("Cobolt_ore.png"), True, 5, False, True, TABLE=path("Cobolt_ore.json", table=True))
Aluminium_ore = s.Object(path("Aluminium_ore.png"), True, 3, False, True, TABLE=path("Aluminium_ore.json", table=True))
Nickel_ore = s.Object(path("Nickel_ore.png"), True, 3, False, True, TABLE=path("Nickel_ore.json", table=True))
"""
Hard_stone = s.Object(path("Hard_stone.png"), True, 3, False, True, path("Hard_stone.json", table=True), True, stone_chunk, 1)
l(s.INFO, "Materials initialized")


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
g.start(air=Dirt)
g.mass([ Dirt, Hard_stone, Stone, Copper_ore, Iron_ore])
GAME_GRID, CRACK_GRID = g.get()
l(s.INFO, "Game grid generated")

player = Player(START_X, START_Y)
GAME_GRID[START_X][START_Y] = Air
state = "game"
gui = gui.gui()
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
            elif option == "Inventory":
                gui.inventory(screen, btn, txt)
                

        pygame.display.flip()
        clock.tick(60)
