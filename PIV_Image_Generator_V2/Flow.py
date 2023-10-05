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


class Rankine_Vortex:
    '''漩涡流'''
    def __init__(self, xc, yc, R, max_velocity, dt):
        self.xc = xc
        self.yc = yc
        self.R = R
        self.circulation = max_velocity / R
        self.dt = dt
    
    def computer_displacement_at_image_position(self, particles:List[Particle]):

        for i, particle in enumerate(particles):
            
            r = np.sqrt(np.square(particle.y1 - self.yc) + np.square(particle.x1 - self.xc))
            theta1 = np.arctan2((particle.y1 - self.yc), (particle.x1 - self.xc))
            if r <= self.R:
                p = 1
            else:
                p = self.R ** 2 / r ** 2
            theta2 = self.circulation * self.dt * p + theta1
            particles[i].x2 = r * np.cos(theta2) + self.xc
            particles[i].y2 = r * np.sin(theta2) + self.yc
            
        return particles

    def output(self, image_width:float, image_height:float, ratio:float):
        
        number_cells_x = image_width * ratio
        number_cells_y = image_height * ratio
        
        u:np.ndarray = np.zeros((number_cells_y, number_cells_x))
        v:np.ndarray = np.zeros((number_cells_y, number_cells_x))
        
        print('generating velocity matrix ...')
        
        for x in trange(number_cells_x):
            for y in range(number_cells_y):
                
                x_cor = x - number_cells_x / 2
                
                r = np.sqrt(np.square(y - self.yc) + np.square(x_cor - self.xc))
                theta1 = np.arctan2((y - self.yc), ((x_cor - self.xc)+1e-100))
                
                if r <= self.R:
                    p = 1
                else:
                    p = self.R ** 2 / r ** 2
                
                theta2 = self.circulation * self.dt * p + theta1
                x_ = r * np.cos(theta2) + self.xc
                y_ = r * np.sin(theta2) + self.yc
                u[y][x] = (x_ - x) / self.dt
                v[y][x] = (y_ - y) / self.dt

        return u, v