import pygame
import ammo 
from player import Player
from planet import Planet
from asteroid import Asteroid
from ui import UI
from menu import Upgrade_Menu
from random import randint

def center_collision(sprite_a, sprite_b, type_):
    match type_:
        case 'bullet': 

            if isinstance(sprite_a, ammo.Laser):
                closest_x = max(sprite_a.rect.left, min(sprite_b.position.x, sprite_a.rect.right))
                closest_y = max(sprite_a.rect.top, min(sprite_b.position.y, sprite_a.rect.bottom))
                closest_point = pygame.math.Vector2(closest_x,closest_y)

                distance = sprite_b.position.distance_to(closest_point)

                return distance < (sprite_b.radius - 10)
            
            distance = sprite_b.radius**2

        case 'asteroid': distance = (sprite_a.radius + sprite_b.radius)**2
        
    return sprite_a.position.distance_squared_to(sprite_b.position) <= distance

    


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
        self.player = Player((600,380), self, self.bullet_sprites, self.visible_sprites)
        self.planet = Planet(self.visible_sprites, self.asteroids)

        #user interface 
        self.ui = UI(self.player, self.planet)

        #menu
        self.upgrade_menu = Upgrade_Menu(self.planet, self)


    def generate_celestial_body(self):
        odds = randint(1,10)
        if odds == 1:
            type_ = 'a-small'
        elif 1 < odds <= 8:
            type_ = 'a-medium'
        elif 8 < odds <= 10:
            type_ = 'a-large'
        Asteroid(type_, self.visible_sprites, self.collide_sprites, self.asteroids)


    def get_xp_max(self):
        x = 0
        while True:
            max_xp = 2**(0.2 * x)
            yield round(max_xp*100)
            x += 1


    def get_upgrade_price(self):
        x = 1
        while True:
            price = x
            yield price
            x += 1


    def collision_planet_check(self):
        for sprite in self.collide_sprites:
            distance = (self.planet.radius + sprite.radius)**2

            if self.planet.position.distance_squared_to(sprite.position) < distance:
                self.planet.get_hit()
                sprite.explode('planet')

    
    def collision_bullet_check(self):
        collisions = pygame.sprite.groupcollide(self.bullet_sprites, self.collide_sprites, False, False, 
                                                collided= lambda a,b: center_collision(a, b, 'bullet'))
        
        for bullet in collisions:
            hit_bodies = collisions[bullet]

            for bodie in hit_bodies:
                bodie.get_hit(bullet, self.player)
                

    def collision_asteroid_check(self):
        asteroid_list = [s for s in self.asteroids if s is not self.planet]
        handled = set()

        for sprite in asteroid_list:
            if sprite is handled or not sprite.alive():
                continue

            self.asteroids.remove(sprite)

            collisions = pygame.sprite.spritecollide(sprite, self.asteroids, False, 
                                    collided= lambda a,b: center_collision(a, b, 'asteroid') if b is not self.planet else False)
            
            for hit in collisions:
                if hit not in handled and hit.alive():
                    sprite.inelastic_collision(hit)
                    handled.add(hit)
                    break

            self.asteroids.add(sprite)
            