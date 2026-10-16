# Test Javascript morphological dilation contour algorithm in Python
procW = 640
procH = 360
totalPix = procW * procH

# Create simulated mask
rawAlphaArr = bytearray(totalPix)
for y in range(80, 280):
    for x in range(250, 390):
        rawAlphaArr[y * procW + x] = 255 # person + book

# Run Dilation Barrier (Invisible Protective Boundary)
protectRadius = 2
dilatedAlphaArr = bytearray(totalPix)

import time
t0 = time.time()

for y in range(procH):
    row = y * procW
    for x in range(procW):
        idx = row + x
        if rawAlphaArr[idx] == 255:
            dilatedAlphaArr[idx] = 255
            continue
        
        # Check if within protectRadius of any subject pixel
        # Quick 5x5 / cross check
        found = False
        for dy in range(-protectRadius, protectRadius + 1):
            ny = y + dy
            if ny < 0 or ny >= procH: continue
            nrow = ny * procW
            for dx in range(-protectRadius, protectRadius + 1):
                nx = x + dx
                if nx < 0 or nx >= procW: continue
                if rawAlphaArr[nrow + nx] == 255:
                    found = True
                    break
            if found: break
        
        if found:
            dilatedAlphaArr[idx] = 255

print(f"Dilation done in {(time.time() - t0)*1000:.2f}ms")
print(f"Original solid pixels: {rawAlphaArr.count(255)}, Dilated protected pixels: {dilatedAlphaArr.count(255)}")
