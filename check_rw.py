# Let's inspect studio_cyber_neon.jpg right wall
import struct

with open('03_ASSETS/Studio_Backgrounds/studio_cyber_neon.jpg', 'rb') as f:
    data = f.read()

print('Length of file:', len(data))
