'''
Functionality for Character surface.
'''

import pygame
import pygame_gui

import state

from classes.config import CITY


class City():
    '''Functionality for Character surface.'''

    def __init__(self):
        container = pygame_gui.core.UIContainer(
            relative_rect=pygame.Rect((CITY.SURFACE_X, CITY.SURFACE_Y), (CITY.WIDTH, CITY.HEIGHT)),
            manager=state.ui
        )
        self.UIPanel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect((0, 0), (CITY.WIDTH, CITY.HEIGHT)),
            starting_layer_height=65535,
            container=container,
            manager=state.ui
        )
        self.UIPanel.hide()

        self.general_store = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((0, 0), (150, 50)),
            text='General Store',
            container=self.UIPanel,
            manager=state.ui
        )
        self.dungeon = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((155, 0), (150, 50)),
            text='Dungeon',
            container=self.UIPanel,
            manager=state.ui
        )

    def handle_keys(self, events):
        for e in events:
            if e.type == pygame_gui.UI_BUTTON_PRESSED:
                if self.general_store == e.ui_element:
                    print('GENERAL STORE')
                if self.dungeon == e.ui_element:
                    print('CHANGING MODE TO 2')
                    state.gm.change_mode(2)

    def draw(self, surface):
        # rect = pygame.Rect((0, 0), (CITY.WIDTH, CITY.HEIGHT))
        # pygame.draw.rect(surface, CITY.BG_COLOR, rect)
        # pygame.draw.rect(surface, CITY.BORDER_COLOR, rect, 1)
        if 1 == state.gm.mode:
            self.UIPanel.show()
        else:
            self.UIPanel.hide()
