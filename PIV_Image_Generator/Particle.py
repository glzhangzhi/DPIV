import math
from typing import List

import numpy as np
from Flows import AbsFlow


class Particle:
    
    def __init__(self, x, y, intensity_a, intensity_b) -> None:
        self.x = x
        self.y = y
        self.intensity_a = intensity_a
        self.intensity_b = intensity_b
        self.particle_radius = 1.5
        self.render_radius = 20

def create_particles(image_size_x, image_size_y, laser_sheet_thickness, particle_intensity_peak, out_of_plane_std_deviation) -> List[Particle]:
    '''  
    '''
    density_of_particles_in_pixel_in = 6/256
    density_of_particles_in_pixel_out = 0.75/256
    
    num_particles_in = int(image_size_x * image_size_y * density_of_particles_in_pixel_in)
    num_particles_out = int(image_size_x * image_size_y * density_of_particles_in_pixel_out)
    
    particles = []
    
    # in plane
    for _ in range(num_particles_in):
        
        x = int(np.random.uniform(0, image_size_x))
        y = int(np.random.uniform(0, image_size_y))
        
        position = np.random.uniform(-laser_sheet_thickness/2, laser_sheet_thickness/2)
        intensity_a = particle_intensity_peak * np.e ** (-(position ** 2 / (0.0125 * laser_sheet_thickness ** 2)))
        
        movement = np.random.normal(0, out_of_plane_std_deviation)
        intensity_b = particle_intensity_peak * np.e ** (-((position + movement) ** 2 / (0.0125 * laser_sheet_thickness ** 2)))
        
        p = Particle(x, y, intensity_a, intensity_b)
        
        particles.append(p)
    
    # upper
    for _ in range(int(num_particles_out/2)):
        
        x = np.random.uniform(0, image_size_x)
        y = np.random.uniform(0, image_size_y)
        
        position = np.random.uniform(-laser_sheet_thickness/2 - out_of_plane_std_deviation * 10, -laser_sheet_thickness/2)
        intensity_a = particle_intensity_peak * np.e ** (-(position ** 2 / (0.0125 * laser_sheet_thickness ** 2)))
        
        movement = np.random.normal(0, out_of_plane_std_deviation)
        intensity_b = particle_intensity_peak * np.e ** (-((position + movement) ** 2 / (0.0125 * laser_sheet_thickness ** 2)))
        
        p = Particle(x, y, intensity_a, intensity_b)
        
        particles.append(p)

    # lower
    for _ in range(int(num_particles_out/2)):
        
        x = np.random.uniform(0, image_size_x)
        y = np.random.uniform(0, image_size_y)
        
        position = np.random.uniform(laser_sheet_thickness/2, laser_sheet_thickness/2 + out_of_plane_std_deviation * 10)
        intensity_a = particle_intensity_peak * np.e ** (-(position ** 2 / (0.0125 * laser_sheet_thickness ** 2)))
        
        movement = np.random.normal(0, out_of_plane_std_deviation)
        intensity_b = particle_intensity_peak * np.e ** (-((position + movement) ** 2 / (0.0125 * laser_sheet_thickness ** 2)))
        
        p = Particle(x, y, intensity_a, intensity_b)
        
        particles.append(p)
    
    return particles

def create_image(particles:List[Particle], flow:AbsFlow, dt, sizeX, sizeY, noise_level, bits):

    particles = flow.computer_displacement_at_image_position(particles)
    
    img0 = render_particles(particles, sizeX, sizeY, frame=0)
    img1 = render_particles(particles, sizeX, sizeY, frame=1)
        
    if noise_level > 0:
        
        max_value = 2 ** bits - 1
        
        # 使用noise_level(dBW)作为参数生成高斯白噪声
        noise_img0 = generate_gaussian_white_noise(sizeX, sizeY, noise_level, max_value)
        noise_img1 = generate_gaussian_white_noise(sizeX, sizeY, noise_level, max_value)
        
        # 叠加噪声
        img0 = img0 + noise_img0
        img1 = img1 + noise_img1
    
    return img0, img1
    
def render_particles(particles:List[Particle], sizeX, sizeY, frame=0):
    
    img = np.zeros((sizeX, sizeY))
    
    for particle in particles:
    
        d = particle.particle_radius * 2
        
        maxX = min(round(particle.x + particle.render_radius), sizeX)
        minX = max(round(particle.x - particle.render_radius), 1)
        maxY = min(round(particle.y + particle.render_radius), sizeY)
        minY = max(round(particle.y - particle.render_radius), 1)
        
        xspace = np.linspace(minX, maxX, maxX-minX)
        yspace = np.linspace(minY, maxY, maxY-minY)
        
        xs, ys = np.meshgrid(xspace, yspace)
        
        if frame == 0:
            intensity = particle.intensity_a
        elif frame == 1:
            intensity = particle.intensity_b
        else:
            raise ValueError
        
        if maxY > minY and maxX > minX:
            
            img[minY:maxY, minX:maxX] = img[minY:maxY, minX:maxX] + intensity * np.exp(-((np.float32(xs)+0.5-particle.x)**2 + (np.float32(ys)+0.5-particle.y)**2)/(0.125*d**2))
        
    return img

def generate_gaussian_white_noise(sizeX, sizeY, noise_level, max_value):
    
    # 生成高斯白噪声，均值为0，标准差根据噪声强度调整
    noise_img = np.random.normal(loc=0, scale=noise_level, size=(sizeY, sizeX))
    
    # 将噪声值限制在0到1之间，防止超出图像像素范围
    noise_img = noise_img * (max_value / 255)
    
    return noise_img

def adjust_image_intensity(img0, img1, bits, intensity_method='normalize'):
    
    max_value = 2 ** bits - 1
    
    if intensity_method == 'normalize':
        maxI = np.max((np.max(img0), np.max(img1)))
        if maxI > max_value:
            img0 = img0 * max_value / maxI
            img1 = img1 * max_value / maxI
        img0 = np.round(img0)
        img1 = np.round(img1)
    elif intensity_method == 'clip':
        img0 = np.round(img0)
        img1 = np.round(img1)
        img0[img0>max_value] = max_value
        img1[img1>max_value] = max_value
    else:
        raise ValueError
    
    if bits == 8:
        img0 = np.uint8(img0)
        img1 = np.uint8(img1)
    else:
        img0[img0 > max_value] = max_value
        img1[img1 > max_value] = max_value
        Im0 = np.uint16(Im0)
        Im1 = np.uint16(Im1)
    
    return img0, img1