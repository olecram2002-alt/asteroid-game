import pygame
import settings as s
import random

class Upgrade_Menu:
    def __init__(self, planet):
        self.surface = pygame.display.get_surface()
        self.title_font = pygame.font.Font(s.font_location,50)
        self.mouse_position = (0,0)
        self.selection_list = []
        self.planet = planet


    def input(self):
        self.mouse_position = pygame.mouse.get_pos()


    def get_selection(self, mouse_position):
        for selection in self.selection_list:
            if selection.rect.collidepoint(mouse_position):

                if selection.type == 'big':
                    s.weapons[selection.name] += selection.mod
                elif selection.name == 'luck':
                    s.atributes['luck'] += selection.mod
                else:
                    s.atributes[selection.name] = round(s.atributes[selection.name]*selection.mod,2)

                    if selection.name == 'planet_life':
                        self.planet.life = s.atributes['planet_life']

                return True
        
        return False


    def create_upgrades(self):
        height = ((s.height/2 - 70)/5) -20
        width = s.width/2 - 20

        for i in range(0,5):
            if i < 3: upgrade_type = 'small'
            else: upgrade_type = 'big'

            y = s.height/4 + 70 + 53 + 106*i
            upgrade = Upgrade((width, height), y , upgrade_type) 

            self.selection_list.append(upgrade)

        
    def draw_upgrade_options(self):

        for selection in self.selection_list:
            if selection.rect.collidepoint(self.mouse_position):
                self.surface.blit(selection.image, selection.rect)
                selection.selected = True
            selection.selected = False
                
            selection.draw()


    def display(self):
        background = pygame.Rect(0,0, s.width/2, s.height/2)
        background.center = (s.width/2, s.height/2)
        pygame.draw.rect(self.surface, s.empty_bar_color, background)

        title = self.title_font.render('Upgrade', False, s.font_color)
        title_rect = title.get_rect(center = (s.width/2 , (s.width/4 + 35)))
        self.surface.blit(title, title_rect)

        self.draw_upgrade_options()


    def close_menu(self):
        for selection in self.selection_list:
            selection.kill()
        self.selection_list.clear()
        pygame.mixer.music.play(-1, fade_ms=1000)
        s.menu = False
        s.game = True



class Upgrade(pygame.sprite.Sprite):
    def __init__(self, size, y, upgrade_type, *groups):
        super().__init__(*groups)

        self.image = pygame.Surface(size)
        self.image.fill(s.xp_bar_color)
        self.rect = self.image.get_rect(center=(s.width/2,y))
        
        self.font = pygame.font.Font(s.font_location,30)
        self.surface = pygame.display.get_surface()

        self.type = upgrade_type
        num = random.randint(1,100)
        if num <= 20: self.rarity = 3
        elif num<=50: self.rarity = 2
        else : self.rarity = 1

        self.name, self.text, self.mod = self.set_upgrade()


    def set_upgrade(self):
        small_upgrades = {1:[('planet_life','Restore all planet life, increse max by 10%',1.10)],
                          2:[('movement_speed', 'Increase movement speed by 20%',1.20),
                              ('shooting_speed', 'Increase shooting speed by 10%',0.90),
                              ('damage', 'Increase damage by 20%',1.20)],
                          3:[('luck', 'Increase luck by 1',1),
                             ('bullet_speed','Increase bullet speed by 20%',1.20)]}
        
        big_updates = {1:[('multiple bullet','Add one more bullet in a angle',1),
                          ('small orbiter','Orbiter, protects from 5 collisions',1),
                          ('bumerang orbit','Bullets now follow an orbit',1)],
                       2:[('homing','homing bullets, less damage',1),
                          ('laser','Shoot a laser for a couple seconds',1)],
                       3:[('black hole','Shoots a black hole that attracts asteroids',1),
                          ('comet destroyer','instantly destroy the next comet',1)]}
        
        if self.type == 'small':
            return random.choice(small_upgrades[self.rarity])
        
        if self.type == 'big':
            return random.choice(big_updates[self.rarity])
        

    def draw(self):
        text = self.font.render(self.text, False, s.font_color)
        text_rect = text.get_rect(center = self.rect.center)
        self.surface.blit(text,text_rect)

