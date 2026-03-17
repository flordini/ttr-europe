import base64, struct, zlib

def make_png(size, bg, fg):
    # Simple PNG generator: colored square with a train icon feel
    pixels = []
    cx, cy = size//2, size//2
    r = size//3
    for y in range(size):
        row = []
        for x in range(size):
            dx, dy = x-cx, y-cy
            # outer circle
            if dx*dx+dy*dy <= r*r:
                # inner details: cross/star shape for train
                if abs(dx) < r//4 or abs(dy) < r//4:
                    row += fg
                else:
                    row += bg
            else:
                row += [44, 74, 30]  # dark green border
        pixels.append(bytes(row))

    def chunk(name, data):
        c = zlib.crc32(name + data) & 0xffffffff
        return struct.pack('>I', len(data)) + name + data + struct.pack('>I', c)

    sig = b'\x89PNG\r\n\x1a\n'
    ihdr = chunk(b'IHDR', struct.pack('>IIBBBBB', size, size, 8, 2, 0, 0, 0))
    raw = b''.join(b'\x00' + row for row in pixels)
    idat = chunk(b'IDAT', zlib.compress(raw))
    iend = chunk(b'IEND', b'')
    return sig + ihdr + idat + iend

for sz in [192, 512]:
    data = make_png(sz, [200, 160, 60], [255, 255, 255])
    with open(f'icon-{sz}.png', 'wb') as f:
        f.write(data)
    print(f'icon-{sz}.png written')
