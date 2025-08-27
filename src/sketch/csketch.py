import ctypes
import os
import sys

if getattr(sys, "frozen", False):
    lib_path = os.path.join(os.path.dirname(sys.executable), "sketch", "libsketch")
else:
    lib_path = os.path.join(os.path.dirname(__file__), "libsketch", "libsketch.so")
libsketch = ctypes.cdll.LoadLibrary(lib_path)

POINT_SIZE = 14

class CSketch():
    buf: ctypes.Array[ctypes.c_char]
    
    def __init__(self, device_type):
        self.device_type = device_type
        # ensure buffer is large enough for the worst case
        # worst case scenario for rM2 is buff of size 35MB
        self.buf = ctypes.create_string_buffer(device_type.w() * device_type.h() * POINT_SIZE)
        libsketch.convert.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_int,
                                      ctypes.c_int, ctypes.c_int, ctypes.c_int,
                                      ctypes.c_int, ctypes.POINTER(type(self.buf))]
        libsketch.convert.restype = ctypes.c_size_t

    def convert(self, filename: str, layer_id: int, id_cnt: int, shades: int) -> bytes:
        size = libsketch.convert(filename.encode(), self.device_type.w(), self.device_type.h(), 
            self.device_type.margin, layer_id, id_cnt, shades, ctypes.byref(self.buf))
        return self.buf[:size]


