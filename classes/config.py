'''
Configuration settings.
'''


class SCREEN:
    '''Main game screen configuration'''
    WIDTH = 1280
    HEIGHT = 720


class MENU:
    '''Menu bar surface configuration'''
    WIDTH = 1280
    HEIGHT = 30
    SURFACE_X = 0
    SURFACE_Y = 0

    BG_COLOR = (255, 255, 230)
    BORDER_COLOR = (0, 0, 0)


class CHARACTER:
    '''Character surface configuration'''
    WIDTH = 350
    HEIGHT = 550
    SURFACE_X = 0
    SURFACE_Y = 30

    BG_COLOR = (195, 195, 195)
    BORDER_COLOR = (0, 0, 0)


class LEVEL:
    '''Level surface configuration'''
    WIDTH = 450
    HEIGHT = 450
    SURFACE_X = 350
    SURFACE_Y = 270  # MENU + DUNGEON

    GRID = 17
    GUTTER = 3
    GRID_WIDTH = 30
    GRID_HEIGHT = 30

    BG_COLOR = (195, 195, 195)
    BORDER_COLOR = (0, 0, 0)
    WALL_COLOR = (255, 255, 255)


class CITY:
    '''Dungeon surface configuration'''
    WIDTH = 930
    HEIGHT = 240
    SURFACE_X = 350
    SURFACE_Y = 30

    BG_COLOR = (195, 195, 195)
    BORDER_COLOR = (0, 0, 0)


class DUNGEON:
    '''Dungeon surface configuration'''
    WIDTH = 930
    HEIGHT = 240
    SURFACE_X = 350
    SURFACE_Y = 30

    BG_COLOR = (195, 195, 195)
    BORDER_COLOR = (0, 0, 0)


class PARTY:
    '''Party surface configuration'''
    WIDTH = 350
    HEIGHT = 140
    SURFACE_X = 0
    SURFACE_Y = 580

    BG_COLOR = (195, 195, 195)
    BORDER_COLOR = (0, 0, 0)


class INVENTORY:
    '''Inventory surface configuration'''
    WIDTH = 480
    HEIGHT = 310
    SURFACE_X = 800
    SURFACE_Y = 270

    BG_COLOR = (195, 195, 195)
    BORDER_COLOR = (0, 0, 0)


class MESSAGES:
    '''Messages surface configuration'''
    WIDTH = 480
    HEIGHT = 140
    SURFACE_X = 800
    SURFACE_Y = 580

    BG_COLOR = (195, 195, 195)
    BORDER_COLOR = (0, 0, 0)


class MODAL:
    '''Modal surface configuration'''
    WIDTH = 640
    HEIGHT = 480
    SURFACE_X = 0
    SURFACE_Y = 0
    BG_COLOR = (195, 195, 195)
