import pygame
from player import Player
from planet import Planet
from asteroid import Asteroid
from random import randint

def center_collision(sprite_a, sprite_b):
    match sprite_b.type:
        case 'a-small': distance = 10**2
        case 'a-medium' : distance = 30**2
        case 'a-large' : distance = 50**2
        
    if sprite_a.position.distance_squared_to(sprite_b.position) <= distance:
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
        odds = randint(1,10)
        if odds == 1:
            type_ = 'a-small'
        elif 1 < odds <= 7:
            type_ = 'a-medium'
        elif 7 < odds <= 10:
            type_ = 'a-large'
        Asteroid(type_, self.visible_sprites, self.collide_sprites, self.asteroids)
        print('created')


    def collision_planet_check(self):
        for sprite in self.collide_sprites:
            match sprite.type:
                case 'a-samll': radius = 165**2 #165 is half of the lenght of the planet sprite

                case 'a-medium' : radius = 170**2

                case 'a-large' : radius = 220**2

            if self.planet.position.distance_squared_to(sprite.position) < radius: 
                sprite.explode('planet')

    
    def collision_bullet_check(self):
        collisions = pygame.sprite.groupcollide(self.bullet_sprites, self.collide_sprites, True, False, 
                                                collided= center_collision)
        
        for bullet in collisions:
            hit_bodies = collisions[bullet]

            for bodie in hit_bodies:
                bodie.life -= self.player.damage
                bodie.small_explode_sound.play()
                if bodie.life <= 0 :
                    bodie.explode('bullet')

            