from kaitai import rm_v6

# signatures are typically incremented on each one
# another layer of abstraction to minimize amount of magic values appearing
# in the code
class SigCounter:

    def __init__(self, start_val: int = 0):
        self.starting_point = start_val
        self.val = start_val

    def next(self) -> int:
        result = self.val
        self.val += 1
        return result
    
    def reset(self):
        self.val = self.starting_point


def create_sig_id(parent: rm_v6.ReadWriteKaitaiStruct, val: int) -> rm_v6.RmV6.SigId:
    if (val < 0 or val > 15):
        raise Exception("signature must be a valid hex digit")
    val = (val << 4) + 0x0F
    sig = rm_v6.RmV6.SigId(None, parent, parent._root)
    sig.sig = val
    return sig

def create_sig_len(parent: rm_v6.ReadWriteKaitaiStruct, val: int) -> rm_v6.RmV6.SigLen:
    if (val < 0 or val > 15):
        raise Exception("signature must be a valid hex digit")
    val = (val << 4) + 0x0C
    sig = rm_v6.RmV6.SigLen(None, parent, parent._root)
    sig.sig = val
    return sig

def create_sig_u1(parent: rm_v6.ReadWriteKaitaiStruct, val: int) -> rm_v6.RmV6.SigU1:
    if (val < 0 or val > 15):
        raise Exception("signature must be a valid hex digit")
    val = (val << 4) + 0x01
    sig = rm_v6.RmV6.SigU1(None, parent, parent._root)
    sig.sig = val
    return sig

def create_sig_u2(parent: rm_v6.ReadWriteKaitaiStruct, val: int) -> rm_v6.RmV6.SigU2:
    if (val < 0 or val > 15):
        raise Exception("signature must be a valid hex digit")
    val = (val << 4) + 0x02
    sig = rm_v6.RmV6.SigU2(None, parent, parent._root)
    sig.sig = val
    return sig

def create_sig_u4(parent: rm_v6.ReadWriteKaitaiStruct, val: int) -> rm_v6.RmV6.SigU4:
    if (val < 0 or val > 15):
        raise Exception("signature must be a valid hex digit")
    val = (val << 4) + 0x04
    sig = rm_v6.RmV6.SigU4(None, parent, parent._root)
    sig.sig = val
    return sig

def create_sig_dbl(parent: rm_v6.ReadWriteKaitaiStruct, val: int) -> rm_v6.RmV6.SigDbl:
    if (val < 0 or val > 15):
        raise Exception("signature must be a valid hex digit")
    val = (val << 4) + 0x08
    sig = rm_v6.RmV6.SigDbl(None, parent, parent._root)
    sig.sig = val
    return sig
