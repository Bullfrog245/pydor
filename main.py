'''
A dungeon crawler based heavily on the Windows 3.1 classic Modor.
'''

import pygame

import state
from classes.game_manager import GameManager


def main():
    '''The main game loop.'''

    pygame.init()
    pygame.key.set_repeat(450, 45)  # Allow holding keys to repeat actions

    state.gm = GameManager()
    state.gm.change_mode(1)

    while True:
        state.time_delta = state.clock.tick(60) / 1000.0
        state.gm.tick(state.clock)
        pygame.display.update()


main()
