import socket, struct
from can_socket import open_can, CAN_RAW

# apply kernel-level CAN filter (efficient -- dropped before recv() returns)
# filter format: (can_id & mask) == (filter_id & mask)

CAN_RAW_FILTER = 2

def set_filter(s, filters):
    """filters: list of (can_id, mask) tuples"""
    raw = b''.join(struct.pack('=II', fid, mask) for fid, mask in filters)
    s.setsockopt(CAN_RAW, CAN_RAW_FILTER, raw)

if __name__ == '__main__':
    import sys
    from can_socket import recv
    iface = sys.argv[1] if len(sys.argv) > 1 else 'can0'
    fid   = int(sys.argv[2], 16) if len(sys.argv) > 2 else 0x100
    s = open_can(iface)
    set_filter(s, [(fid, 0x7FF)])  # exact match
    try:
        while True:
            can_id, dlc, data = recv(s)
            print(f'{can_id:03X} [{dlc}] {data.hex()}')
    except KeyboardInterrupt:
        s.close()
