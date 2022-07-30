'''
Managment for the game state.
'''

import sys
import pygame
import pygame_gui

import state
from classes.config import SCREEN
from classes.config import MENU
from classes.config import CHARACTER
from classes.config import CITY
from classes.config import DUNGEON
from classes.config import LEVEL
from classes.config import INVENTORY
from classes.config import PARTY
from classes.config import MESSAGES
from classes.config import MODAL

from classes.character import Character
from classes.city import City
from classes.dungeon import Dungeon
from classes.inventory import Inventory
from classes.menu import Menu
from classes.messages import Messages
from classes.party import Party
from classes.level import Level
from classes.debug import Debug


class GameManager():
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN.WIDTH, SCREEN.HEIGHT), 0, 32)

        state.clock = pygame.time.Clock()
        state.ui = pygame_gui.UIManager((SCREEN.WIDTH, SCREEN.HEIGHT))

        # 0 - Main menu
        # 1 - Town
        # 2 - Dungeon
        self.mode = 0

        self.objects = {
            "menu": {
                "object": Menu(),
                "surface": pygame.Surface((MENU.WIDTH, MENU.HEIGHT)).convert(),
                "coords": (MENU.SURFACE_X, MENU.SURFACE_Y)
            },
            "character": {
                "object": Character(),
                "surface": pygame.Surface((CHARACTER.WIDTH, CHARACTER.HEIGHT)).convert(),
                "coords": (CHARACTER.SURFACE_X, CHARACTER.SURFACE_Y)
            },
            "city": {
                "object": City(),
                "surface": pygame.Surface((CITY.WIDTH, CITY.HEIGHT)).convert(),
                "coords": (CITY.SURFACE_X, CITY.SURFACE_Y)
            },
            "dungeon": {
                "object": Dungeon(),
                "surface": pygame.Surface((DUNGEON.WIDTH, DUNGEON.HEIGHT)).convert(),
                "coords": (DUNGEON.SURFACE_X, DUNGEON.SURFACE_Y)
            },
            "level": {
                "object": Level(1),
                "surface": pygame.Surface((LEVEL.WIDTH, LEVEL.HEIGHT)).convert(),
                "coords": (LEVEL.SURFACE_X, LEVEL.SURFACE_Y)
            },
            "inventory": {
                "object": Inventory(),
                "surface": pygame.Surface((INVENTORY.WIDTH, INVENTORY.HEIGHT)).convert(),
                "coords": (INVENTORY.SURFACE_X, INVENTORY.SURFACE_Y)
            },
            "party": {
                "object": Party(),
                "surface": pygame.Surface((PARTY.WIDTH, PARTY.HEIGHT)).convert(),
                "coords": (PARTY.SURFACE_X, PARTY.SURFACE_Y)
            },
            "messages": {
                "object": Messages(),
                "surface": pygame.Surface((MESSAGES.WIDTH, MESSAGES.HEIGHT)).convert(),
                "coords": (MESSAGES.SURFACE_X, MESSAGES.SURFACE_Y)
            },
            "modal": pygame.Surface((MODAL.WIDTH, MODAL.HEIGHT)).convert(),
        }

        self.debug = Debug()
        self.debug_enabled = False

    def enable_debug(self):
        self.debug_enabled = True

    def change_mode(self, mode):
        self.mode = mode

    def get_surface(self, surface):
        return self.surfaces[surface]

    def tick(self, clock):
        # Process user interaction. Save the events list for processing by
        # other modules.
        self.events = pygame.event.get()
        for e in self.events:
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            state.ui.process_events(e)

        # Process GUI actions.
        state.ui.update(state.time_delta)

        # Depending on the game mode, process game logic.
        if (0 == self.mode):
            pass
        elif (1 == self.mode):
            objects = ['menu', 'character', 'city', 'inventory', 'party', 'messages']
            pass
        elif (2 == self.mode):
            objects = ['menu', 'character', 'dungeon', 'level', 'inventory', 'party', 'messages']
        else:
            raise Exception('Invalid game mode ' + self.mode)

        for o in objects:
            surface = self.objects[o]['surface']
            self.objects[o]['object'].handle_keys(self.events)
            self.objects[o]['object'].draw(surface)
            self.screen.blit(surface, self.objects[o]['coords'])

        state.ui.draw_ui(self.screen)

        if (self.debug_enabled):
            self.debug.fps_counter(clock, self.screen)
