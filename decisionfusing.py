# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 10:32:33 2019

@author: s159890
"""

import numpy as np
import 

def decisionfusing(fixed_im, reg_ims, pred_segs):
    """ Takes as input a fixed image (3D numpy array), a series of registered images (4D numpy array) with the
    fixed image as target, and accompanying predicated segmentations per registered image (4D numpy array)
    
    Executes decision fusing technique described in Isgum et al. (2009). Returns a binary, decision fused
    numpy array of same dimensions as fixed image. """
    
    # Begin by checking dimensions of input arguments
    assert fixed_im.shape == reg_ims[0,:,:,:].shape, "Fixed image dimensions do not match registered images."
    assert fixed_im.shape == pred_segs[0,:,:,:].shape, "Fixed image dimensions do not match predicted segmentation images."
    
    # Allocate memory & calculate difference images
    diff_ims = np.zeros(reg_ims.shape, dtype = reg_ims.dtype)
    for i in range(reg_ims.shape[0]):
        diff_ims[i] = np.abs(reg_ims[i] - fixed_im)
        
    # Allocate memory & calculate weight images
    weights = np.zeros(reg_im.shape, dtype = reg_ims.dtype)
    for i in range(reg_ims.shape[0]):
        
    
    return diff_ims
    
## DEBUGGING
import SimpleITK as sitk

image1 = sitk.ReadImage(r'C:\Users\s159890\Documents\Q3 Jaar 1 (BME)\Capita selecta in image analysis (8DM20)\Registration\Assignment 2\Dataset\p102\mr_bffe.mhd')
image1 = sitk.GetArrayFromImage(image1)

image2 = sitk.ReadImage(r'C:\Users\s159890\Documents\Q3 Jaar 1 (BME)\Capita selecta in image analysis (8DM20)\Registration\Assignment 2\Dataset\p107\mr_bffe.mhd')
image2 = sitk.GetArrayFromImage(image2)

image3 = sitk.ReadImage(r'C:\Users\s159890\Documents\Q3 Jaar 1 (BME)\Capita selecta in image analysis (8DM20)\Registration\Assignment 2\Dataset\p107\prostaat.mhd')
image3 = sitk.GetArrayFromImage(image3)

images = np.stack([image2, image2, image2])
segs = np.stack([image3, image3, image3])

diff_ims = decisionfusing(image1, images, segs)
