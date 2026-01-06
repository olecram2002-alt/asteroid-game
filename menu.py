import pygame
import settings as s

class Upgrade_Menu:
    def __init__(self):
        self.surface = pygame.display.get_surface()
        self.title_font = pygame.font.Font(s.font_location,50)

    def small_update(self):
        pass

    def big_upgrade(self):
        pass

    
    def draw_upgrade_options(self):
        pass


    def display(self):
        background = pygame.Rect(0,0, s.width/2, s.height/2)
        background.center = (s.width/2, s.height/2)
        pygame.draw.rect(self.surface, s.empty_bar_color, background)

        title = self.title_font.render('Upgrade', False, s.font_color)
        title_rect = title.get_rect(center = (s.width/2 , (s.width/4 + 35)))
        self.surface.blit(title, title_rect)

        self.draw_upgrade_options()
 
