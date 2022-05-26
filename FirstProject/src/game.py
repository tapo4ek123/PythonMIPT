import pygame
import time
from src.boost import Boost
from src.button import Button
import sys


class Game:
    def __init__(self):
        pygame.init()
        self.display_weight = 800
        self.display_height = 800
        self.fps = 60
        self.time_between_update = 1
        self.prev_update_count = time.time()
        self.surface = pygame.display.set_mode((self.display_weight, self.display_height))

        self.boosts = [Boost(1), Boost(10), Boost(100), Boost(1000)]
        self.boosts_buttons = [Button(0, 0, 50, 'rect', self.surface),
                               Button(0, 60, 50, 'rect', self.surface),
                               Button(0, 120, 50, 'rect', self.surface),
                               Button(0, 180, 50, 'rect', self.surface)]
        self.cookie_button = Button(400, 300, 100, 'circ', self.surface)

        self.reset_button = Button(600, 0, 70, 'rect', self.surface, (200, 200, 200))
        self.exit_button = Button(600, 100, 70, 'rect', self.surface, (255, 0, 0))

        self.count = 0
        self.font = None
        self.income = 0
        self.cookie_add = 10

        self.reset_text = None
        self.exit_text = None

    def make_font(self):
        self.font = pygame.font.SysFont('Helvetica', 24)

    def make_text(self, text, color=(255, 255, 255)):
        return self.font.render(text, True, color)

    def make_surface(self):
        self.surface = pygame.display.set_mode((self.display_weight, self.display_height))

    def render_text(self):
        self.reset_text = self.make_text('reset', (0, 0, 0))
        self.exit_text = self.make_text('exit', (0, 0, 0))

    def load_data(self):
        with open('savings\\saves.txt', 'r') as f:
            data = f.read().split()
            self.count = int(data[0])
            self.income = int(data[1])
            self.boosts[0].count = int(data[2])
            self.boosts[1].count = int(data[3])
            self.boosts[2].count = int(data[4])
            self.boosts[3].count = int(data[5])

    def save_data(self):
        with open('savings\\saves.txt', 'w') as f:
            f.write(str(self.count) + ' ' + str(self.income) + ' ' + str(self.boosts[0].count) + ' ' +
                    str(self.boosts[1].count) + ' ' + str(self.boosts[2].count) + ' ' + str(self.boosts[3].count))

    def exit(self):
        self.save_data()
        sys.exit()

    def handle_events(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_is_clicked = pygame.mouse.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit()

        for i in range(0, len(self.boosts)):
            if self.boosts_buttons[i].x < mouse_pos[0] < self.boosts_buttons[i].x + self.boosts_buttons[i].size and \
               self.boosts_buttons[i].y < mouse_pos[1] < self.boosts_buttons[i].y + self.boosts_buttons[i].size:
                if mouse_is_clicked[0] and not self.boosts_buttons[i].was_clicked:
                    self.boosts_buttons[i].was_clicked = True
                elif not mouse_is_clicked[0] and self.boosts_buttons[i].was_clicked:
                    if self.count >= self.boosts[i].cost:
                        self.boosts[i].count += 1
                        self.count -= self.boosts[i].cost
                        self.income += self.boosts[i].income
                    self.boosts_buttons[i].was_clicked = False

        if ((mouse_pos[0] - self.cookie_button.x) ** 2 + (mouse_pos[1] - self.cookie_button.y) ** 2) ** 0.5 < \
                self.cookie_button.size:
            if mouse_is_clicked[0] and not self.cookie_button.was_clicked:
                self.cookie_button.was_clicked = True
            elif not mouse_is_clicked[0] and self.cookie_button.was_clicked:
                self.count += self.cookie_add
                self.cookie_button.was_clicked = False

        if self.reset_button.x < mouse_pos[0] < self.reset_button.x + self.reset_button.size and \
                self.reset_button.y < mouse_pos[1] < self.reset_button.y + self.reset_button.size and \
                mouse_is_clicked[0]:
            self.count = 0
            self.income = 0
            for i in self.boosts:
                i.count = 0

        if self.exit_button.x < mouse_pos[0] < self.exit_button.x + self.exit_button.size and \
                self.exit_button.y < mouse_pos[1] < self.exit_button.y + self.exit_button.size and mouse_is_clicked[0]:
            self.exit()

    def update(self):
        if time.time() - self.prev_update_count >= self.time_between_update:
            self.prev_update_count = time.time()
            for i in self.boosts:
                self.count += i.count * i.income

    def draw(self):
        self.surface.fill((0, 0, 0))

        for i in self.boosts_buttons:
            i.draw()
        self.cookie_button.draw()
        self.surface.blit(self.make_text('score:     ' + str(self.count)), (500, 500))
        self.surface.blit(self.make_text('income:  ' + str(self.income)), (500, 520))

        self.reset_button.draw()
        self.exit_button.draw()
        self.surface.blit(self.reset_text, (610, 30))
        self.surface.blit(self.exit_text, (610, 130))

        for i in range(0, len(self.boosts)):
            self.surface.blit(self.make_text('BUY', (0, 0, 0)), (self.boosts_buttons[i].x + 5,
                                                                 self.boosts_buttons[i].y + 10))

            self.surface.blit(self.make_text('cost: ' + str(self.boosts[i].cost)),
                              (self.boosts_buttons[i].x + self.boosts_buttons[i].size + 20,
                               self.boosts_buttons[i].y))

            self.surface.blit(self.make_text('count: ' + str(self.boosts[i].count)),
                              (self.boosts_buttons[i].x + self.boosts_buttons[i].size + 20,
                               self.boosts_buttons[i].y + 22))

            self.surface.blit(self.make_text('boost: ' + str(self.boosts[i].income)),
                              (self.boosts_buttons[i].x + self.boosts_buttons[i].size + 150,
                               self.boosts_buttons[i].y + 11))

    def start(self):
        self.make_surface()
        self.make_font()
        self.load_data()
        self.render_text()

        self.run()

    def run(self):
        running = True
        while running:
            self.handle_events()
            self.update()
            self.draw()

            pygame.display.update()
            pygame.time.Clock().tick(self.fps)
