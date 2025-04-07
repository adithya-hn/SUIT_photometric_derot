
import sunpy.map
import matplotlib.pyplot as plt
import astropy.units as u
import numpy as np



def get_rotMap(image_map,rot_angle):
    old_header=image_map.fits_header
    o_sum=np.sum(np.array(image_map.data,dtype='int64'))
    rot_map=image_map.rotate(angle=rot_angle * u.deg)
    rotMap_header=rot_map.fits_header
    r_sum=np.sum(np.asarray(rot_map.data,dtype='int64'))
    
    old_header['CRPIX1']=rotMap_header['CRPIX1']
    old_header['CRPIX2']=rotMap_header['CRPIX2']
    err=(o_sum-r_sum)*100/o_sum
    print(o_sum,r_sum,err)
    Rotated_map=sunpy.map.Map(rot_map.data,old_header)
    return Rotated_map,err

def create_subpixels(matrix, scale):
  new_matrix = np.zeros((matrix.shape[0] * scale, matrix.shape[1] * scale))
  for i in range(matrix.shape[0]):
    for j in range(matrix.shape[1]):
      new_matrix[i * scale:(i + 1) * scale, j * scale:(j + 1) * scale] = matrix[i, j]
  new_matrix=new_matrix/pow(scale,2)
  return new_matrix

def bin_back(matrix,scale):
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
    Rotated_subPix_map,er=get_rotMap(subPixMap,rot_angle)
    RsubPix_map_header=Rotated_subPix_map.fits_header
    RsubPix_map_header['CRPIX1']=Rotated_subPix_map.fits_header['CRPIX1']/bin_scale
    RsubPix_map_header['CRPIX2']=Rotated_subPix_map.fits_header['CRPIX2']/bin_scale
    Rotated_map=sunpy.map.Map(bin_back(Rotated_subPix_map.data,bin_scale),RsubPix_map_header)
    Rotated_map.save(f'Rotated_Map_{rot_angle}deg.fits',overwrite=True)
    return Rotated_map,err

input_file="/Analysis/Research_Projects/SUIT_work/derotation/data/raw/SUT_T24_0956_000465_Lev1.0_2024-07-10T13.05.51.135_0983NB03.fits"
input_map = sunpy.map.Map(input_file)
bin_scale=4
angle=7 # anticlock direction
Rotated_map,err=get_photometric_derot(input_map,angle,bin_scale)
print(f"Error in rotation: {err}")
Rotated_map.save(f'Rotated_Map_{angle}deg.fits',overwrite=True)


