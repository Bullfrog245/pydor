'''
Functionality for Dungeon surface.
'''

import pygame

from .config import INVENTORY


class Inventory():
    '''Functionality for Character surface.'''

    def __init__(self):
        self.something = True

    def draw(self, surface):
        rect = pygame.Rect((0, 0), (INVENTORY.WIDTH, INVENTORY.HEIGHT))
        pygame.draw.rect(surface, INVENTORY.BG_COLOR, rect)
        pygame.draw.rect(surface, INVENTORY.BORDER_COLOR, rect, 1)

    def handle_keys(self, events):
        pass
