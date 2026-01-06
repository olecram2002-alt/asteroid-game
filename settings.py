from random import randint
width,height = 1200,1200
fps = 60
scale_factor = 1
efex_volume = 0.3
music_volume = 0.1
game_over = False
menu = False
game = True

#ui helpers
empty_bar_color = '#1e3a29'
life_bar_color = '#89a257'
xp_bar_color = '#4d8061'

font_location = 'sprites/Pixeltype.ttf'
font_color = '#eeffcc'

#asteroids
G = 4
asteroid_spawn_time = 2*1000
angle_spawn_range = randint(35,45)
speed_magnitud = randint(4,6)
asteroids_list = ['a-small', 'a-medium', 'a-large', 'a-xlarge']

asteroid_atributes = {'a-small':(100,10,10),      # mass, life, xp
                      'a-medium':(500,20,20),
                      'a-large':(1000,30,20),
                      'a-xlarge':(1500,50,30)}

#player
atributes = {'planet_life':100,
            'movement_speed':2,
            'shooting_speed':100,
            'bullet_speed':10,
            'damage':10,
            'luck':0}

weapons = {'multiple bullet':1,
           'small orbiter':0,
           'bumerang orbit':0,
           'homing':0,
           'laser':0,
           'black hole':0,
           'comet destroyer':0}

gems = 0

#implement particles
#implement a score system
