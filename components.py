import pickle
from pathlib import Path

import numpy as np
import scipy.io
from PIL import Image


def convert_mat2pkl(path_mat:Path):
    
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
        
def get_velocity_field(path_pkl, factor=10):

    with open(path_pkl, 'rb') as f:
        uv = pickle.load(f)
    
    u = uv[:, :, 0] * factor
    v = uv[:, :, 1] * factor

    return u, v

def set_particle(image1, image2, x, y, u, v):
    '''place particle in two frames according to velocity field'''
    
    # generate particle intensity image
    base_image = np.ones((3, 3))
    base_image[1, :] = 2
    base_image[:, 1] = 2
    base_image[1, 1] = 3
    for i in range(base_image.shape[0]):
        for j in range(base_image.shape[1]):
            base_image[i, j] += np.random.random()
    
    # normalize particle intensity
    base_image = (base_image - base_image.min()) / (base_image.max() - base_image.min()) * 255
    
    # TODO: maybe it is better to calculate the position before and after with the center of (x, y)
    # calculate particle position after velocity field
    x_, y_ = int(u[y, x] + x), int(v[y, x] + y)

    # draw particle image in first frame
    if x - 1 >= 0 and x + 1 <= image1.shape[1] - 1:
        if y - 1 >= 0 and y + 1 <= image1.shape[0] - 1:
            try:
                image1[y - 1:y + 2, x - 1:x + 2] = base_image
            except IndexError:
                pass

    # draw particle image in second frame
    if x_ - 1 >= 0 and x_ + 1 <= image2.shape[1] - 1:
        if y_ - 1 >= 0 and y_ + 1 <= image2.shape[0] - 1:
            try:
                image2[y_ - 1:y_ + 2, x_ - 1:x_ + 2] = base_image
            except IndexError:
                pass

    return image1, image2

def generate_frame_pair(u, v, width=256, height=512, num_particle=2000):
    '''place particle into a velocity field to generate two frames of PIV image'''

    # genrate two frames of blank image
    image1 = np.zeros((height, width))
    image2 = np.zeros((height, width))

    # place particles
    for _ in range(num_particle):
        
        # choice the cordinate to place particle randomly
        y = np.random.randint(0, height)
        x = np.random.randint(0, width)

        image1, image2 = set_particle(image1, image2, x, y, u, v)

    # convert two frame images into single channel
    image1_object = Image.fromarray(image1).convert('L')
    image2_object = Image.fromarray(image2).convert('L')

    return image1_object, image2_object