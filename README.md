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




## Usage
- Open the ph_rot.py file and update these variables
input_file = "/path/to/suit_image.fits"
bin_scale = 5   # subdivide each pixel into 5×5 sub-pixels
angle = 7       # degrees, anticlockwise; can also use map_rot_angle


```bash
