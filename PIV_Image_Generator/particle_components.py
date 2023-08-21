from typing import List

import numpy as np

from PIV_Image_Generator.Particle import Particle


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