'''
Functionality for the top menu.
'''

import pygame

from .config import MENU


class Menu():
    '''Functionality for the top menu.'''

    def __init__(self):
        self.something = True

    def draw(self, surface):
        rect = pygame.Rect((0, 0), (MENU.WIDTH, MENU.HEIGHT))
        pygame.draw.rect(surface, MENU.BG_COLOR, rect)
        pygame.draw.rect(surface, MENU.BORDER_COLOR, rect, 1)

    def handle_keys(self, events):
        pass
