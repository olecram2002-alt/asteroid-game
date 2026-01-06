import pygame
import settings as s
import random

class Upgrade_Menu:
    def __init__(self):
        self.surface = pygame.display.get_surface()
        self.title_font = pygame.font.Font(s.font_location,50)
        self.mouse_position = (0,0)
        self.selections = []


    def input(self):
        self.mouse_position = pygame.mouse.get_pos()


    def create_upgrades(self):
        height = ((s.height/2 - 70)/5) -20
        width = s.width/2 - 20

        for i in range(0,5):
            if i < 3: upgrade_type = 'small'
            else: upgrade_type = 'big'

            y = s.height/4 + 70 + 53 + 106*i
            upgrade = Upgrade((width, height), y , upgrade_type) 

            self.selections.append(upgrade)

        
    def draw_upgrade_options(self):

        for selection in self.selections:
            if selection.rect.collidepoint(self.mouse_position):
                self.surface.blit(selection.image, selection.rect)
                
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
        for selection in self.selections:
            selection.kill()
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

        self.name, self.text = self.set_upgrade()


    def set_upgrade(self):
        small_upgrades = {1:[('planet_life','Restore all planet life')],
                          2:[('movement_speed', 'Increase movement speed by 20%'),
                              ('shooting_speed', 'Increase shooting speed by 10%'),
                              ('damage', 'Increase damage by 20%')],
                          3:[('luck', 'Increase luck by 1')]}
        
        big_updates = {}
        if self.type == 'small':
            return random.choice(small_upgrades[self.rarity])
        
        if self.type == 'big':
            return ('','')
        

    def draw(self):
        text = self.font.render(self.text, False, s.font_color)
        text_rect = text.get_rect(center = self.rect.center)
        self.surface.blit(text,text_rect)

