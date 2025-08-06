from dataclasses import dataclass
from enum import Enum

@dataclass
class Resolution():
    height: int
    width: int
    margin: int

    def __init__(self, height, width):
        self.width = width
        self.height = height
        self.margin = 0

    def with_margin(self, margin: int):
        self.margin = margin
        return self

    def w(self):
        return self.width - 2 * self.margin
    
    def h(self):
        return self.height - 2 * self.height

    @staticmethod
    def rM2():
        return Resolution(1872, 1404)
    
    @staticmethod
    def rMPP():
        return Resolution(2160, 1620)
    

class DeviceResolution(Enum):
    RM = Resolution.rM2()
    RM2 = Resolution.rM2()
    RMPP = Resolution.rMPP()
