import pygame


class Button:
    def __init__(self, x, y, size, shape, surface, color=(255, 255, 255)):
        self.x = x
        self.y = y
        self.size = size
        self.shape = shape
        self.surface = surface
        self.was_clicked = False
        self.color = color

    def draw(self):
        if self.shape == 'rect':
            pygame.draw.rect(self.surface, self.color, (self.x + self.was_clicked * 5, self.y + self.was_clicked * 5,
                                                        self.size - self.was_clicked * 10,
                                                        self.size - self.was_clicked * 10))
        else:
            pygame.draw.circle(self.surface, (101, 67, 33), (self.x, self.y), self.size - self.was_clicked * 10)
