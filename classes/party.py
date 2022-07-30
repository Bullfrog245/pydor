'''
Functionality for Dungeon surface.
'''

import pygame

from .config import PARTY


class Party():
    '''Functionality for Character surface.'''

    def __init__(self):
        self.something = True

    def draw(self, surface):
        rect = pygame.Rect((0, 0), (PARTY.WIDTH, PARTY.HEIGHT))
        pygame.draw.rect(surface, PARTY.BG_COLOR, rect)
        pygame.draw.rect(surface, PARTY.BORDER_COLOR, rect, 1)

    def handle_keys(self, events):
        pass
