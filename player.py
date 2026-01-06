import pygame, math
import settings as s
import ammo 
import random

class Player(pygame.sprite.Sprite):
    def __init__(self, pos:tuple, manager, bullet_sprite_group:pygame.sprite.Group, *groups):
        super().__init__(*groups)
        self.bullet_sprites = bullet_sprite_group
        self.manager = manager
        self.xp_max_generator = manager.get_xp_max()

        raw_image = pygame.image.load('sprites/spaceship-1.png').convert_alpha()
        self.original_image = pygame.transform.scale_by(raw_image, s.scale_factor)
        self.image = self.original_image
        self.rect = self.image.get_rect(center = pos)
        
        self.angle = math.radians(-90)

        #attributes
        self.speed = s.atributes['movement_speed']
        self.shotting_speed = s.atributes['shooting_speed']
        self.damage = s.atributes['damage']
        self.max_xp = next(self.xp_max_generator)
        self.xp = 0
        self.level = 0
        self.gems = s.gems

        #shooting
        self.time_last_trigger = 0
        self.shoot_sound = pygame.mixer.Sound('sounds/weapons/sfx_wpn_laser8.wav')
        self.shoot_sound.set_volume(s.efex_volume - 0.2)


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

        x,y = s.width/2, s.height/2
        radius = 100 * s.scale_factor #arbitrary number just feel bad
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
            for i in range(s.weapons['multiple bullet']):
                angle_modifier = 10*((i+1)//2)*(-1)**i # angle output will be  0,10,-10,20,-20
                weapons = []

                for key, value in s.weapons.items():
                    if key == 'multiple bullet' or key == 'comet destroyer' or key == 'small orbiter':
                        continue
                    if value:
                        for i in range(value):
                            weapons.append(key)

                if not random.randint(0,5-min(5,s.atributes['luck'])):
                    weapon_name = random.choice(weapons or ['basic'])
                else: weapon_name = 'basic'

                match weapon_name:
                    case 'basic': ammo.Basic(self.degree_angle + angle_modifier, self.rect.center, self.bullet_sprites, visible_sprites)

                    case 'homing': ammo.Homing(self.degree_angle + angle_modifier, self.rect.center, self.manager, self.bullet_sprites, visible_sprites)

                    case 'bumerang orbit': ammo.Bumerang(self.degree_angle + angle_modifier, self.rect.center, self.rect.width, self.bullet_sprites, visible_sprites)

                    case 'laser': ammo.Laser(self.degree_angle + angle_modifier, self.rect.center, self.bullet_sprites, visible_sprites)

                    case 'black hole': pass
                
                self.shoot_sound.play()
            self.time_last_trigger = current_time


    def xp_handle(self):
        if self.xp >= self.max_xp:
            self.manager.upgrade_menu.create_upgrades()
            s.menu = True
            s.game = False
            self.xp = 0
            self.max_xp = next(self.xp_max_generator)
            self.level += 1

    
    def update(self):
        self.move()
        self.xp_handle()


