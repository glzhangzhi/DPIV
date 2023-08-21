import numpy as np
from Flow import Uniform
from Particle import Particle
from PIL import Image
from visualize_components import render_image_v1

if __name__ == '__main__':
    
    # np.random.seed(2333) 
    
    image_width = 64
    image_height = 64
    laser_sheet_thickness = 5
    
    particle_density = 1 / 256

    particle_radius = 2
    particle_intensity_peak = 1

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
    image1_png.save('./outpus/test1.png')
    
    flow = Uniform(u=3, v=4, dt=1)
    
    particle_list = flow.computer_displacement_at_image_position(particle_list)
    
    image2 = render_image_v1(image_width, image_height, 1, particle_list, frame='after')
    
    image2 = (image2 - image2.min()) / (image2.max() - image2.min()) * 200
    
    image2_png = Image.fromarray(image2).convert('L')
    image2_png.save('./outpus/test2.png')
    
    frames = [image1_png, image2_png]
    
    frames[0].save("test.gif", format='GIF',
                append_images=frames[1:],
                save_all=True,
                duration=300, loop=0)
    
    u, v = flow.output(image_width, image_height, 1)
    
    m = (u ** 2 + v ** 2) ** 0.5
    
    u_png = Image.fromarray(u).convert('L')
    u_png.save('./outpus/u.png')
    v_png = Image.fromarray(v).convert('L')
    v_png.save('./outpus/v.png') 
    m_png = Image.fromarray(m).convert('L')
    m_png.save('./outpus/m.png')
    print('end')