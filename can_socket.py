import socket, struct

CAN_MTU = 16
CAN_RAW = 1

def open_can(iface='can0'):
    s = socket.socket(socket.AF_CAN, socket.SOCK_RAW, CAN_RAW)
    s.bind((iface,))
    return s

def pack_frame(can_id, data):
    dlc = len(data)
    pad = bytes(8 - dlc)
    return struct.pack('=IB3x8s', can_id, dlc, bytes(data) + pad)

def unpack_frame(raw):
    can_id, dlc = struct.unpack_from('=IB', raw)
    data = raw[8:8+dlc]
    return can_id, dlc, data

def send(s, can_id, data):
    s.send(pack_frame(can_id, data))

def recv(s):
    raw = s.recv(CAN_MTU)
    return unpack_frame(raw)
