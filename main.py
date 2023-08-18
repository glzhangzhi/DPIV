from pathlib import Path

from components import *

path_raw_data = Path('SOFTX_2020_33/out/Bits08')

for raw_data in path_raw_data.rglob('*.mat'):
    convert_mat2pkl(raw_data)


path_dataset = Path('./dataset')

output_dir = Path('./output')
output_dir.mkdir(exist_ok=True)

for path_pkl in path_dataset.rglob('*.pkl'):

    name = path_pkl.stem

    for k in [5]:

        u, v = get_velocity_field(path_pkl, k)

        image1, image2 = generate_frame_pair(u, v, density_of_particles_in_pixel_in=6/256/10, density_of_particles_in_pixel_out=0.75/256/10)

        image1.save(f'./output/{name}-{k}-before.png')
        image2.save(f'./output/{name}-{k}-after.png')


from PIL import Image

img_paths = [
    "C:/Users/Administrator/Desktop/DPIV/output/uniform_run02_validation-2-after.png",
    "C:/Users/Administrator/Desktop/DPIV/output/uniform_run02_validation-2-before.png",
]

for p in Path('C:/Users/Administrator/Desktop/DPIV/output').glob('*_before.png'):
    
    name = p.stem
    name_without_suffix = name.split('-before')[0]
    name_after = name_without_suffix + '-after'
    
    


    # Create the frames
    frames = []

    for i in img_paths:
        new_frame = Image.open(i)
        frames.append(new_frame)

    # Save into a GIF file that loops forever
    frames[0].save("C:/Users/Administrator/Desktop/DPIV/output/uniform_run02_validation-2.gif", format='GIF',
                    append_images=frames[1:],
                    save_all=True,
                    duration=300, loop=0)


