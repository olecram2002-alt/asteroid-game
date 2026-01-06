import pygame,sys
from game_manager import Manager
import settings as s
class Game:
    def __init__(self):

        #esentials
        pygame.init()
        pygame.mixer.init()

        info = pygame.display.Info()
        screen_width = info.current_w
        screen_height = info.current_h

        if screen_width < s.width or screen_height < s.height:
            flags = pygame.FULLSCREEN | pygame.SCALED
        else: 
            flags = 0
        
        self.screen = pygame.display.set_mode((s.width,s.height), flags)
        pygame.display.set_caption('Asteroids')
        self.clock = pygame.time.Clock()
        pygame.mixer.music.load('sounds/music/Cranky-2D-Creatures.ogg')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(s.music_volume)

        #game manager
        self.manager = Manager()

        #game variables
        self.running = True

        #events
        self.asteroid_spawn = pygame.USEREVENT + 1
        pygame.time.set_timer(self.asteroid_spawn, s.asteroid_spawn_time)


    def run(self):
        while self.running:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == self.asteroid_spawn:
                    self.manager.generate_celestial_body()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

            self.update()
            self.draw()

            pygame.display.update()
            self.clock.tick(s.fps)


    def update(self):
        self.manager.planet.update()
        self.manager.player.update()
        for sprite in self.manager.asteroids:
            if sprite is self.manager.planet:
                continue
            sprite.update()
        for sprite in self.manager.bullet_sprites:
            sprite.update()
        self.manager.collision_bullet_check()
        self.manager.collision_planet_check()
        self.manager.collision_asteroid_check()


    def draw(self):
        self.screen.fill('black')
        self.manager.visible_sprites.draw(self.screen)
        self.manager.ui.display()
        


if __name__ == '__main__':
    game = Game()
    game.run()