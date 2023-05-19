import struct

def read_int8(f):
    return struct.unpack("b", f.read(1))[0]

def read_uint8(f):
    return struct.unpack("B", f.read(1))[0]

def read_int16(f):
    return struct.unpack("h", f.read(2))[0]

def read_uint16(f):
    return struct.unpack("H", f.read(2))[0]

def read_int32(f):
    return struct.unpack("i", f.read(4))[0]

def read_uint32(f):
    return struct.unpack("I", f.read(4))[0]

def read_float(f):
    return struct.unpack("f", f.read(4))[0]