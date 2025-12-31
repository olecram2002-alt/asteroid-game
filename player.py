import pygame, math
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos:tuple, bullet_sprite:pygame.sprite.Group, *groups):
        super().__init__(*groups)
        self.bullet_sprites = bullet_sprite

        raw_image = pygame.image.load('sprites/spaceship-1.png').convert_alpha()
        self.original_image = pygame.transform.scale_by(raw_image, scale_factor)
        self.image = self.original_image
        self.rect = self.image.get_rect(center = pos)
        
        self.angle = math.radians(-90)

        #attributes
        self.speed = 2
        self.shotting_speed = 100

        #shooting
        self.time_last_trigger = 0
        self.shoot_sound = pygame.mixer.Sound('sounds/weapons/sfx_wpn_laser8.wav')
        self.shoot_sound.set_volume(efex_volume)


    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.angle -= math.radians(self.speed)

        if keys[pygame.K_d]:
            self.angle += math.radians(self.speed)

        if keys[pygame.K_SPACE]:
            self.shoot()


    def move(self):
        self.input()

        x,y = width/2, height/2
        radius = 200 
        self.degree_angle = -90 - math.degrees(self.angle) #angle to rotate the sprite

        self.position = (x + radius*math.cos(self.angle), (y + radius*math.sin(self.angle)))

        ship = pygame.transform.rotate(self.original_image, self.degree_angle)

        self.image = ship
        self.rect = self.image.get_rect(center = self.position)


    def shoot(self):
        current_time = pygame.time.get_ticks()
        for group in self.groups():
            if group.name == 'visible_sprites':
                visible_sprites = group

        if current_time - self.time_last_trigger >= self.shotting_speed:
            Ammo(self.degree_angle, self.rect.center, self.bullet_sprites, visible_sprites)
            self.shoot_sound.play()
            self.time_last_trigger = current_time
        
    

    def update(self):
        self.move()



class Ammo(pygame.sprite.Sprite):
    def __init__(self, angle, position, *groups):
        super().__init__(*groups)

        rad_angle = math.radians(angle+90)
        self.direction = pygame.math.Vector2(math.cos(rad_angle), -math.sin(rad_angle))

        self.position = self.direction*64 + position #32 is half the lenght of the bullet sprite
        
        raw_image = pygame.image.load('sprites/basic_ammo.png')
        self.original_image = pygame.transform.scale_by(raw_image,scale_factor)
        self.image = pygame.transform.rotate(self.original_image, angle)
        self.rect = self.image.get_rect(center = self.position)

        self.velocity = self.direction*10


    def move(self):
        self.position += self.velocity
        self.rect.center =self.position


    def update(self):
        self.move()
        if self.position.distance_squared_to((width/2, height/2)) >= 900**2:
            self.kill()





        




