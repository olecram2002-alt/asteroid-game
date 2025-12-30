import pygame, math
from settings import *
from random import randint

class Celestial_body(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        position = self.calculate_position0()
        velocity = self.calculate_velocity0(position)
        self.pos = pygame.math.Vector2(position)
        self.vel = pygame.math.Vector2(velocity)
        self.acc = pygame.math.Vector2(0,0)

        for group in self.groups():
            if group.name == 'asteroids':
                self.asteroids_group = group
            elif group.name == 'collide_sprites':
                self.collide_group = group

        #sprite atributes
        raw_image = self.load_assets()
        self.original_image = pygame.transform.scale_by(raw_image, scale_factor)
        self.image = self.original_image
        self.rect = self.image.get_rect(center = self.pos)

    def calculate_position0(self)->tuple:
        x,y = width/2, height/2
        screen_radius = math.sqrt(width**2 + height**2)/2 
        angle = math.radians(randint(0,360))

        position = (x + screen_radius*math.cos(angle), y + screen_radius*math.sin(angle))

        return position
    
    def calculate_velocity0(self, position:tuple)->tuple:
        x,y = position
        index = randint(0,1)
        velocity_magnitud = randint(0,4)

        if x > 0 and y > 0 :
            if index: velocity = (0,-1*velocity_magnitud)
            else: velocity = (-1*velocity_magnitud,0)
        
        elif x > 0 and y < 0 :
            if index: velocity = (0,1*velocity_magnitud)
            else: velocity = (-1*velocity_magnitud,0)

        elif x < 0 and y < 0 :
            if index: velocity = (0,1*velocity_magnitud)
            else: velocity = (1*velocity_magnitud,0)

        elif x < 0 and y > 0:
            if index: velocity = (0,-1*velocity_magnitud)
            else: velocity = (1*velocity_magnitud,0)

        return velocity


    def load_assets(self):
        raise NotImplementedError('Subclass has to implement this method')

    def update(self):
        self.move()

    def move(self):
        force = pygame.math.Vector2(0,0)

        for sprite in self.asteroids_group:
            if sprite is self:
                continue
            force_d:pygame.math.Vector2 = sprite.pos - self.pos
            force_d.normalize()
            force_m = (G * self.mass*sprite.mass)/self.pos.distance_squared_to(sprite.pos)
            force_d.scale_to_length(force_m)

            force += force_d

        self.acc = force/self.mass
        self.vel += self.acc
        self.pos += self.vel

        self.rect.center = self.pos

        self.acc *= 0


class Asteroid(Celestial_body):
    def __init__(self, type_:str, *groups):
        self.type = type_
        super().__init__(*groups)

    def load_assets(self)->pygame.Surface:
        index = randint(1,3)
        #load images
        match self.type:
            case 'a-small':
                self.mass = 200

            case 'a-medium':
                raw_image = pygame.image.load(f'sprites/medium_sz_asteroid-{index}.png')
                self.mass = 400

            case 'a-large':
                self.mass = 600
        
        return raw_image


        
        
                



