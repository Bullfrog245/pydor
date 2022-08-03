'''
A dungeon crawler based heavily on the Windows 3.1 classic Modor.
'''

import pygame
import pygame_gui

import state
from classes.config import LEVEL
from classes.level import Level


pygame.init()

pygame.display.set_caption('Quick Start')
screen = pygame.display.set_mode((800, 600))

state.mode = 9

background = pygame.Surface((800, 600))
background.fill(pygame.Color('#ffffff'))

level_surface = pygame.Surface((LEVEL.WIDTH, LEVEL.HEIGHT)).convert()

ui = pygame_gui.UIManager((800, 600), 'settings/theme.json')
# ui.add_font_paths("OpenSans", "assets/fonts/OpenSans-Regular.ttf")
# # ui.add_font_paths("cozette", str(ASSET_PATH / "fonts/cozette_bitmap.ttf"))

# fonts = [
#     {"name": "OpenSans", "point_size": 12, "style": "regular"},
#     #{"name": "cozette", "point_size": 12, "style": "regular"},
# ]
# ui.preload_fonts(fonts)


level = Level()
level.set_level(1)

level_options = level.get_levels()
level_select = pygame_gui.elements.UIDropDownMenu(
    relative_rect=pygame.Rect((25, 500), (200, 60)),
    options_list=level_options,
    starting_option=level_options[0],
    manager=ui
)

wall_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((540, 20), (60, 30)), text='Walls', manager=ui)
wall_up = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((540, 45), (60, 30)), text='Up', manager=ui)
wall_right = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((570, 75), (60, 30)), text='Right', manager=ui)
wall_down = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((540, 105), (60, 30)), text='Down', manager=ui)
wall_left = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((510, 75), (60, 30)), text='Left', manager=ui)

door_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((680, 20), (60, 30)), text='Doors', manager=ui)
door_up = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((680, 45), (60, 30)), text='Up', manager=ui)
door_right = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((710, 75), (60, 30)), text='Right', manager=ui)
door_down = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((680, 105), (60, 30)), text='Down', manager=ui)
door_left = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((650, 75), (60, 30)), text='Left', manager=ui)

add_rock = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((510, 150), (60, 60)), text='Rock', manager=ui)
add_water = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((570, 150), (60, 60)), text='Water', manager=ui)

save = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((720, 520), (60, 60)), text='Save', manager=ui)

clock = pygame.time.Clock()
is_running = True

while is_running:
    time_delta = clock.tick(60) / 1000.0
    events = pygame.event.get()
    for e in events:
        if e.type == pygame.QUIT:
            is_running = False

        if e.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
            if e.ui_element == level_select:
                level.set_level(int(e.text.replace('Level ', '')))

        if e.type == pygame_gui.UI_BUTTON_PRESSED:
            if e.ui_element == wall_up:
                level.add_wall('up')
            if e.ui_element == wall_right:
                level.add_wall('right')
            if e.ui_element == wall_down:
                level.add_wall('down')
            if e.ui_element == wall_left:
                level.add_wall('left')

            if e.ui_element == door_up:
                level.add_door('up')
            if e.ui_element == door_right:
                level.add_door('right')
            if e.ui_element == door_down:
                level.add_door('down')
            if e.ui_element == door_left:
                level.add_door('left')

            if e.ui_element == add_rock:
                level.add_rock()

            if e.ui_element == save:
                level.save_map()

        ui.process_events(e)

    ui.update(time_delta)

    screen.blit(background, (0, 0))

    level.handle_keys(events)
    level.draw(level_surface)
    screen.blit(level_surface, (30, 30))

    ui.draw_ui(screen)

    pygame.display.update()
