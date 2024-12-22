import settings as s
import json
import random

class Generate:
    def __init__(self):
        self.grid = []

    def start(self, air):
        self.grid = [[air for _ in range(s.MINE_DEPTH)] for _ in range(s.MINE_WIDTH)]
        self.crack_grid = [[0 for _ in range(s.MINE_DEPTH)] for _ in range(s.MINE_WIDTH)]

    def load_table(self, ore):
        try:
            with open(ore.table(), 'r') as file:
                table = json.load(file)
            return table
        except Exception as e:
            print(f"Error loading table: {e}")
            return None

    def mass(self, ores):
        for ore in ores:
            self.single(ore)

    def single(self, ore):
        table = self.load_table(ore)
        if not table:
            print(f"Table {ore.name} could not be loaded")
            return  # Skip if the table could not be loaded

        for y in range(s.MINE_DEPTH):
            for zn in range(int(table["zones"])):
                for zone in table[str(zn)]:
                    if zone["min"] <= y <= zone["max"]:
                        for x in range(s.MINE_WIDTH):
                            r = random.randint(0, 100)
                            if r < zone["chance"]:
                                self.grid[x][y] = ore

    def get(self):
        return self.grid, self.crack_grid
