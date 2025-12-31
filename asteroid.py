import pygame, math
from settings import *
from random import randint

class Celestial_body(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        position = self.calculate_position0()
        velocity = self.calculate_velocity0(position)
        self.position = pygame.math.Vector2(position)
        self.velocity = pygame.math.Vector2(velocity)
        self.acceleration = pygame.math.Vector2(0,0)

        for group in self.groups():
            if group.name == 'asteroids':
                self.asteroids_group = group
            elif group.name == 'collide_sprites':
                self.collide_group = group

        #sprite atributes
        raw_image = self.load_assets()
        self.original_image = pygame.transform.scale_by(raw_image, scale_factor)
        self.image = self.original_image
        self.rect = self.image.get_rect(center = self.position)

        #sounds
        self.explode_sound = pygame.mixer.Sound('sounds/explotions/sfx_exp_short_hard2.wav')
        self.explode_sound.set_volume(efex_volume)
        self.small_explode_sound = pygame.mixer.Sound('sounds/explotions/sfx_exp_shortest_soft2.wav')
        self.small_explode_sound.set_volume(efex_volume)


    def calculate_position0(self)->tuple:
        x,y = width/2, height/2
        screen_radius = math.sqrt(width**2 + height**2)/2 
        angle = math.radians(randint(0,360))

        position = (x + screen_radius*math.cos(angle), y + screen_radius*math.sin(angle))
        return position
    
    
    def calculate_velocity0(self, position:tuple)->tuple:
        magnitud = randint(4,6)
        if randint(0,1): sign = -1
        else: sign = 1

        origin = pygame.math.Vector2(width/2, height/2)

        direction_center = (origin - position).normalize()
        direction = direction_center.rotate(sign*randint(30,45))

        velocity = direction * magnitud
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
            force_d:pygame.math.Vector2 = sprite.position - self.position
            force_m = (G * self.mass*sprite.mass)/self.position.distance_squared_to(sprite.position)
            force_d.scale_to_length(force_m)

            force += force_d

        self.acceleration = force/self.mass
        self.velocity += self.acceleration
        self.position += self.velocity

        self.rect.center = self.position

        self.acceleration *= 0


    def explode(self, type_:str):
        #animation code for explotion in the future
        self.explode_sound.play()
        self.kill()
        


class Asteroid(Celestial_body):
    def __init__(self, type_:str, *groups):
        self.type = type_
        super().__init__(*groups)


    def load_assets(self)->pygame.Surface:
        index = randint(1,3)
        #load images
        match self.type:
            case 'a-small':
                raw_image = pygame.image.load(f'sprites/small_sz_asteroid-{index}.png')
                self.mass = 100
                self.life = 10

            case 'a-medium':
                raw_image = pygame.image.load(f'sprites/medium_sz_asteroid-{index}.png')
                self.mass = 500
                self.life = 30

            case 'a-large':
                raw_image = pygame.image.load(f'sprites/large_sz_asteroid-{index}.png')
                self.mass = 1000
                self.life = 50
        return raw_image


        
        
                



