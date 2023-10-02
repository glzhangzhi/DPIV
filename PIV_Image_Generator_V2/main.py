from copy import deepcopy

import numpy as np
from color_map import munsell_to_rgb, vector_to_munsell
from Flow import Uniform
from Particle import Particle
from PIL import Image
from visualize_components import render_image_v1

if __name__ == '__main__':
    
    # 定义图像属性
    
    # np.random.seed(2333)  # 随机种子
    
    image_width = 64  # 图像宽度
    image_height = 64  # 图像高度
    laser_sheet_thickness = 5  # 激光厚度
    
    particle_density = 1 / 256  # 粒子密度

    particle_radius = 2  # 粒子半径
    particle_intensity_peak = 1  # 粒子强度峰值

    num_particles = int(image_width * image_height * laser_sheet_thickness * particle_density)

    particle_list = []

    for _ in range(num_particles):
        
        x = np.random.uniform(-image_width / 2 + particle_radius, image_width / 2 - particle_radius)
        y = np.random.uniform(0 + particle_radius, image_height - particle_radius)
        z = np.random.uniform(-laser_sheet_thickness / 2, laser_sheet_thickness / 2)
        
        p = Particle(x, y, z, particle_intensity_peak, particle_radius)
        
        particle_list.append(p)

    image1 = render_image_v1(image_width, image_height, 1, particle_list, frame='before')
    
    image1 = (image1 - image1.min()) / (image1.max() - image1.min()) * 200
    
    image1_png = Image.fromarray(image1).convert('L')
    image1_png.save('./output/test1.png')
    
    # TODO more types of flow
    flow = Uniform(u=3, v=4, dt=1)
    
    particle_list = flow.computer_displacement_at_image_position(particle_list)
    
    image2 = render_image_v1(image_width, image_height, 1, particle_list, frame='after')
    
    image2 = (image2 - image2.min()) / (image2.max() - image2.min()) * 200
    
    image2_png = Image.fromarray(image2).convert('L')
    image2_png.save('./output/test2.png')
    
    frames = [image1_png, image2_png]
    
    frames[0].save("./output/test.gif", format='GIF',
                append_images=frames[1:],
                save_all=True,
                duration=300, loop=0)
    
    u, v = flow.output(image_width, image_height, 1)
    m = (u ** 2 + v ** 2) ** 0.5
    
    max_v = m.max()
    
    # convert vector to RGB color system
    color_m = np.zeros((m.shape[0], m.shape[1], 3), dtype=np.uint8)
    
    for i in range(m.shape[0]):
        for j in range(m.shape[1]):
            hue, value, chroma = vector_to_munsell(u[i, j], v[i, j], max_v)
            color_m[i, j, :] = munsell_to_rgb(hue, value, chroma)
    
    u_png = Image.fromarray(u).convert('L')
    u_png.save('./output/u.png')
    v_png = Image.fromarray(v).convert('L')
    v_png.save('./output/v.png') 
    color_m = Image.fromarray(color_m, 'RGB')
    color_m.save('./output/m.png')
    print('end')