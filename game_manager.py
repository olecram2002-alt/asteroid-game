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
        
        self.asteroids = pygame.sprite.Group() #gravity check group
        self.asteroids.name = 'asteroids'

        self.bullet_sprites = pygame.sprite.Group()
        self.bullet_sprites.name = 'bullet_sprites'

        #important sprites
        self.player = Player((600,380), self.bullet_sprites, self.visible_sprites)
        self.planet = Planet(self.visible_sprites, self.asteroids)

        print(self.planet.rect.width)

    def generate_celestial_body(self):
        Asteroid('a-medium',self.visible_sprites, self.collide_sprites, self.asteroids)

    def collision_planet_check(self):
        for sprite in self.collide_sprites:
            if self.planet.pos.distance_squared_to(sprite.pos) < 170**2: #165 is half of the lenght of the planet sprite
                sprite.kill()
                sprite.explode()

            