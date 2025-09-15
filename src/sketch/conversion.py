from enum import Enum
    
class ImageConversion(Enum):
    NAIVE = 0
    POTRACE = 1

    @staticmethod
    def choices():
        return [ImageConversion.NAIVE.name, ImageConversion.POTRACE.name]

