import math

import numpy as np


class AbsFlow:
    
    def __init__(self):
        pass
    
    def computer_displacement_at_image_position(self):
        pass

class Uniform(AbsFlow):
    '''平面均匀流'''
    def __init__(self, max_velocity_pixel, dt, sizex, sizey, marginsy):
        self.max_velocity_pixel = max_velocity_pixel
        self.dt = dt
        self.imsizex = sizex
        self.imsizey = sizey
        self.marginsy = marginsy
    
    def computer_displacement_at_image_position(self, particles):
        
        m = 1
        
        for i, particle in enumerate(particles):
            
            particles[i].x1 = m * self.max_velocity_pixel * self.dt + particle.x
            particles[i].y1 = m * 0 + particle.y
        
        return particles

class Rankine_Vortex_And_Uniform(AbsFlow):
    '''涡流和均匀流的叠加'''
    def __init__(self, max_velocity_pixel, dt, sizex, sizey, marginsy):
        
        self.radius = 100  # REVIEW 这两个参数是用来控制什么的？
        self.weight = 1
        
        self.dt = dt
        
        c1 = 0.35  # Ratio of constant velocity components u,v contribution for the max Velocity magnitude 
        c = 1 - c1
        m = c + math.sqrt(2) * c1
        
        self.u = max_velocity_pixel * c1 / m
        self.v = max_velocity_pixel * c1 / m
        self.circulation = max_velocity_pixel * c / m
        
        self.yc = (sizex - 1) / 2
        self.xc = (sizey - 1) / 2  # 图像中心点的坐标
    
    def computer_displacement_at_image_position(self, particles):
        '''
        用Runge-Kutta numeric method of 4th order计算某个位置的位移
        
        x0, y0: 所有粒子的坐标集合
        dt: 时间间隔
        '''
        
        for i, particle in enumerate(particles):

            x = particle.x
            y = particle.y
            
            xk1 = x - self.xc
            yk1 = y - self.yc
            
            r = math.sqrt(xk1 ** 2 + yk1 ** 2)
            
            m = self.circulation * self.radius
            
            if r > self.radius:
                
                k1x = self.dt * (-(m * yk1)/(xk1**2 + yk1**2) + self.u)
                k1y = self.dt * ((m * xk1)/(xk1**2 + yk1**2) + self.v)

                xk2 = xk1 + k1x/2
                yk2 = yk1 + k1y/2
                k2x = self.dt * (-(m * yk2)/(xk2**2 + yk2**2) + self.u)
                k2y = self.dt * ((m * xk2)/(xk2**2 + yk2**2) + self.v)

                xk3 = xk1 + k2x/2
                yk3 = yk1 + k2y/2
                k3x = self.dt * (-(m * yk3)/(xk3**2 + yk3**2) + self.u)
                k3y = self.dt * ((m * xk3)/(xk3**2 + yk3**2) + self.v)

                xk4 = xk1 + k3x
                yk4 = yk1 + k3y
                k4x = self.dt * (-(m * yk4)/(xk4**2 + yk4**2) + self.u)
                k4y = self.dt * ((m * xk4)/(xk4**2 + yk4**2) + self.v)

                particles[i].x1 = xk1 + 1/6*(k1x + 2*k2x + 2*k3x + k4x) + self.xc
                particles[i].y1 = yk1 + 1/6*(k1y + 2*k2y + 2*k3y + k4y) + self.yc
            
            else:
                
                k1x = self.dt * (-(m * yk1) + self.u)
                k1y = self.dt * ((m * xk1) + self.v)

                xk2 = xk1 + k1x/2
                yk2 = yk1 + k1y/2
                k2x = self.dt * (-(m * yk2) + self.u)
                k2y = self.dt * ((m * xk2) + self.v)

                xk3 = xk1 + k2x/2
                yk3 = yk1 + k2y/2
                k3x = self.dt * (-(m * yk3) + self.u)
                k3y = self.dt * ((m * xk3) + self.v)

                xk4 = xk1 + k3x
                yk4 = yk1 + k3y
                k4x = self.dt * (-(m * yk4) + self.u)
                k4y = self.dt * ((m * xk4) + self.v)

                particles[i].x1 = xk1 + 1/6*(k1x + 2*k2x + 2*k3x + k4x) + self.xc
                particles[i].y1 = yk1 + 1/6*(k1y + 2*k2y + 2*k3y + k4y) + self.yc

        return particles