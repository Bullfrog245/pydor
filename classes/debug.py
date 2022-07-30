import pygame

class Debug:
    def __init__(self):
        self.font = pygame.font.SysFont("Arial", 18)

    def fps_counter(self, clock, screen):
        fps = int(clock.get_fps())
        fps_t = self.font.render("FPS: {0}".format(fps), True, (255, 0, 0))
        screen.blit(fps_t, (960, 740))
