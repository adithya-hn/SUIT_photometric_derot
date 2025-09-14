#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
2025-09-14 22:32:26
@author: janmejoyarch
@hostname: suitpoc1

DESCRIPTION
"""

import numpy as np
import os, glob
from astropy.io import fits
import matplotlib.pyplot as plt

project_path= os.path.abspath("..")
raw_file=glob.glob(os.path.join(project_path, "data/raw/*"))[0]
phot_error_ls=[]
angles= np.arange(5,90,5)
processed_files= sorted(glob.glob(os.path.join(project_path, "data/processed", f"*{os.path.basename(raw_file)}")))

for processed_file in processed_files:
    with fits.open(raw_file) as raw_hdu:
        raw_data= raw_hdu[0].data
        raw_header= raw_hdu[0].header
    with fits.open(processed_file) as processed_hdu:
        processed_data= processed_hdu[0].data
        processed_data= np.nan_to_num(processed_data, nan=0.0)
        processed_header= processed_hdu[0].header

    phot_error= (np.sum(raw_data)-np.sum(processed_data))*100/np.sum(raw_data)
    phot_error_ls.append(phot_error)
    print(os.path.basename(processed_file), phot_error)
plt.figure()
plt.plot(angles, phot_error_ls)
plt.show()
