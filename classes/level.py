'''
Functionality for the dungeon map.
'''

import json
import pygame

import state
from classes.config import LEVEL


class Level():
    '''Functionality for the dungeon map.'''

    def __init__(self, level):
        # Level
        self.debug = True
        self.level = level
        self.loaded = False
        self.layout = {}
        self.load_map()

        # Avatar
        self.pos = (14, 14)
        self.facing = 0
        self.direction = [
            (0, -1),
            (1, 0),
            (0, 1),
            (-1, 0)
        ]

    def load_map(self):
        '''Load the map for the current level from maps/level-#.json'''
        if self.loaded:
            return

        with open('maps/level-' + str(self.level) + '.json', 'r', encoding='utf-8') as map_file:
            self.layout = json.load(map_file)
            print("MAP LOADED")
            self.loaded = True

    def draw(self, surface):
        '''Draw the map to the specified surface'''
        rect = pygame.Rect((0, 0), (LEVEL.WIDTH, LEVEL.HEIGHT))
        pygame.draw.rect(surface, LEVEL.BG_COLOR, rect)
        pygame.draw.rect(surface, LEVEL.BORDER_COLOR, rect, 1)

        if 2 == state.gm.mode:
            for y in range(0, int(len(self.layout))):
                if (y >= LEVEL.GRID_HEIGHT):
                    raise Exception('Map height out-of-bounds')

                for x in range(0, int(len(self.layout[y]))):
                    if (x >= LEVEL.GRID_WIDTH):
                        raise Exception('Map width out-of-bounds')

                    grid_x = x * LEVEL.GRID
                    grid_y = y * LEVEL.GRID
                    rect = pygame.Rect((grid_x, grid_y), (LEVEL.GRID, LEVEL.GRID))

                    if ((x + y) % 2) == 0:
                        pygame.draw.rect(surface, (20, 20, 20), rect)
                    else:
                        pygame.draw.rect(surface, (10, 10, 10), rect)
                    pygame.draw.line(surface, (0, 0, 0), (grid_x, grid_y), (grid_x + LEVEL.GRID, grid_y))
                    pygame.draw.line(surface, (0, 0, 0), (grid_x, grid_y), (grid_x, grid_y + LEVEL.GRID))

                    for callable, args in self.layout[y][x].items():
                        # Check if callable is defined
                        if (not hasattr(self, 'draw_' + callable)):
                            raise Exception('Invalid map entity ' + callable)

                        getattr(self, 'draw_' + callable)(surface, (grid_x, grid_y), args)

            pygame.draw.line(surface, (0, 0, 0), (LEVEL.WIDTH, 0), (LEVEL.WIDTH, LEVEL.HEIGHT))
            pygame.draw.line(surface, (0, 0, 0), (0, LEVEL.HEIGHT), (LEVEL.WIDTH, LEVEL.HEIGHT))
            self.draw_avatar(surface)

    def draw_coords(self, surface, pos, args):
        pass

    # Walls use "CSS" notation (top, right, bottom, left)
    def draw_walls(self, surface, pos, args):
        x, y = pos

        if (args[0]):
            pygame.draw.line(surface, LEVEL.WALL_COLOR, (x, y), (x + LEVEL.GRID, y))

        if (args[1]):
            pygame.draw.line(surface, LEVEL.WALL_COLOR, (x + LEVEL.GRID, y), (x + LEVEL.GRID, y + LEVEL.GRID))

        if (args[2]):
            pygame.draw.line(surface, LEVEL.WALL_COLOR, (x, y + LEVEL.GRID), (x + LEVEL.GRID, y + LEVEL.GRID))

        if (args[3]):
            pygame.draw.line(surface, LEVEL.WALL_COLOR, (x, y), (x, y + LEVEL.GRID))

    # Walls use "CSS" notation (top, right, bottom, left)
    def draw_doors(self, surface, pos, args):
        x, y = pos

        if (args[0]):
            pygame.draw.line(surface, LEVEL.WALL_COLOR, (x, y), (x + 4, y))
            pygame.draw.line(surface, LEVEL.WALL_COLOR, (x + 4, y - 1), (x + 4, y + 1))
            pygame.draw.line(surface, LEVEL.WALL_COLOR, (x + (LEVEL.GRID - 4), y), (x + LEVEL.GRID, y))
            pygame.draw.line(surface, LEVEL.WALL_COLOR, (x + (LEVEL.GRID - 4), y - 1), (x + (LEVEL.GRID - 4), y + 1))

        if (args[1]):
            pygame.draw.line(surface, LEVEL.WALL_COLOR, (x + LEVEL.GRID, y), (x + LEVEL.GRID, y + 4))
            pygame.draw.line(surface, LEVEL.WALL_COLOR, (x + (LEVEL.GRID - 1), y + 4), (x + (LEVEL.GRID + 1), y + 4))
            pygame.draw.line(surface, LEVEL.WALL_COLOR, (x + LEVEL.GRID, y + (LEVEL.GRID - 4)), (x + LEVEL.GRID, y + LEVEL.GRID))
            pygame.draw.line(surface, LEVEL.WALL_COLOR, (x + (LEVEL.GRID - 1), y + (LEVEL.GRID - 4)), (x + (LEVEL.GRID + 1), y + (LEVEL.GRID - 4)))

        if (args[2]):
            pygame.draw.line(surface, LEVEL.WALL_COLOR, (x, y + LEVEL.GRID), (x + 4, y + LEVEL.GRID))
            pygame.draw.line(surface, LEVEL.WALL_COLOR, (x + 4, y + (LEVEL.GRID - 1)), (x + 4, y + (LEVEL.GRID + 1)))
            pygame.draw.line(surface, LEVEL.WALL_COLOR, (x + (LEVEL.GRID - 4), y + LEVEL.GRID), (x + LEVEL.GRID, y + LEVEL.GRID))
            pygame.draw.line(surface, LEVEL.WALL_COLOR, (x + (LEVEL.GRID - 4), y + (LEVEL.GRID - 1)), (x + (LEVEL.GRID - 4), y + (LEVEL.GRID + 1)))

        if (args[3]):
            pygame.draw.line(surface, LEVEL.WALL_COLOR, (x, y), (x, y + 4))
            pygame.draw.line(surface, LEVEL.WALL_COLOR, (x - 1, y + 4), (x + 1, y + 4))
            pygame.draw.line(surface, LEVEL.WALL_COLOR, (x, y + (LEVEL.GRID - 4)), (x, y + LEVEL.GRID))
            pygame.draw.line(surface, LEVEL.WALL_COLOR, (x - 1, y + (LEVEL.GRID - 4)), (x + 1, y + (LEVEL.GRID - 4)))

    def draw_avatar(self, surface):
        offset = LEVEL.GRID
        x, y = self.pos
        x = x * offset
        y = y * offset

        polygon = [
            [
                (x, y + offset),
                (x + offset, y + offset),
                (x + (offset / 2), y)
            ],
            [
                (x, y),
                (x, y + offset),
                (x + offset, y + (offset / 2))
            ],
            [
                (x, y),
                (x + offset, y),
                (x + (offset / 2), y + offset)
            ],
            [
                (x + offset, y),
                (x + offset, y + offset),
                (x, y + (offset / 2))
            ]
        ]
        pygame.draw.polygon(surface, (255, 0, 255), polygon[self.facing])

    def flip(self):
        if self.facing == 0:
            self.facing = 2
        elif self.facing == 1:
            self.facing = 3
        elif self.facing == 2:
            self.facing = 0
        else:
            self.facing = 1

    def turn(self, direction):
        if (direction == 'right'):
            self.facing = self.facing + 1
        else:
            self.facing = self.facing - 1

        if self.facing > 3:
            self.facing = 0

        if self.facing < 0:
            self.facing = 3

    def move(self):
        if self.check_collision(self.pos, self.direction[self.facing]):
            # Bonk
            pass
        else:
            x, y = self.direction[self.facing]
            self.pos = (self.pos[0] + x, self.pos[1] + y)

    def check_collision(self, pos, direction):
        x, y = pos

        if (0 <= y < len(self.layout)) and (0 <= x < len(self.layout[y])):
            current = self.layout[y][x]

            if direction[1] < 0 and 1 == current['walls'][0]:
                return True  # Wall up
            if direction[0] > 0 and 1 == current['walls'][1]:
                return True  # Wall right
            if direction[1] > 0 and 1 == current['walls'][2]:
                return True  # Wall down
            if direction[0] < 0 and 1 == current['walls'][3]:
                return True  # Wall left
        else:
            return False

    def handle_keys(self, events):
        # Individual key presses
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP:
                    self.move()
                elif e.key == pygame.K_RIGHT:
                    self.turn('right')
                elif e.key == pygame.K_DOWN:
                    self.flip()

                    # If either SHIFT key is being help, flip and move
                    keys = pygame.key.get_pressed()
                    if (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]):
                        self.move()
                elif e.key == pygame.K_LEFT:
                    self.turn('left')
