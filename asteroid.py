import pygame, math
import ammo
import settings as s
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
        self.setup_visuals()

        #sounds
        self.explode_sound_1 = pygame.mixer.Sound('sounds/explotions/sfx_exp_short_hard2.wav')
        self.explode_sound_1.set_volume(s.efex_volume)
        self.explode_sound_2 = pygame.mixer.Sound('sounds/explotions/sfx_exp_medium6.wav')
        self.explode_sound_2.set_volume(s.efex_volume)
        self.small_explode_sound = pygame.mixer.Sound('sounds/explotions/sfx_exp_shortest_soft2.wav')
        self.small_explode_sound.set_volume(s.efex_volume)

        #distance check for sounds
        center = pygame.math.Vector2(s.width/2, s.height/2)
        if self.position.distance_squared_to(center) <= (s.width**2 + s.height**2)/4:
            self.inrange = True

        else: self.inrange = False


    def calculate_position0(self)->tuple:
        x,y = s.width/2, s.height/2
        screen_radius = math.sqrt(s.width**2 + s.height**2)/2 
        angle = math.radians(randint(0,360))

        position = (x + screen_radius*math.cos(angle), y + screen_radius*math.sin(angle))
        return position
    
    
    def calculate_velocity0(self, position:tuple)->tuple:
        if randint(0,1): sign = -1
        else: sign = 1

        origin = pygame.math.Vector2(s.width/2, s.height/2)

        direction_center = (origin - position).normalize()
        direction = direction_center.rotate(sign * s.angle_spawn_range)

        velocity = direction * s.speed_magnitud
        return velocity
    

    def setup_visuals(self, sprite=False):
        if sprite:
            self.image = sprite.image
        else:
            raw_image = self.load_assets()
            self.original_image = pygame.transform.scale_by(raw_image, s.scale_factor)
            self.image = self.original_image

        self.rect = self.image.get_rect(center = self.position)
        self.radius = self.rect.width/2 - 5 # -10 is just a correction so they overlap for a little bit
        self.mass, self.life, self.xp = s.asteroid_atributes[self.type]
    

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
            force_m = (s.G * self.mass*sprite.mass)/self.position.distance_squared_to(sprite.position)
            force_d.scale_to_length(force_m)

            force += force_d

        self.acceleration = force/self.mass
        self.velocity += self.acceleration
        self.position += self.velocity

        self.rect.center = self.position

        self.acceleration *= 0
    

    def inelastic_collision(self, hit_sprite):
        #asteroid new type
        rank = {}
        reverse_rank = {}
        for index,item in enumerate(s.asteroids_list):
            rank[item] = index + 1
            reverse_rank[index + 1] = item


        val1,val2 = rank[self.type], rank[hit_sprite.type]

        if val1 == val2:
            new_val = min(len(s.asteroids_list), val1 +1) #first variable is the num of asteroids in asteroids_list
        else:
            new_val = max(val1, val2)

        new_type = reverse_rank[new_val]

        #new velocity
        new_velocity = (self.velocity*self.mass + hit_sprite.velocity*hit_sprite.mass)/(self.mass + hit_sprite.mass)

        #asteroid new position and create new asteroid
        self.type = new_type
        if val1 == val2:
            new_position = (self.position + hit_sprite.position)/2

            self.setup_visuals()
        elif val1 > val2:
            new_position = self.position

        else:
            new_position = hit_sprite.position

            self.setup_visuals(hit_sprite)

        self.position = new_position
        self.velocity = new_velocity
        self.rect.center = self.position

        hit_sprite.explode('asteroid')

        
    def explode(self, type_:str):
        #animation code for explotion in the future
        match type_:
            case 'planet':
                self.explode_sound_2.play()
            case 'bullet':
                pass
            case 'asteroid':
                if self.inrange: 
                    self.explode_sound_1.play()
        self.kill()


    def get_hit(self, bullet, player):
        self.life -= bullet.damage
        self.small_explode_sound.play()
        if not isinstance(bullet, ammo.Laser):
            bullet.kill()

        if self.life <= 0:
            player.xp += self.xp
            s.gems += self.calculate_drop(self.type)
            self.explode('bullet')

        
    def calculate_drop(self, type_):
        raise NotImplementedError('Subclass has to implement this method')


class Asteroid(Celestial_body):
    def __init__(self, type_:str, *groups):
        self.type = type_
        super().__init__(*groups)


    def load_assets(self)->pygame.Surface:
        index = randint(1,3)
        #load images
        match self.type:
            case 'a-small': raw_image = pygame.image.load(f'sprites/small_sz_asteroid-{index}.png').convert_alpha()

            case 'a-medium': raw_image = pygame.image.load(f'sprites/medium_sz_asteroid-{index}.png').convert_alpha()

            case 'a-large': raw_image = pygame.image.load(f'sprites/large_sz_asteroid-{index}.png').convert_alpha()

            case 'a-xlarge': raw_image = pygame.image.load(f'sprites/xlarge_sz_asteroid-{index}.png').convert_alpha()

        return raw_image
    

    def calculate_drop(self, type_):
        if type_ == 'a-xlarge':
            return 1
        elif type_ == 'a-large':
            if randint(0,2):
                return 1
            
        return 0
