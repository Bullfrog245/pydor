'''
Functionality for Character surface.
'''

import pygame

from .config import CHARACTER


class Character():
    '''Functionality for Character surface.'''

    def __init__(self):
        self.something = True

    def draw(self, surface):
        rect = pygame.Rect((0, 0), (CHARACTER.WIDTH, CHARACTER.HEIGHT))
        pygame.draw.rect(surface, CHARACTER.BG_COLOR, rect)
        pygame.draw.rect(surface, CHARACTER.BORDER_COLOR, rect, 1)

    def handle_keys(self, events):
        pass
