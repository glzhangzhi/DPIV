from typing import List

import numpy as np
from Particle import Particle
from tqdm import trange


class Uniform:
    '''平面均匀流'''
    def __init__(self, u:float, v:float, dt:float):
        self.u = u
        self.v = v
        self.dt = dt
    
    def computer_displacement_at_image_position(self, particles:List[Particle]):
        
        for i, particle in enumerate(particles):
            particles[i].y2 = self.v * self.dt + particle.y1
            particles[i].x2 = self.u * self.dt + particle.x1     
        return particles
    
    def output(self, image_width:float, image_height:float, ratio:float):
        
        number_cells_x = image_width * ratio
        number_cells_y = image_height * ratio
        
        u:np.ndarray = np.zeros((number_cells_y, number_cells_x))
        v:np.ndarray = np.zeros((number_cells_y, number_cells_x))
        
        print('generating velocity matrix ...')
        
        for x in trange(number_cells_x):
            for y in range(number_cells_y):
                u[y][x] = self.u
                v[y][x] = self.v

        return u, v