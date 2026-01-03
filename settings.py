from random import randint
width,height = 1200,1200
fps = 60
scale_factor = 1

#asteroids
G = 4
asteroid_spawn_time = 2*1000
angle_spawn_range = randint(35,45)
speed_magnitud = randint(4,6)
asteroids_list =['a-small','a-medium','a-large']
asteroid_atributes = {'a-small':(100,10),      # mass,life
                      'a-medium':(500,30),
                      'a-large':(1000,50)}

efex_volume = 0.3
music_volume = 0.1

#implement life in the planet
#implement collsions
#implement particles
#implement a score system
#make a dict with all the atributs for each respective type of celestial body so is easire to acces to it
