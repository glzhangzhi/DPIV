import math

from PIL import Image

from PIV_Image_Generator.Flows import Rankine_Vortex_And_Uniform, Uniform
from PIV_Image_Generator.Particle import (
    adjust_image_intensity,
    create_image,
    create_particles,
)

sizex = 512
sizey = 512

bitdepth = 8
deltaXfactor = 0.25
particle_radius = 1.5  # 粒子直径，单位是pixel
ni = 6  # 每个PIV中的粒子个数
noiselevel = 0  # dBW (10 log (V ^ 2)) - 20dBW -> 10 噪声强度
out_of_plane_std_deviation = 0.025
number_of_runs = 1

max_velocity = 1000  # 1000 mm / s uv方向最大速度
render_radius = 20  # Radius (square) in pixels for rendering a particle  # REVIEW 渲染一个粒子的最大半径？

max_value = 2 ** bitdepth - 1
particle_intensity_peak = 150 * max_value / 255  # 粒子中心的最大强度

last_window = [16, 16]  # PIV窗口的大小 - (y;x)

laser_sheet_thickness = 2.00  # 2mm # REVIEW 激光厚度？

marginsx = 2 * last_window[1]
marginsy = 2 * last_window[0]

# sizex = sizex + marginsx
# sizey = sizey + marginsy

mm_per_pixel = 7.5 * 10 ** -2  # 0.0075 mm / pixel  # 真实距离和像素距离的比例
mm_per_pixel = mm_per_pixel * particle_radius / 1.5

di = last_window[0] * mm_per_pixel  # mm PIV窗口在Y方向上的长度
dtao = 2 * particle_radius * mm_per_pixel  # mm 粒子直径

c = ni / (laser_sheet_thickness * di ** 2)  # 窗口体积中的粒子密度

# ratio between the sum of particle perimeters in last window and the perimeter of last window
# 每个窗口中粒子的个数 / （窗口周长/粒子周长）
ns = ni / (4 / math.pi * di / dtao)  

mindi = min(last_window)  # REVIEW 粒子移动的最小距离？

max_velocity_pixel = max_velocity / mm_per_pixel

dt = mindi * deltaXfactor / max_velocity_pixel  # REVIEW 时间间隔？

# 创建流场
# flow = Rankine_Vortex_And_Uniform(max_velocity_pixel, dt, sizex, sizey, marginsy)
flow = Uniform(max_velocity_pixel, dt, sizex, sizey, marginsy)

# 创建粒子分布
particles = create_particles(sizex, sizey, laser_sheet_thickness, particle_intensity_peak, out_of_plane_std_deviation)

# 创建两帧图像
img0, img1 = create_image(particles, flow, dt, sizex, sizey, noiselevel, bitdepth)

# 调整强度
# img0, img1 = adjust_image_intensity(img0, img1, bitdepth)

img0 = Image.fromarray(img0).convert('L')
img1 = Image.fromarray(img1).convert('L')

img0.save('./frame0.png')
img1.save('./frame1.png')

frames = [img0, img1]

frames[0].save('img.gif', append_iamges=frames[1:], save_all=True, duration=300, loop=1)