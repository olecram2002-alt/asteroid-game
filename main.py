import pygame,sys
from game_manager import Manager
from settings import *
class Game:
    def __init__(self):

        #esentials
        pygame.init()
        self.screen = pygame.display.set_mode((width,height))
        pygame.display.set_caption('Asteroids')
        self.clock = pygame.time.Clock()

        #game manager
        self.manager = Manager()

        #game variables
        self.running = True

        #events
        self.asteroid_spawn = pygame.USEREVENT + 1
        pygame.time.set_timer(self.asteroid_spawn, spawn_time)

    def run(self):
        while self.running:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == self.asteroid_spawn:
                    self.manager.generate_celestial_body()
                    print('created')

            self.update()
            self.draw()

            pygame.display.update()
            self.clock.tick(fps)

    def update(self):
        self.manager.planet.update()
        self.manager.player.update()
        for sprite in self.manager.asteroids:
            if sprite is self.manager.planet:
                continue
            sprite.update()

    def draw(self):
        self.screen.fill('black')
        self.manager.visible_sprites.draw(self.screen)
        


if __name__ == '__main__':
    game = Game()
    game.run()