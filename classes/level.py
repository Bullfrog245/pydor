'''
Functionality for the dungeon map.
'''

import json
import pygame
from os import listdir
from os.path import isfile, join

import state
from classes.config import LEVEL


class Level():
    '''Functionality for the dungeon map.'''

    def __init__(self):
        # Level
        self.maps_loaded = False
        self.level_data = {}
        self.load_maps()

        self.highlight_selected = False
        self.selected_x = 0
        self.selected_y = 0

        # Avatar
        self.pos = (14, 14)
        self.facing = 0
        self.direction = [
            (0, -1),
            (1, 0),
            (0, 1),
            (-1, 0)
        ]
        self.tiles = []

    def load_maps(self):
        '''Load the map for the current level from maps/level-#.json'''
        if self.maps_loaded:
            return

        print('Initializing map data...')
        maps = [f for f in listdir('maps') if isfile(join('maps', f))]

        for map in maps:
            if 'level-' in map:
                with open('maps/' + map, 'r', encoding='utf-8') as map_file:
                    level = json.load(map_file)
                    self.level_data[level['level']] = level
                    print("Loaded " + map)

        # Ensure we only load maps once
        self.maps_loaded = True
        print('')

    def save_map(self):
        map = 'level-' + str(self.level) + '.json'
        print('Saving map data...')

        # Clean up map data that exists only for the editor
        data = self.level_data[self.level]
        for y in range(0, int(len(data['data']))):
            for x in range(0, int(len(data['data'][y]))):
                if 'selected' in data['data'][y][x]:
                    del data['data'][y][x]['selected']
                if 'coords' in data['data'][y][x]:
                    del data['data'][y][x]['coords']

        with open('maps/' + map, 'w', encoding='utf-8') as map_file:
            json.dump(data, map_file)
        print('Saved ' + map)

    def get_levels(self):
        levels = []
        for level in self.level_data:
            levels.append('Level ' + str(level))
        return levels

    def set_level(self, level):
        self.level = level

    def draw(self, surface):
        '''Draw the map to the specified surface'''
        rect = pygame.Rect((0, 0), (LEVEL.WIDTH, LEVEL.HEIGHT))
        pygame.draw.rect(surface, LEVEL.BG_COLOR, rect)
        pygame.draw.rect(surface, LEVEL.BORDER_COLOR, rect, 1)

        # Grid is 17 offset 3
        # Decorations are 11x11

        if 2 == state.mode or 9 == state.mode:
            data = self.level_data[self.level]['data']
            offset_x = 30
            offset_y = 30

            # Check if the mouse was clicked inside the map area. If not, don't
            # process further collision checks.
            if self.highlight_selected:
                if not pygame.Rect((offset_x, offset_y), (LEVEL.WIDTH, LEVEL.HEIGHT)).collidepoint(pygame.mouse.get_pos()):
                    self.highlight_selected = False

            # FOR DEBUGGING
            for y in range(0, int(len(data))):
                if (y >= LEVEL.GRID_HEIGHT):
                    raise Exception('Map height out-of-bounds')

                for x in range(0, int(len(data[y]))):
                    if (x >= LEVEL.GRID_WIDTH):
                        raise Exception('Map width out-of-bounds')

                    grid_x = (x * LEVEL.GRID) - (x * LEVEL.GUTTER)
                    grid_y = (y * LEVEL.GRID) - (y * LEVEL.GUTTER)

                    rect = pygame.Rect((grid_x, grid_y), (LEVEL.GRID, LEVEL.GRID))

                    pygame.draw.rect(surface, (0, 0, 0), rect)
                    # if ((x + y) % 2) == 0:
                    #     pygame.draw.rect(surface, (90, 90, 90), rect)
                    # else:
                    #     pygame.draw.rect(surface, (50, 50, 50), rect)

                    pygame.draw.rect(surface, (0, 0, 0), rect, 3)
                    # pygame.draw.line(surface, (255, 0, 0), (grid_x, grid_y), (grid_x + 4, grid_y))
                    # pygame.draw.line(surface, (255, 0, 0), (grid_x, grid_y), (grid_x, grid_y + 4))

            for y in range(0, int(len(data))):
                if (y >= LEVEL.GRID_HEIGHT):
                    raise Exception('Map height out-of-bounds')

                for x in range(0, int(len(data[y]))):
                    if (x >= LEVEL.GRID_WIDTH):
                        raise Exception('Map width out-of-bounds')

                    grid_x = (x * LEVEL.GRID) - (x * LEVEL.GUTTER)
                    grid_y = (y * LEVEL.GRID) - (y * LEVEL.GUTTER)

                    # If in editor mode, check if the MOUSEBUTTONUP occured
                    # within the bounds of a map grid.
                    if self.highlight_selected:
                        col_x = grid_x + offset_x + 1
                        col_y = grid_y + offset_y + 1
                        length = LEVEL.GRID - (LEVEL.GUTTER)

                        if pygame.Rect((col_x, col_y), (length, length)).collidepoint(pygame.mouse.get_pos()):
                            self.selected_x = x
                            self.selected_y = y
                            print((self.selected_x, self.selected_y))
                            self.level_data[self.level]['data'][y][x]['selected'] = True
                        else:
                            self.level_data[self.level]['data'][y][x]['selected'] = False

                    for callable, args in data[y][x].items():
                        # Check if callable is defined
                        if (not hasattr(self, 'draw_' + callable)):
                            raise Exception('Invalid map entity ' + callable)

                        getattr(self, 'draw_' + callable)(surface, (grid_x, grid_y), args)

            # Draw the right and bottom walls
            x = x + 1
            y = y + 1
            grid_x = (x * LEVEL.GRID) - (x * LEVEL.GUTTER)
            grid_y = (y * LEVEL.GRID) - (y * LEVEL.GUTTER)
            pygame.draw.rect(surface, LEVEL.WALL_COLOR, pygame.Rect((1, 1), (grid_x + 1, grid_y + 1)), 1)
            # pygame.draw.line(surface, LEVEL.WALL_COLOR, (grid_x + 1, 0), (grid_x + 1, grid_y + 1))
            # pygame.draw.line(surface, LEVEL.WALL_COLOR, (0, grid_y + 1), (grid_x + 1, grid_y + 1))

            self.highlight_selected = False

            if 2 == state.mode:
                self.draw_avatar(surface)

    def draw_coords(self, surface, pos, args):
        pass

    # Walls use "CSS" notation (top, right, bottom, left)
    def draw_walls(self, surface, pos, args):
        x = pos[0] + 1
        y = pos[1] + 1
        length = LEVEL.GRID - LEVEL.GUTTER

        if (args[0]):
            pygame.draw.line(surface, LEVEL.WALL_COLOR, (x, y), (x + length, y))

        # if (args[1]):
        #     pygame.draw.line(surface, LEVEL.WALL_COLOR, (x + LEVEL.GRID, y), (x + LEVEL.GRID, y + LEVEL.GRID))

        # if (args[2]):
        #     pygame.draw.line(surface, LEVEL.WALL_COLOR, (x, y + LEVEL.GRID), (x + LEVEL.GRID, y + LEVEL.GRID))

        if (args[3]):
            pygame.draw.line(surface, LEVEL.WALL_COLOR, (x, y), (x, y + length))

    # Walls use "CSS" notation (top, right, bottom, left)
    def draw_doors(self, surface, pos, args):
        x = pos[0] + 1
        y = pos[1] + 1
        length = LEVEL.GRID - LEVEL.GUTTER

        if (args[0]):
            pygame.draw.line(surface, LEVEL.WALL_COLOR, (x, y), (x + 4, y))
            pygame.draw.line(surface, LEVEL.WALL_COLOR, (x + 5, y - 1), (x + 5, y + 1))
            pygame.draw.line(surface, LEVEL.WALL_COLOR, (x + (length - 4), y), (x + length, y))
            pygame.draw.line(surface, LEVEL.WALL_COLOR, (x + (length - 5), y - 1), (x + (length - 5), y + 1))

        # if (args[1]):
        #     pygame.draw.line(surface, LEVEL.WALL_COLOR, (x + LEVEL.GRID, y), (x + LEVEL.GRID, y + 4))
        #     pygame.draw.line(surface, LEVEL.WALL_COLOR, (x + (LEVEL.GRID - 1), y + 4), (x + (LEVEL.GRID + 1), y + 4))
        #     pygame.draw.line(surface, LEVEL.WALL_COLOR, (x + LEVEL.GRID, y + (LEVEL.GRID - 4)), (x + LEVEL.GRID, y + LEVEL.GRID))
        #     pygame.draw.line(surface, LEVEL.WALL_COLOR, (x + (LEVEL.GRID - 1), y + (LEVEL.GRID - 4)), (x + (LEVEL.GRID + 1), y + (LEVEL.GRID - 4)))

        # if (args[2]):
        #     pygame.draw.line(surface, LEVEL.WALL_COLOR, (x, y + LEVEL.GRID), (x + 4, y + LEVEL.GRID))
        #     pygame.draw.line(surface, LEVEL.WALL_COLOR, (x + 4, y + (LEVEL.GRID - 1)), (x + 4, y + (LEVEL.GRID + 1)))
        #     pygame.draw.line(surface, LEVEL.WALL_COLOR, (x + (LEVEL.GRID - 4), y + LEVEL.GRID), (x + LEVEL.GRID, y + LEVEL.GRID))
        #     pygame.draw.line(surface, LEVEL.WALL_COLOR, (x + (LEVEL.GRID - 4), y + (LEVEL.GRID - 1)), (x + (LEVEL.GRID - 4), y + (LEVEL.GRID + 1)))

        if (args[3]):
            pygame.draw.line(surface, LEVEL.WALL_COLOR, (x, y), (x, y + 4))
            pygame.draw.line(surface, LEVEL.WALL_COLOR, (x - 1, y + 5), (x + 1, y + 5))
            pygame.draw.line(surface, LEVEL.WALL_COLOR, (x, y + (length - 4)), (x, y + length))
            pygame.draw.line(surface, LEVEL.WALL_COLOR, (x - 1, y + (length - 5)), (x + 1, y + (length - 5)))

    def draw_rock(self, surface, pos, args):
        if args:
            x = pos[0] + 3
            y = pos[1] + 3
            length = LEVEL.GRID - LEVEL.GUTTER - LEVEL.GUTTER
            pygame.draw.rect(surface, LEVEL.WALL_COLOR, pygame.Rect((x, y), (length, length)))

    def draw_selected(self, surface, pos, args):
        if args:
            x = pos[0] + 3
            y = pos[1] + 3
            length = LEVEL.GRID - LEVEL.GUTTER - LEVEL.GUTTER
            pygame.draw.rect(surface, (255, 0, 0), pygame.Rect((x, y), (length, length)))

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

        if (0 <= y < len(self.level_data[self.level]['data'])) and (0 <= x < len(self.level_data[self.level]['data'][y])):
            current = self.level_data[self.level]['data'][y][x]

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
            if 2 == state.mode:
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

            if 9 == state.mode:
                if e.type == pygame.MOUSEBUTTONUP:
                    self.highlight_selected = True

    def add_wall(self, direction):
        self.add_positional(direction, 'walls')

    def add_door(self, direction):
        self.add_positional(direction, 'doors')

    def add_positional(self, direction, key):
        tile = self.level_data[self.level]['data'][self.selected_y][self.selected_x]

        if self.selected_y + 1 < len(self.level_data[self.level]['data']):
            down = self.level_data[self.level]['data'][self.selected_y + 1][self.selected_x]
        else:
            down = False

        if self.selected_x + 1 < len(self.level_data[self.level]['data'][self.selected_y]):
            right = self.level_data[self.level]['data'][self.selected_y][self.selected_x + 1]
        else:
            right = False

        tile['selected'] = True

        if key not in tile:
            tile[key] = [0, 0, 0, 0]
        if down and key not in down:
            down[key] = [0, 0, 0, 0]
        if right and key not in right:
            right[key] = [0, 0, 0, 0]

        if 'up' == direction:
            if tile[key][0]:
                tile[key][0] = 0
            else:
                tile[key][0] = 1
        if 'right' == direction:
            if tile[key][1]:
                tile[key][1] = 0
                if right:
                    right[key][3] = 0
            else:
                tile[key][1] = 1
                if right:
                    right[key][3] = 1
        if 'down' == direction:
            if tile[key][2]:
                tile[key][2] = 0
                if down:
                    down[key][0] = 0
            else:
                tile[key][2] = 1
                if down:
                    down[key][0] = 1
        if 'left' == direction:
            if tile[key][3]:
                tile[key][3] = 0
            else:
                tile[key][3] = 1

        self.level_data[self.level]['data'][self.selected_y][self.selected_x] = tile
        if right:
            self.level_data[self.level]['data'][self.selected_y][self.selected_x + 1] = right
        if down:
            self.level_data[self.level]['data'][self.selected_y + 1][self.selected_x] = down

    def add_rock(self):
        tile = self.level_data[self.level]['data'][self.selected_y][self.selected_x]

        if 'rock' in tile:
            del(tile['rock'])
        else:
            tile['rock'] = True
