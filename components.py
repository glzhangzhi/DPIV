import scipy.io
import numpy as np
from PIL import Image

def get_velocity_field(path_mat, factor=10):

    mat = scipy.io.loadmat(str(path_mat))
    u = mat['exactOpticalFlowDisplacements'][0][0][0][0][0][0] * factor
    v = mat['exactOpticalFlowDisplacements'][0][0][0][0][0][1] * factor

    return u, v

def set_particle(image1, image2, x, y, u, v):
    
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
    
    # calculate particle position after velocity field
    x_, y_ = int(u[y, x] + x), int(v[y, x] + y)

    # draw particle image
    if x - 1 >= 0 and x + 1 <= image1.shape[1] - 1:
        if y - 1 >= 0 and y + 1 <= image1.shape[0] - 1:
            try:
                image1[y-1:y+2, x-1:x+2] = base_image
            except IndexError:
                pass

    if x_ - 1 >= 0 and x_ + 1 <= image2.shape[1] - 1:
        if y_ - 1 >= 0 and y_ + 1 <= image2.shape[0] - 1:
            try:
                image2[y_-1:y_+2, x_-1:x_+2] = base_image
            except IndexError:
                pass


    return image1, image2

def generate_frame_pair(u, v, width=256, height=512, num_particle=2000):

    image_width = width
    image_height = height

    num_particle = 2000

    image1 = np.zeros((image_height, image_width))
    image2 = np.zeros((image_height, image_width))

    for _ in range(num_particle):
        
        y = np.random.randint(0, image_height)
        x = np.random.randint(0, image_width)
        image1, image2 = set_particle(image1, image2, x, y, u, v)

    image1_object = Image.fromarray(image1).convert('L')
    image2_object = Image.fromarray(image2).convert('L')

    return image1_object, image2_object