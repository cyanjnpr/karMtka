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
        self.margin = min(margin, self.width / 2)
        return self

    def w(self):
        return self.width - 2 * self.margin
    
    def h(self):
        return self.height - 2 * self.margin

    @staticmethod
    def rM():
        return Resolution(1872, 1404)
    
    @staticmethod
    def rMPP():
        return Resolution(2160, 1620)
    
    @staticmethod
    def rMPPM():
        return Resolution(1696, 954)
    

class DeviceResolution(Enum):
    RM = Resolution.rM()
    RMPP = Resolution.rMPP()
    RMPPM = Resolution.rMPPM()

    @staticmethod
    def choices():
        return [DeviceResolution.RM.name, DeviceResolution.RMPP.name,
                DeviceResolution.RMPPM.name]
