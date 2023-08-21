import math
from typing import List

import numpy as np
from Flows import AbsFlow


class Particle:
    
    def __init__(self, x, y, intensity_a, intensity_b, t) -> None:
        self._x = x
        self._y = y
        self.intensity_a = intensity_a
        self.intensity_b = intensity_b
        self.particle_radius = 1.5
        self.render_radius = 20
        self.t = t
    
    @property
    def x(self):
        return int(self._x)
    
    @property
    def y(self):
        return int(self._y)
    
    @property
    def x1(self):
        return int(self._x1)
    
    @property
    def y1(self):
        return int(self._y1)
    
    @x1.setter
    def x1(self, x1):
        self._x1 = x1
    
    @y1.setter
    def y1(self, y1):
        self._y1 = y1