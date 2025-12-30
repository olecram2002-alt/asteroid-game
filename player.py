import pygame, math
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos:tuple, *groups):
        super().__init__(*groups)

        raw_image = pygame.image.load('sprites/spaceship-1.png').convert_alpha()
        self.original_image = pygame.transform.scale_by(raw_image, scale_factor)
        self.image = self.original_image
        self.rect = self.image.get_rect(center = pos)
        
        self.angle = math.radians(-90)

        #attributes
        self.speed = 2


    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.angle -= math.radians(self.speed)

        if keys[pygame.K_d]:
            self.angle += math.radians(self.speed)


    def move(self):
        self.input()

        x,y = width/2, height/2
        radius = 220
        self.new_position = (x + radius*math.cos(self.angle), y + radius*math.sin(self.angle))

        ship = pygame.transform.rotate(self.original_image, - 90 - math.degrees(self.angle))

        self.image = ship
        self.rect.center = self.new_position


    def update(self):
        self.move()


