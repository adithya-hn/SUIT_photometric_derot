![Logo](https://suit.iucaa.in/sites/default/files/top_banner_compressed_2_1.png)

# SUIT Photometric Derotation

This repository provides a **flux-conserving rotation routine** for Solar Ultraviolet Imaging Telescope (SUIT) images.  
The rotation is performed about the **full-disc centre** and minimizes photometric loss by subdividing each pixel into sub-pixels before rotation.

---

## Features

- Rotation about the **disc centre**, not the ROI centre.  
- **Flux conservation** via sub-pixel resampling.  
- Works directly with **FITS images** (SunPy `Map` objects).  
- Reports the **photometric error** (total counts before vs after rotation).  
- Saves the rotated map as a new FITS file with updated WCS.
---
## Usage
- Place files to be processed in `./data/raw`
- Get processed data in `./data/processed`
- Any photometric test results or plots will be saved in `./products`

- `bin_scale = n`   # subdivide each pixel into n×n sub-pixels
- `ANGLE= d`       # degrees, anticlockwise; can also use map_rot_angle
---

## How It Works

The rotation is implemented in three main steps:

1. **Sub-pixel Expansion**  
   - Each pixel of the original SUIT image is subdivided into a finer grid of  
     `bin_scale × bin_scale` sub-pixels.  
   - This increases spatial sampling and ensures that flux is properly redistributed  
     during rotation.

2. **Rotation About the Full-disc Centre**  
   - The high-resolution grid is rotated by the desired angle (anticlockwise, in degrees).  
   - The rotation axis is always the **full-disc centre**, ensuring consistency across  
     both ROI and full-disc images.

3. **Rebinning to Original Resolution**  
   - The rotated high-resolution image is binned back to the original  
     pixel scale.  
   - This step conserves the total flux, minimizing interpolation losses.



---

### Why Sub-pixel Expansion?
Standard image rotation (e.g., bilinear or spline interpolation) can cause  
photometric errors because pixel values are redistributed approximately.  
By subdividing each pixel into many smaller sub-pixels before rotation and  
then rebinning, the method ensures that the total counts are conserved to  
better than ~0.01% (depending on `bin_scale`).




