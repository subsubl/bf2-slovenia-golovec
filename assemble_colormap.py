import os, glob
import numpy as np
from PIL import Image
from osgeo import gdal

print("Preparing to assemble 4096x4096 ColorMap...")

# Mosaic bounds:
# Easting: 466000 to 471000 (5 tiles = 5000m = 5000px)
# Northing: 97000 to 102000 (5 tiles = 5000m = 5000px)

cols = [466, 467, 468, 469, 470]
rows = ['101', '100', '099', '098', '097'] # Top to bottom (North to South)

mosaic = np.zeros((5000, 5000, 3), dtype=np.uint8)

for r_idx, r in enumerate(rows):
    r_start = r_idx * 1000
    r_end = r_start + 1000
    for c_idx, c in enumerate(cols):
        c_start = c_idx * 1000
        c_end = c_start + 1000
        
        fname_short = f'/home/ator/BF2/pof_1m/POF_{c}_{int(r)}.tif'
        fname_long = f'/home/ator/BF2/pof_1m/POF_{c}_{r}.tif'
        fname = fname_short if os.path.exists(fname_short) else fname_long
        
        if not os.path.exists(fname):
            print(f"Warning: missing {fname}")
            continue
            
        ds = gdal.Open(fname)
        data = ds.ReadAsArray() # shape: (3, 1000, 1000)
        # Transpose to (1000, 1000, 3)
        rgb = np.transpose(data[:3, :, :], (1, 2, 0))
        mosaic[r_start:r_end, c_start:c_end, :] = rgb

print(f"Full 5000x5000 mosaic assembled.")

# Crop to exact 4096m x 4096m map bounds:
# E_min = 466450 (offset from 466000 is 450px)
# E_max = 470546 (offset is 450 + 4096 = 4546px)
# N_max = 101514 (offset from 102000 is 102000 - 101514 = 486px from top)
# N_min = 97418 (offset is 486 + 4096 = 4582px from top)

x_start = 450
x_end = x_start + 4096
y_start = 486
y_end = y_start + 4096

cropped_rgb = mosaic[y_start:y_end, x_start:x_end, :]
print(f"Cropped to exact map bounds: shape={cropped_rgb.shape}")

# Save uncompressed preview PNG
img = Image.fromarray(cropped_rgb)
png_path = '/home/ator/BF2/ColorMap_preview.png'
img.save(png_path, optimize=True)
print(f"Saved {png_path} ({os.path.getsize(png_path)} bytes)")

# Save DirectDraw Surface (DDS) DXT1 format for Refractor 2
dds_path = '/home/ator/BF2/ColorMap.dds'
img.save(dds_path, format='DDS', pixel_format='DXT1')
print(f"Saved {dds_path} ({os.path.getsize(dds_path)} bytes)")
print("ColorMap generation complete!")
