import pygame, math
from settings import *
from random import randint

class Asteroid(pygame.sprite.Sprite):
    def __init__(self, position:tuple, type_:str, *groups):
        super().__init__(*groups)
        self.type = type_
        index = randint(1,3)
        self.pos = pygame.math.Vector2(position)
        self.vel = pygame.math.Vector2(0,0)
        self.acc = pygame.math.Vector2(0,0)

        for group in self.groups():
            if group.name == 'asteroids':
                self.asteroids_group = group
            elif group.name == 'collide_sprites':
                self.collide_group = group

        #load images
        match self.type:
            case 'a-small':
                self.mass = 20000

            case 'a-medium':
                raw_image = pygame.image.load(f'sprites/medium_sz_asteroid-{index}.png')
                self.mass = 40000

            case 'a-large':
                self.mass = 60000

        #sprite atributes
        self.original_image = pygame.transform.scale_by(raw_image, scale_factor)
        self.image = self.original_image
        self.rect = self.image.get_rect(center = self.pos)


    def update(self):
        self.move()


    def move(self):
        force = pygame.math.Vector2(0,0)

        for sprite in self.asteroids_group:
            if sprite is self:
                continue
            force_d:pygame.math.Vector2 = self.pos - sprite.pos 
            force_d.normalize()
            force_m = (G * self.mass*sprite.mass)/self.pos.distance_squared_to(sprite.pos)
            force_d.scale_to_length(force_m)

            force = force + force_d

        self.acc = force/self.mass
        

            


        
        
                



