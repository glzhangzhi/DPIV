class Particle:

    def __init__(self, x1:float, y1:float, z:float, intensity_peak:float, r:float, x2:float='nan', y2:float='nan', i2:float='nan'):
        self.x1 = x1
        self.y1 = y1
        self.z = z
        self.intensity_peak = intensity_peak
        self.r = r

    def get_intensity_map(self, x:float, y:float, frame='before') -> float:
        
        if frame == 'after':
            d = ((x - self.x2) ** 2 + (y - self.y2) ** 2) ** 0.5
        else:
            d = ((x - self.x1) ** 2 + (y - self.y1) ** 2) ** 0.5
        
        if d ** 2 >= self.r ** 2 - self.z ** 2:
            return 0
        else:
            return self.intensity_peak * ((self.r ** 2 - d ** 2) ** 0.5 / self.r) * ((self.r - abs(self.z)) / self.r)


if __name__ == '__main__':

    a = Particle(0, 0, 1, 10, 1)

    print(a.get_intensity_map(0, 1))
    print(a.get_intensity_map(1, 0))
    print(a.get_intensity_map(0, 0))
    print(a.get_intensity_map(2 ** 0.5 / 2, 2 ** 0.5 / 2))
    print(a.get_intensity_map(3 ** 0.5 / 2, 0))
