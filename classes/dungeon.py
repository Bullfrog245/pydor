'''
Functionality for Dungeon surface.
'''

import pygame
import pygame_gui

import state

from .config import DUNGEON


class Dungeon():
    '''Functionality for Character surface.'''

    def __init__(self):
        container = pygame_gui.core.UIContainer(
            relative_rect=pygame.Rect((DUNGEON.SURFACE_X, DUNGEON.SURFACE_Y), (DUNGEON.WIDTH, DUNGEON.HEIGHT)),
            manager=state.ui
        )
        self.UIPanel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect((0, 0), (DUNGEON.WIDTH, DUNGEON.HEIGHT)),
            starting_layer_height=65535,
            container=container,
            manager=state.ui
        )
        self.UIPanel.hide()

        self.take = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((0, 0), (150, 50)),
            text='Take',
            container=self.UIPanel,
            manager=state.ui
        )

    def handle_keys(self, events):
        for e in events:
            if e.type == pygame_gui.UI_BUTTON_PRESSED:
                if self.take == e.ui_element:
                    print('CHANGING MODE TO 1')
                    state.gm.change_mode(1)

    def draw(self, surface):
        if 2 == state.gm.mode:
            self.UIPanel.show()
        else:
            self.UIPanel.hide()
