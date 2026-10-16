# pure python test
import time

# Let's test the dilation and protective contour algorithm in Python
procW = 640
procH = 360
totalPix = procW * procH

# Create simulated probability mask: person in center (x: 200..440, y: 50..320)
# and a held book (x: 270..370, y: 180..260 with lower prob 70)
# and background noise (wall painting at x: 50..100, y: 50..100)
mask = [0] * totalPix
for y in range(50, 320):
    for x in range(220, 420):
        mask[y * procW + x] = 220 # person core

for y in range(180, 260):
    for x in range(270, 370):
        mask[y * procW + x] = 85 # held book

# background noise
for y in range(50, 100):
    for x in range(50, 100):
        mask[y * procW + x] = 160 # wall painting

# Algorithm test
t0 = time.time()

# Step 1: Find person envelope
pMinX, pMaxX = procW, 0
pMinY, pMaxY = procH, 0
for y in range(0, procH, 2):
    row = y * procW
    for x in range(0, procW, 2):
        if mask[row + x] > 165:
            if x < pMinX: pMinX = x
            if x > pMaxX: pMaxX = x
            if y < pMinY: pMinY = y
            if y > pMaxY: pMaxY = y

print(f"Person envelope: ({pMinX}, {pMinY}) to ({pMaxX}, {pMaxY})")

# Step 2: Interaction zone for held objects
hasPerson = (pMaxX > pMinX)
objXMin = max(0, pMinX - 35) if hasPerson else 0
objXMax = min(procW - 1, pMaxX + 35) if hasPerson else procW - 1
objYMin = pMinY + int((pMaxY - pMinY) * 0.25) if hasPerson else 0
objYMax = min(procH - 1, pMaxY + 35) if hasPerson else procH - 1

print(f"Held object zone: ({objXMin}, {objYMin}) to ({objXMax}, {objYMax})")
print(f"Elapsed: {(time.time() - t0)*1000:.2f}ms")
