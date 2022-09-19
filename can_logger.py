import time, sys
from can_socket import open_can, recv

def log(iface='can0', outfile=None):
    s = open_can(iface)
    f = open(outfile, 'w') if outfile else sys.stdout
    try:
        while True:
            can_id, dlc, data = recv(s)
            ts = time.time()
            hex_data = ' '.join(f'{b:02X}' for b in data)
            line = f'{ts:.6f} {can_id:08X} [{dlc}] {hex_data}'
            print(line, file=f, flush=True)
    except KeyboardInterrupt:
        pass
    finally:
        s.close()
        if outfile: f.close()

if __name__ == '__main__':
    log(outfile=sys.argv[1] if len(sys.argv) > 1 else None)
