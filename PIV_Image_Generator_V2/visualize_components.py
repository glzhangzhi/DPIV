from typing import List

import numpy as np
from Particle import Particle
from tqdm import trange


def render_image_v1(image_width:float, image_height:float, ratio:float, particle_list:List[Particle], frame='before'):
    
    number_cells_x = image_width * ratio
    number_cells_y = image_height * ratio
    
    image = np.zeros((number_cells_y, number_cells_x))
    
    print('rendering particle image ...')
    
    for x in trange(number_cells_x):
        for y in range(number_cells_y):
            rx = x - image_width / 2 + 0.5
            ry = image_height + 0.5 - y
            sum_intensity = 0
            for p in particle_list:
                i = p.get_intensity_map(rx, ry, frame)
                if i >= sum_intensity:
                    sum_intensity = i
            image[y][x] = sum_intensity
    
    return image