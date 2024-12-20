import pygame
from settings import log as l
import settings as s

c1 = s.COLOUR_1
c2 = s.COLOUR_2
c3 = s.COLOUR_3
c4 = s.COLOUR_4

"""
class input_box:
    def __init__(self, x, y, w, h, value, bc, type="str"):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = bc
        self.value = value
        self.type = type
        self.text_surface = s.FONT.render(str(value), True, c1)
        self.active = False
        self.cursor_pos = len(str(value))

    def handle(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False

        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.value = str(self.value)[:-1] 
                elif event.key == pygame.K_RETURN:
                    if self.type == "int":
                        try:
                            self.value = int(self.value) 
                        except ValueError:
                            print("Invalid input for integer!")
                    elif self.type == "tuple":
                        try:
                            self.value = tuple(map(int, self.value.split(',')))
                        except ValueError:
                            print("Invalid input for tuple!")
                    self.active = False 
                else:
                    self.value += event.unicode  

            self.text_surface = input_font.render(str(self.value), True, BLACK)

    def render(self, screen):
        # Draw the input box
        color = BLUE if self.active else self.color
        pygame.draw.rect(screen, color, self.rect, 2)
        # Draw the text
        screen.blit(self.text_surface, (self.rect.x + 5, self.rect.y + 5))

"""        
# Ok so input box might be a bit broken
# i was going to use it to change settings in game
# but they are constants
# so mabye we should leave them alone

# ... perhaps?
       
class text:
    def __init__(self, text, x, y, width, height, colour=(66, 135, 245)):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.colour = colour
        if text == "Empty":
            self.surface = s.FONT.render(text, True, c1)
        else:
            self.surface = s.FONT.render(text.name, True, c1)

    def render(self, screen):
        pygame.draw.rect(screen, self.colour, self.rect)
        text_rect = self.surface.get_rect(center=self.rect.center)
        screen.blit(self.surface, text_rect)


class button:
    def __init__(self, text, x, y, width, height, base_color, hover_color):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.base_color = base_color
        self.hover_color = hover_color
        self.text_surface = s.FONT.render(text, True, c1)

    def render(self, screen):
        color = self.hover_color if self.rect.collidepoint(pygame.mouse.get_pos()) else self.base_color
        pygame.draw.rect(screen, color, self.rect)
        text_rect = self.text_surface.get_rect(center=self.rect.center)
        screen.blit(self.text_surface, text_rect)

    def clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos)

class gui:
    def __init__(self):
        pass

    def menu(self, screen, button):
        waiting = True
        buttons = [
            button("Play", 100, 50, 150, 50, (66, 135, 245), (20, 107, 247)),
            button("Settings", 100, 110, 150, 50, (66, 135, 245), (20, 107, 247)),
            button("Inventory", 100, 170, 150, 50, (66, 135, 245), (20, 107, 247)),
            button("Quit", 100, 230, 150, 50, (66, 135, 245), (20, 107, 247)),
        ]
        while waiting:
            for event in pygame.event.get():
                if event == pygame.QUIT:
                    return "quit"
                
                for button in buttons:
                    if button.clicked(event):
                        if button.text == "Play":
                            return "game"
                        elif button.text == "Settings":
                            raise NotImplementedError
                        elif button.text == "Quit":
                            return "quit"
                        elif button.text == "Inventory":
                            return "Inventory"
                        
            screen.fill((0, 0, 0))
            for button in buttons:
                button.render(screen)

            pygame.display.flip()


    def settings(self, input_box):
        pass

    def inventory(self, screen, button, text, item_list):
        waiting = True
        point = 0
        active = []
        buttons = [
            button("Up", 600, 540, 150, 50, c2, c3),
            button("Down", 600, 600, 150, 50, c2, c3),
            button("Exit", 600, 50, 150, 50, c2, c3)
        ]

        while waiting:
            screen.fill((0, 0, 0))
            active = []
            for i in range(s.INVENTORY_RANGE):  # Loads 10 items into active
                try:
                    active.append(item_list[point + i])
                except IndexError:
                    active.append("Empty")

            texts = [
                text(active[0], 100, 50, 200, 50),
                text(active[1], 100, 110, 200, 50),
                text(active[2], 100, 170, 200, 50),
                text(active[3], 100, 230, 200, 50),
                text(active[4], 100, 290, 200, 50),
                text(active[5], 100, 350, 200, 50),
                text(active[6], 100, 410, 200, 50),
                text(active[7], 100, 470, 200, 50),
                text(active[8], 100, 530, 200, 50),
                text(active[9], 100, 590, 200, 50),
            ]

            for txt in texts:
                txt.render(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                for btn in buttons:
                    if btn.clicked(event):
                        if btn.text == "Up":
                            if point > 0:
                                point -= 1
                            s.log(s.INFO, f"Inventory moved up a point is now {point}")
                        elif btn.text == "Down":
                            if point < len(item_list) - s.INVENTORY_RANGE:
                                s.log(s.INFO, f"Inventory moved down a point is now {point}")
                                point += 1
                        elif btn.text == "Exit":
                            waiting = False

            for btn in buttons:
                btn.render(screen)
            pygame.display.flip()

    def crafting_gui(self, ls):
        pass

"""    def create_boxes(self, value, x, y, ib):
        input_boxes = []
        if isinstance(value, int):
            input_boxes.append(ib(x, y, 150, 50, value, c4, type="int"))
        if isinstance(value, str):
            input_boxes.append(ib(x, y, 150, 50, value, c4, type="str"))
"""
