# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 10:32:33 2019

@author: s159890
"""

import numpy as np
from scipy.ndimage import gaussian_filter

def decisionfusing(fixed_im, reg_ims, pred_segs):
    """ Takes as input a fixed image (3D numpy array), a series of registered images (4D numpy array) with the
    fixed image as target, and accompanying predicated segmentations per registered image (4D numpy array)
    
    Executes decision fusing technique described in Isgum et al. (2009). Returns a binary, decision fused
    numpy array of same dimensions as fixed image. """
    
    # Constants
    SCALE1 = 0.5
    SCALE2 = 0.5
    EPSILON = 0.001
    
    # Begin by checking dimensions of input arguments
    assert fixed_im.shape == reg_ims[0,:,:,:].shape, "Fixed image dimensions do not match registered images."
    assert fixed_im.shape == pred_segs[0,:,:,:].shape, "Fixed image dimensions do not match predicted segmentation images."
    
    # Allocate memory & calculate difference images
    diff_ims = np.zeros(reg_ims.shape, dtype = reg_ims.dtype)
    for i in range(reg_ims.shape[0]):
        diff_ims[i] = np.abs(reg_ims[i] - fixed_im)
    
    # Blur all volumes with gaussian kernel, then calculate weight images
    for i in range(reg_ims.shape[0]):
        diff_ims[i] = gaussian_filter(diff_ims[i], sigma = SCALE1)
    weights = 1 / (diff_ims + EPSILON)
    
    # Fuse predicted segmentations by taking (normalised) weighted sum
    norm_factor = 1 / (np.sum(weights, axis = 0))    
    fused_pred_segs = norm_factor * np.sum(weights*pred_segs, axis = 0)
    
    # Lastly, blur predictions with scale 2, then treshold for final segmentation
    fused_pred_segs = gaussian_filter(fused_pred_segs, sigma = SCALE2)
    return fused_pred_segs > 0.5
    