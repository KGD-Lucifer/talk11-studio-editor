# We will load studio_cyber_neon.jpg and find the exact coordinates
# Canvas resolution is 1920 x 1080.
# The background is drawn at ctx.drawImage(imgStudioCyber, 0, 0, 1920, 1080).
# Let's write a script that generates an image with a coordinate grid over studio_cyber_neon.jpg
# so we can read the exact (x, y) coordinates of every single frame corner!

from PIL import Image, ImageDraw, ImageFont
import os

img_path = '03_ASSETS/Studio_Backgrounds/studio_cyber_neon.jpg'
bg = Image.open(img_path).resize((1920, 1080), Image.Resampling.LANCZOS)
draw = ImageDraw.Draw(bg)

# Draw grid lines every 50 pixels on the right wall (x: 1200 to 1920, y: 0 to 1080)
for x in range(1200, 1921, 50):
    color = (255, 0, 0) if x % 100 == 0 else (100, 100, 100)
    draw.line([(x, 0), (x, 1080)], fill=color, width=1)
    if x % 100 == 0:
        draw.text((x + 2, 10), str(x), fill=(255, 255, 0))
        draw.text((x + 2, 500), str(x), fill=(255, 255, 0))
        draw.text((x + 2, 1000), str(x), fill=(255, 255, 0))

for y in range(0, 1081, 50):
    color = (255, 0, 0) if y % 100 == 0 else (100, 100, 100)
    draw.line([(1200, y), (1920, y)], fill=color, width=1)
    if y % 100 == 0:
        draw.text((1205, y + 2), str(y), fill=(255, 255, 0))
        draw.text((1550, y + 2), str(y), fill=(255, 255, 0))
        draw.text((1850, y + 2), str(y), fill=(255, 255, 0))

# Also draw grid lines on left wall (x: 0 to 800)
for x in range(0, 801, 50):
    color = (0, 255, 255) if x % 100 == 0 else (80, 80, 80)
    draw.line([(x, 0), (x, 1080)], fill=color, width=1)
    if x % 100 == 0:
        draw.text((x + 2, 10), str(x), fill=(0, 255, 255))
        draw.text((x + 2, 500), str(x), fill=(0, 255, 255))

for y in range(0, 1081, 50):
    color = (0, 255, 255) if y % 100 == 0 else (80, 80, 80)
    draw.line([(0, y), (800, y)], fill=color, width=1)
    if y % 100 == 0:
        draw.text((5, y + 2), str(y), fill=(0, 255, 255))
        draw.text((400, y + 2), str(y), fill=(0, 255, 255))

bg.save('grid_measurement.png')
print('Grid measurement image saved successfully!')
