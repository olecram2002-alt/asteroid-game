import pygame
from settings import *

class Planet(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.pos = pygame.math.Vector2(width/2, height/2)
        self.mass = 4000 #kg
        
        #planet
        raw_planet_image = pygame.image.load('sprites/planet.png').convert_alpha()
        self.original_p_image = pygame.transform.scale_by(raw_planet_image, scale_factor)
        self.planet_angle = 0

        #clouds
        raw_clouds_image = pygame.image.load('sprites/clouds.png').convert_alpha()
        self.original_c_image = pygame.transform.scale_by(raw_clouds_image, scale_factor)
        self.clouds_angle = 0

        #transparent surface
        self.image = pygame.Surface((self.original_c_image.get_width(),self.original_c_image.get_height()),pygame.SRCALPHA)

        self.image.blit(self.original_p_image,(0,0))
        self.image.blit(self.original_c_image,(0,0))

        self.rect = self.image.get_rect(center = self.pos)


    def update(self):
        self.rotate()


    def rotate(self):
        self.planet_angle += 0.25
        self.clouds_angle +=0.1

        planet = pygame.transform.rotate(self.original_p_image, self.planet_angle)
        clouds = pygame.transform.rotate(self.original_c_image, self.clouds_angle)

        rect_c = clouds.get_rect()
        rect_p = planet.get_rect(center = rect_c.center)
        self.image = pygame.Surface(rect_c.size, pygame.SRCALPHA)

        self.image.blit(planet, rect_p.topleft)
        self.image.blit(clouds, rect_c)

        self.rect = self.image.get_rect(center = self.pos)

