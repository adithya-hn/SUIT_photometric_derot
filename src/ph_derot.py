
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



def get_rotMap(image_map,rot_angle): #apply rotation for subpixel map
    old_header=image_map.fits_header
    o_sum=np.sum(np.array(image_map.data,dtype='int64'))
    rot_map=image_map.rotate(angle=rot_angle * u.deg)
    rotMap_header=rot_map.fits_header
    r_sum=np.sum(np.asarray(rot_map.data,dtype='int64'))
    
    old_header['CRPIX1']=rotMap_header['CRPIX1']
    old_header['CRPIX2']=rotMap_header['CRPIX2']
    err=(o_sum-r_sum)*100/o_sum
    #print(o_sum,r_sum,err)
    Rotated_map=sunpy.map.Map(rot_map.data,old_header)
    return Rotated_map,err

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
    Rotated_subPix_map,err=get_rotMap(subPixMap,rot_angle)
    RsubPix_map_header=Rotated_subPix_map.fits_header
    RsubPix_map_header['CRPIX1']=Rotated_subPix_map.fits_header['CRPIX1']/bin_scale
    RsubPix_map_header['CRPIX2']=Rotated_subPix_map.fits_header['CRPIX2']/bin_scale

    if RsubPix_map_header['CROTA2']: # if CROTA2 exist in header it will be updated.
       print('initial map rotation angle : ', RsubPix_map_header['CROTA2'])
       print('Updated angle will be: ', RsubPix_map_header['CROTA2']-rot_angle)
       RsubPix_map_header['CROTA2']=RsubPix_map_header['CROTA2']-rot_angle
      
    Rotated_map=sunpy.map.Map(bin_back(Rotated_subPix_map.data,bin_scale),RsubPix_map_header)

    #Rotated_map.save(f'Rotated_Map_{rot_angle}deg.fits',overwrite=True)
    return Rotated_map,err

if __name__=='__main__':
    input_file="/Analysis/Research_Projects/Flare_studies/SUIT_Flares/Case2_June02/data/raw/SUT_T24_0785_000397_Lev1.0_2024-06-02T02.30.52.740_0973NB03.fits"
    input_map = sunpy.map.Map(input_file)
    if input_map.meta.get('CROTA2'):
       map_rot_angle=input_map.meta.get('CROTA2')
       print('Map rotation angle, as per header key CROTA2:',map_rot_angle )

    bin_scale=5 #each pixel will be made into 5 subpixels before rotation
    angle=7     #in degrees, anticlock direction, custom angle or header value (map_rot_angle) can be equated here

    Rotated_map,err=get_photometric_derot(input_map,angle,bin_scale)
    print(f"%Error in total count after rotation: {err}") #% error
    Rotated_map.save(f'Rotated_Map_{angle}deg.fits',overwrite=True) # to save the rotated map


