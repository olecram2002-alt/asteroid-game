from random import randint
width,height = 1200,1200
fps = 60
scale_factor = 1
efex_volume = 0.3
music_volume = 0.1
game_over = False
menu = False

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
                      'a-medium':(500,30,20),
                      'a-large':(1000,50,20),
                      'a-xlarge':(1500,100,30)}

#atributes
atributes = {'planet_life':100,
            'movement_speed':2,
            'shooting_speed':80,
            'damage':10}

#implement life in the planet
#implement particles
#implement a score system
