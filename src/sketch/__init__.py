from config import C_SKETCH_IMPLEMENTATION
if (C_SKETCH_IMPLEMENTATION):
    from .csketch import CSketch
else: 
    from .sketch import Sketch

from .conversion import ImageConversion
