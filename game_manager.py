import pygame
from player import Player
from planet import Planet
from asteroid import Asteroid

class Manager:
    def __init__(self):
        self.screen = pygame.display.get_surface()

        #sprite groups
        self.visible_sprites = pygame.sprite.Group()
        self.visible_sprites.name = 'visible_sprites'

        self.collide_sprites = pygame.sprite.Group()
        self.collide_sprites.name = 'collide_sprites'
        
        self.asteroids = pygame.sprite.Group() 
        self.asteroids.name = 'asteroids'

        #important sprites
        self.player = Player((600,380), self.visible_sprites)
        self.planet = Planet(self.visible_sprites, self.asteroids)

    def generate_celestial_body(self):
        Asteroid('a-medium',self.visible_sprites, self.collide_sprites, self.asteroids)