import math

import numpy as np

'''
https://www.rapidtables.com/convert/color/hsv-to-rgb.html
https://www.rapidtables.com/convert/color/rgb-to-hsv.html
'''

def vector_to_munsell(u, v, max_v):
    '''
    convert a vector in 2D into Munsell color system
    '''
    
    # 映射到色调
    hue = math.degrees(np.arctan2(v, u))
    if hue < 0:
        hue += 360

    value = 100

    # 映射到饱和度
    chroma = math.sqrt(u ** 2 + v ** 2) / max_v * 100

    return hue, value, chroma

def munsell_to_rgb(hue: float, value: float, chroma: float):
    '''
    convert color in munsell system into RGB system
    
    0 <= H < 360, 0 <= chroma <= 100, 0 <= value <= 100
    '''

    chroma = chroma / 100
    value = value / 100
    
    c = value * chroma
    x = c * (1 - abs((hue / 60) % 2 - 1))
    m = value - c
    
    if 0 <= hue < 60:
        R_, G_, B_ = (c, x, 0)
    elif 60 <= hue < 120:
        R_, G_, B_ = (x, c, 0)
    elif 120 <= hue < 180:
        R_, G_, B_ = (0, c, x)
    elif 180 <= hue < 240:
        R_, G_, B_ = (0, x, c)
    elif 240 <= hue < 300:
        R_, G_, B_ = (x, 0, c)
    elif 300 <= hue < 360:
        R_, G_, B_ = (c, 0, x)
    else:
        raise ValueError('hue should belong to [0, 360)')
    
    R = (R_ + m) * 255
    G = (G_ + m) * 255
    B = (B_ + m) * 255
    
    return (R, G, B)


def rgb_to_munsell(r, g, b):
    '''
    convert color in rgb system into munsell color system
    '''
    r_ = r / 255
    g_ = g / 255
    b_ = b / 255
    
    cmax = max(r_, g_, b_)
    cmin = min(r_, g_, b_)
    delta = cmax - cmin
    
    value = cmax
    
    if cmax == 0:
        chroma = 0
    else:
        chroma = delta / cmax
    
    if delta == 0:
        hue = 0
    elif cmax == r_:
        hue = 60 * (((g_ - b_) / delta) % 6)
    elif cmax == g_:
        hue = 60 * (((b_ - r_) / delta) + 2)
    elif cmax == b_:
        hue = 60 * (((r_ - g_) / delta) + 4)
    else:
        raise ValueError('can not calculate the hue')
    
    return hue, value * 100, chroma * 100

if __name__ == "__main__":
    
    x, y, max_v = 4, 3, 10

    # 调用函数进行映射
    hue, value, chroma = vector_to_munsell(x, y, max_v)

    # 输出结果
    print(f"色调(Hue): {hue:.2f}°")
    print(f"明度(Value): {value:.2f}")
    print(f"饱和度(Chroma): {chroma:.2f}")

    # 调用函数进行转换
    r, g, b = munsell_to_rgb(hue, value, chroma)

    # 输出RGB值
    print(f"对应的RGB值为:({r}, {g}, {b})")
    
    # 再反向转换到munsell
    h, v, c = rgb_to_munsell(r, g, b)
    
    # 输出结果
    print(f"色调(Hue): {h:.2f}°")
    print(f"明度(Value): {v:.2f}")
    print(f"饱和度(Chroma): {c:.2f}")
