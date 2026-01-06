import pygame
import settings as s
import random
import math

class Ammo(pygame.sprite.Sprite):
    def __init__(self, angle, position, *groups):
        super().__init__(*groups)

        rad_angle = math.radians(angle+90)
        self.direction = pygame.math.Vector2(math.cos(rad_angle), -math.sin(rad_angle))
        self.angle = angle

        self.position = self.get_position(position)
        self.get_visuals()

        self.velocity = self.direction*s.atributes['bullet_speed']

        self.damage = self.get_damage()


    def get_position(self, position):
        return self.direction*(32*s.scale_factor) + position #32 is half the lenght of the bullet sprite

    
    def get_visuals(self):
        raw_image = self.get_image()
        self.original_image = pygame.transform.scale_by(raw_image, s.scale_factor)
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center = self.position)


    def get_image(self):
        pass


    def get_damage(self):
        pass


    def move(self):
        self.position += self.velocity
        self.rect.center = self.position


    def update(self):
        self.move()
        if self.position.distance_squared_to((s.width/2, s.height/2)) >= 900**2:
            self.kill()



class Basic(Ammo):
    def __init__(self, angle, position, *groups):
        super().__init__(angle, position, *groups)


    def get_image(self):
        return pygame.image.load('sprites/basic_ammo.png').convert_alpha()
    

    def get_damage(self):
        return s.atributes['damage']*1
    


class Homing(Ammo):
    def __init__(self, angle, position, manager,*groups):
        self.manager = manager
        super().__init__(angle, position, *groups)
        

    def get_image(self):
        return pygame.image.load('sprites/homing-ammo.png').convert_alpha()
    

    def get_damage(self):
        return s.atributes['damage']*0.5
    

    def move(self):
        self.range = pygame.Rect(0,0,200,200) #200 is range of the homing missles could be an scalable stat
        self.range.center = self.position
        
        hit = self.range.collideobjects(self.manager.collide_sprites.sprites())
        if hit:
            self.direction = (hit.position - pygame.math.Vector2(self.rect.center))
            self.direction.normalize_ip()
            self.velocity = self.direction*(s.atributes['bullet_speed']*0.8)
        super().move()



class Bumerang(Ammo):
    def __init__(self, angle, position, sprite_width, *groups):
        super().__init__(angle, position, *groups)
        self.orientation = random.choice([-1,1])
        self.angle = math.radians(-90)
        self.sprite_width = sprite_width


    def get_image(self):
        return pygame.image.load('sprites/orbiter-ammo.png').convert_alpha()
    

    def get_damage(self):
        return s.atributes['damage']*2
    

    def move(self):
        self.angle += math.radians(s.atributes['bullet_speed']*0.5*self.orientation)
        x,y = s.width/2, s.height/2
        radius = 100*s.scale_factor + self.sprite_width

        self.position = pygame.math.Vector2(x + radius*math.cos(self.angle), (y + radius*math.sin(self.angle)))
        self.rect.center = self.position


    def update(self):
        self.move()
        if self.angle >= math.radians(270) or self.angle <= math.radians(-450):
            self.kill()



class Laser(Ammo):
    def __init__(self, angle, position, *groups):
        super().__init__(angle, position, *groups)
        self.time_created = pygame.time.get_ticks()


    def get_position(self, position):
        return self.direction*460*s.scale_factor + position #450 is half the size of the laser

    
    def get_image(self):
        return pygame.image.load('sprites/laser-ammo.png').convert_alpha()
    

    def get_damage(self):
        return s.atributes['damage']*0.1
    

    def update(self):
        time_elapsed = pygame.time.get_ticks()

        if time_elapsed - self.time_created >= 50*s.atributes['bullet_speed']:
            self.kill()
        
