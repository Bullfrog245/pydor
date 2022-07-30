'''
Functionality for Dungeon surface.
'''

import pygame

from .config import MESSAGES


class Messages():
    '''Functionality for Character surface.'''

    def __init__(self):
        self.something = True

    def draw(self, surface):
        rect = pygame.Rect((0, 0), (MESSAGES.WIDTH, MESSAGES.HEIGHT))
        pygame.draw.rect(surface, MESSAGES.BG_COLOR, rect)
        pygame.draw.rect(surface, MESSAGES.BORDER_COLOR, rect, 1)

    def handle_keys(self, events):
        pass
