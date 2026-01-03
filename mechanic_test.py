import pygame, sys
from game_manager import *
from asteroid import *
from random import randint
from settings import *


class Tester:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.screen = pygame.display.set_mode((800,800))
        self.clock = pygame.time.Clock()

        self.manager = Manager()

        self.running = True

        self.manager.visible_sprites.empty()
        self.manager.asteroids.empty()

    def run(self):
     while self.running:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    #asteroid type
                    print(self.manager.asteroids)
                    index = randint(0,2)
                    Asteroid_test(asteroids_list[index],event.pos,self.manager.visible_sprites,self.manager.asteroids)

        self.update()
        self.draw()

        pygame.display.update()
        self.clock.tick(60)

    def update(self):
        for sprite in self.manager.asteroids:
            sprite.update()
        self.manager.collision_asteroid_check()
        self.manager.asteroids.remove(self.manager.planet)


    def draw(self):
        self.screen.fill('black')
        self.manager.visible_sprites.draw(self.screen)


class Asteroid_test(Asteroid):
    def __init__(self, type_, position, *groups):
        self.new_position = position
        super().__init__(type_, *groups)

    def calculate_position0(self):
        return self.new_position
    
    def calculate_velocity0(self, position):
        return (0,0)

if __name__ == '__main__':
    game = Tester()
    game.run()