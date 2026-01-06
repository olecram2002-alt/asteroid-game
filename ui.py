import pygame
from player import Player
from planet import Planet
import settings as s

class UI:
    def __init__(self, player:Player, planet:Planet):
        self.surface = pygame.display.get_surface()
        self.font = pygame.font.Font(s.font_location,40)
        self.planet = planet
        self.player = player
        self.life_max = s.atributes['planet_life']


    def draw_background(self):
        self.xp_bar_rect = pygame.Rect(0,0,s.width,30)
        pygame.draw.rect(self.surface, s.empty_bar_color, self.xp_bar_rect)

        self.life_bar_rect = pygame.Rect(30,60,200,30)
        pygame.draw.rect(self.surface, s.empty_bar_color, self.life_bar_rect)

    
    def draw_stats(self):
        #xp
        self.xp_num = self.player.xp
        self.xp_bar_width = self.xp_num * ((s.width - 10) / self.player.max_xp)

        xp_rect = pygame.Rect(5,5,self.xp_bar_width,20)
        pygame.draw.rect(self.surface, s.xp_bar_color, xp_rect)

        #life
        self.life_num = self.planet.life
        self.life_bar_width = self.life_num * (190 / self.life_max)

        life_rect = pygame.Rect(35,65,self.life_bar_width,20)
        pygame.draw.rect(self.surface, s.life_bar_color, life_rect)


    def draw_text(self):
        xp_text = self.font.render(f'Level: {self.player.level}', False, s.font_color)
        xp_rect = xp_text.get_rect(center=self.xp_bar_rect.center)
        self.surface.blit(xp_text, xp_rect)

        life_text = self.font.render('Life', False, s.font_color)
        life_rect = life_text.get_rect(center=self.life_bar_rect.center)
        self.surface.blit(life_text, life_rect)


    def display(self):
        self.draw_background()
        self.draw_stats()
        self.draw_text()
    

    def game_over(self):
        font1 = pygame.font.Font(s.font_location,100)
        font2 = pygame.font.Font(s.font_location,90)

        text1 = font1.render('GAME OVER', False, s.empty_bar_color)
        rect1 = text1.get_rect(center=(s.width/2, s.height/2))
        self.surface.blit(text1,rect1)

        text2 = font2.render('GAME OVER', False, s.font_color)
        rect2 = text2.get_rect(center=(s.width/2, s.height/2))
        self.surface.blit(text2,rect2)
