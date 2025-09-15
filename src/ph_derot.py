'''
Created on: 12-08-2024
@author: adithya-hn
Aim: Derotate the SUIT/Aditya-L1 images
Method: We make a subpixel binning for each pixel and then apply the rotation, and then bin by the same amount 
to convert them back to their original size, this process reduces the photometric loss during the rotation.

Update History
 - 03-09-24: Rotation angle value in header (CROTA2) is corrected.

'''

import sunpy.map
import matplotlib.pyplot as plt
import astropy.units as u
import numpy as np
import os, glob
from concurrent.futures import ProcessPoolExecutor

def get_rotMap(image_map,rot_angle): #apply rotation for subpixel map
    old_header=image_map.fits_header
    rot_map=image_map.rotate(angle=rot_angle * u.deg)
    rotMap_header=rot_map.fits_header
    old_header['CRPIX1']=rotMap_header['CRPIX1']
    old_header['CRPIX2']=rotMap_header['CRPIX2']
    Rotated_map=sunpy.map.Map(rot_map.data,old_header)
    return Rotated_map

def create_subpixels(matrix, scale):
  new_matrix = np.zeros((matrix.shape[0] * scale, matrix.shape[1] * scale))
  for i in range(matrix.shape[0]):
    for j in range(matrix.shape[1]):
      new_matrix[i * scale:(i + 1) * scale, j * scale:(j + 1) * scale] = matrix[i, j]
  new_matrix=new_matrix/pow(scale,2)
  return new_matrix

def bin_back(matrix,scale): #bin back or create a super pixel to have the same size.
   new_matrix = np.zeros((int(matrix.shape[0] / scale), int(matrix.shape[1] / scale)))
   for i in range(new_matrix.shape[0]):
    for j in range(new_matrix.shape[1]):
       new_matrix[i, j]=np.sum(matrix[i * scale:(i + 1) * scale, j * scale:(j + 1) * scale])
   return new_matrix

def get_photometric_derot(input_map,rot_angle,bin_scale):
    binUpImg=create_subpixels(input_map.data,bin_scale)
    refmap_header=input_map.fits_header
    refmap_header['CRPIX1']=input_map.fits_header['CRPIX1']*bin_scale
    refmap_header['CRPIX2']=input_map.fits_header['CRPIX2']*bin_scale
    subPixMap=sunpy.map.Map(binUpImg,refmap_header) 
    Rotated_subPix_map=get_rotMap(subPixMap,rot_angle)
    RsubPix_map_header=Rotated_subPix_map.fits_header
    RsubPix_map_header['CRPIX1']=Rotated_subPix_map.fits_header['CRPIX1']/bin_scale
    RsubPix_map_header['CRPIX2']=Rotated_subPix_map.fits_header['CRPIX2']/bin_scale

    if RsubPix_map_header['CROTA2']: # if CROTA2 exist in header it will be updated.
       RsubPix_map_header['CROTA2']=RsubPix_map_header['CROTA2']-rot_angle
    Rotated_map=sunpy.map.Map(bin_back(Rotated_subPix_map.data,bin_scale),RsubPix_map_header)
    return Rotated_map

def run(input_file): 
    input_map = sunpy.map.Map(input_file)
    if USE_CUSTOM_ANGLE: # anticlockwise rotation angle. CROTA2 can be used interchangably.
        ANGLE=15 
    else:
        ANGLE= input_map.meta.get('CROTA2')
    bin_scale=5 #each pixel will be made into 5 subpixels before rotation
    Rotated_map= get_photometric_derot(input_map,ANGLE,bin_scale)
    if SAVE:
        save_name=os.path.join(project_path, "data/processed", f"{os.path.basename(input_file)}")
        print(save_name)
        Rotated_map.save(save_name,overwrite=True) # to save the rotated map

if __name__=='__main__':
    SAVE= True #save images toggle
    USE_CUSTOM_ANGLE= False
    project_path= os.path.abspath("..")
    input_files=sorted(glob.glob(os.path.join(project_path, "data/raw/*")))
    with ProcessPoolExecutor() as executor:
        executor.map(run, input_files)
