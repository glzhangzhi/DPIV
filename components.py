import pickle
from pathlib import Path
from typing import List

import numpy as np
import scipy.io
from PIL import Image
from tqdm import tqdm

def convert_mat2pkl(path_mat:Path):
    '''convert *.mat file containing velocity field into numpy matrix into pickle file

    Parameters
    ----------
    path_mat : Path
        path to *.mat file
    '''
    dataset_dir = Path('./dataset')
    dataset_dir.mkdir(exist_ok=True)
    
    name = path_mat.stem
    
    if (dataset_dir / f'{name}.pkl').exists():
        return None    
    
    mat = scipy.io.loadmat(str(path_mat))
    
    u = mat['exactOpticalFlowDisplacements'][0][0][0][0][0][0]
    v = mat['exactOpticalFlowDisplacements'][0][0][0][0][0][1]
    
    vu = np.stack((u, v), axis=2)
    
    with open(f'./dataset/{name}.pkl', 'wb') as f:
        pickle.dump(vu, f)
        
def get_velocity_field(path_pkl:Path, factor=10) -> [np.ndarray, np.ndarray]:

    with open(path_pkl, 'rb') as f:
        uv = pickle.load(f)
    
    u = uv[:, :, 0] * factor
    v = uv[:, :, 1] * factor

    return u, v

def set_particle(image1:np.ndarray, image2:np.ndarray, p:Particle, u:np.ndarray, v:np.ndarray) -> [np.ndarray, np.ndarray]:
    '''place particle in two frames according to velocity field'''
    
    x = p.x
    y = p.y
    
    # generate particle intensity image
    base_image = np.zeros((41, 41))
    
    for i in range(base_image.shape[0]):
        for j in range(base_image.shape[1]):
            
            if p.t == 'in':
                intensity = p.intensity_a
            elif p.t == 'out':
                intensity = p.intensity_b
            else:
                raise ValueError
            
            # intensity = intensity * np.e ** (-(((i + 0.5 - 20) ** 2 + (j + 0.5 - 20) ** 2) / (0.125 * p.particle_radius ** 2)))
            intensity = intensity * np.e ** (-(((i - 20) ** 2 + (j - 20) ** 2) / (1 * p.particle_radius ** 2)))
            
            base_image[i, j] += intensity
    
    # normalize particle intensity
    base_image = (base_image - base_image.min()) / (base_image.max() - base_image.min()) * 255
    
    # calculate particle position after velocity field
    x_, y_ = int(u[y, x] + x), int(v[y, x] + y)

    # draw particle image in first frame
    if x - 20 >= 0 and x + 21 <= image1.shape[1] - 1:
        if y - 20 >= 0 and y + 21 <= image1.shape[0] - 1:
            try:
                image1[y - 20:y + 21, x - 20:x + 21] += base_image
            except IndexError:
                pass

    # draw particle image in second frame
    if x_ - 20 >= 0 and x_ + 21 <= image2.shape[1] - 1:
        if y_ - 20 >= 0 and y_ + 21 <= image2.shape[0] - 1:
            try:
                image2[y_ - 20:y_ + 21, x_ - 20:x_ + 21] += base_image
            except IndexError:
                pass

    return image1, image2

def generate_frame_pair(u:np.ndarray, v:np.ndarray, width=256, height=512, density_of_particles_in_pixel_in=6/256, density_of_particles_in_pixel_out=0.75/256, laser_sheet_thickness=2, out_of_plane_std_deviation=0.025, bitsdepth=8) -> [Image, Image]:
    '''place particle into a velocity field to generate two frames of PIV image'''

    particle_intensity_peak = 150/255 * (2 ** bitsdepth - 1)
    
    # genrate two frames of blank image
    image1 = np.zeros((height, width))
    image2 = np.zeros((height, width))

    num_particles_in = int(width * height * density_of_particles_in_pixel_in)
    num_particles_out = int(width * height * density_of_particles_in_pixel_out)
    
    particles = []
    
    # in plane
    for _ in range(num_particles_in):
        
        x = int(np.random.uniform(0, width))
        y = int(np.random.uniform(0, height))
        
        position = np.random.uniform(-laser_sheet_thickness/2, laser_sheet_thickness/2)
        intensity_a = particle_intensity_peak * np.e ** (-(position ** 2 / (0.0125 * laser_sheet_thickness ** 2)))
        
        movement = np.random.normal(0, out_of_plane_std_deviation)
        intensity_b = particle_intensity_peak * np.e ** (-((position + movement) ** 2 / (0.0125 * laser_sheet_thickness ** 2)))
        
        p = Particle(x, y, intensity_a, intensity_b, t='in')
        
        particles.append(p)
    
    # upper
    for _ in range(int(num_particles_out/2)):
        
        x = np.random.uniform(0, width)
        y = np.random.uniform(0, height)
        
        position = np.random.uniform(-laser_sheet_thickness/2 - out_of_plane_std_deviation * 10, -laser_sheet_thickness/2)
        intensity_a = particle_intensity_peak * np.e ** (-(position ** 2 / (0.0125 * laser_sheet_thickness ** 2)))
        
        movement = np.random.normal(0, out_of_plane_std_deviation)
        intensity_b = particle_intensity_peak * np.e ** (-((position + movement) ** 2 / (0.0125 * laser_sheet_thickness ** 2)))
        
        p = Particle(x, y, intensity_a, intensity_b, t='out')
        
        particles.append(p)

    # lower
    for _ in range(int(num_particles_out/2)):
        
        x = np.random.uniform(0, width)
        y = np.random.uniform(0, height)
        
        position = np.random.uniform(laser_sheet_thickness/2, laser_sheet_thickness/2 + out_of_plane_std_deviation * 10)
        intensity_a = particle_intensity_peak * np.e ** (-(position ** 2 / (0.0125 * laser_sheet_thickness ** 2)))
        
        movement = np.random.normal(0, out_of_plane_std_deviation)
        intensity_b = particle_intensity_peak * np.e ** (-((position + movement) ** 2 / (0.0125 * laser_sheet_thickness ** 2)))
        
        p = Particle(x, y, intensity_a, intensity_b, t='out')
        
        particles.append(p)
    
    # place particles
    for p in tqdm(particles):
        
        # choice the cordinate to place particle randomly
        y = np.random.randint(0, height)
        x = np.random.randint(0, width)

        image1, image2 = set_particle(image1, image2, p, u, v)

    # convert two frame images into single channel
    image1_object = Image.fromarray(image1).convert('L')
    image2_object = Image.fromarray(image2).convert('L')

    return image1_object, image2_object