import pygame
from player import Player
from planet import Planet
from asteroid import Asteroid

def center_collision(sprite_a, sprite_b):
    if sprite_a.position.distance_squared_to(sprite_b.position) <= 30**2:
        return True
    else: 
        return False

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

    def generate_celestial_body(self):
        Asteroid('a-medium',self.visible_sprites, self.collide_sprites, self.asteroids)

    def collision_planet_check(self):
        for sprite in self.collide_sprites:
            if self.planet.position.distance_squared_to(sprite.position) < 170**2: #165 is half of the lenght of the planet sprite
                sprite.kill()
                sprite.explode()
    
    def collision_bullet_check(self):
        pygame.sprite.groupcollide(self.bullet_sprites, self.collide_sprites, True, True, 
                                   collided= center_collision)

            