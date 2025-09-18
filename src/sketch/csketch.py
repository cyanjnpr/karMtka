import ctypes
import os
import sys
from typing import Tuple
from packet import RemarkableId
from .conversion import ImageConversion

if getattr(sys, "frozen", False):
    lib_path = os.path.join(os.path.dirname(sys.executable), "sketch", "libsketch", "libsketch.so")
else:
    lib_path = os.path.join(os.path.dirname(__file__), "libsketch", "libsketch.so")
libsketch = ctypes.cdll.LoadLibrary(lib_path)

POINT_SIZE = 14

# implementation in C
class CSketch():
    buf: ctypes.Array[ctypes.c_char]
    
    def __init__(self, layer_id: RemarkableId, device_type):
        self.device_type = device_type
        self.layer_id = layer_id
        # ensure buffer is large enough for the worst case
        # worst case scenario for rM2 is buff of size 35MB
        self.buf = ctypes.create_string_buffer(device_type.w() * device_type.h() * POINT_SIZE)
        libsketch.convert_potrace.argtypes = [ctypes.c_char_p, # filename
            ctypes.c_int, # page width
            ctypes.c_int, # page height
            ctypes.c_int, # page margin
            ctypes.c_int, # layer id major
            ctypes.c_int, # layer id minor
            ctypes.c_int, # threshold
            ctypes.POINTER(ctypes.c_int), # id counter
            ctypes.POINTER(type(self.buf)) # buf
            ]
        libsketch.convert_potrace.restype = ctypes.c_size_t
        libsketch.convert_naive.argtypes = [ctypes.c_char_p, # filename
            ctypes.c_int, # page width
            ctypes.c_int, # page height
            ctypes.c_int, # page margin
            ctypes.c_int, # layer id major
            ctypes.c_int, # layer id minor
            ctypes.c_int, # shades
            ctypes.POINTER(ctypes.c_int), # id counter
            ctypes.POINTER(type(self.buf)) # buf
            ]
        libsketch.convert_naive.restype = ctypes.c_size_t
        libsketch.convert_cutoff.argtypes = [ctypes.c_char_p, # filename
            ctypes.c_int, # page width
            ctypes.c_int, # page height
            ctypes.c_int, # page margin
            ctypes.c_int, # layer id major
            ctypes.c_int, # layer id minor
            ctypes.c_int, # threshold
            ctypes.POINTER(ctypes.c_int), # id counter
            ctypes.POINTER(type(self.buf)) # buf
            ]
        libsketch.convert_cutoff.restype = ctypes.c_size_t

    def convert(self,  id_cnt: int, filename: str, q: int, conversion: str) -> Tuple[int, bytes]:
        if conversion == ImageConversion.NAIVE.name:
            return self.convert_naive(id_cnt, filename, q)
        elif conversion == ImageConversion.POTRACE.name:
            return self.convert_potrace(id_cnt, filename, q)
        elif conversion == ImageConversion.CUTOFF.name:
            return self.convert_cutoff(id_cnt, filename, q)
    
    def convert_naive(self, id_cnt: int, filename: str, shades: int):
        counter = ctypes.c_int(id_cnt)
        size = libsketch.convert_naive(
            filename.encode(), self.device_type.w(), self.device_type.h(), 
            self.device_type.margin, self.layer_id.major, self.layer_id.minor, 
            shades, ctypes.byref(counter), ctypes.byref(self.buf))
        return counter.value.real, self.buf[:size]
    
    def convert_cutoff(self, id_cnt: int, filename: str, threshold: int):
        counter = ctypes.c_int(id_cnt)
        size = libsketch.convert_cutoff(
            filename.encode(), self.device_type.w(), self.device_type.h(), 
            self.device_type.margin, self.layer_id.major, self.layer_id.minor, 
            threshold, ctypes.byref(counter), ctypes.byref(self.buf))
        return counter.value.real, self.buf[:size]

    def convert_potrace(self, id_cnt: int, filename: str, threshold: int):
        counter = ctypes.c_int(id_cnt)
        size = libsketch.convert_potrace(
            filename.encode(), self.device_type.w(), self.device_type.h(), 
            self.device_type.margin, self.layer_id.major, self.layer_id.minor, 
            threshold, ctypes.byref(counter), ctypes.byref(self.buf))
        return counter.value.real, self.buf[:size]

