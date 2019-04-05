# -*- coding: utf-8 -*-
"""
Created on Fri Feb 22 14:49:50 2019

@author: s159890
"""

# dice.py
# Function that compares (binary) numpy arrays and returns Dice score to quantify 'overlay' of images
import numpy as np

def dice(image, mask):
    # Check if dimensions of image and mask are the same
    if (image.size != mask.size):
        raise ValueError("Sizes of arguments are not identical.")
    
    dice = np.sum(image[mask == np.max(mask)]*2.0 / (np.sum(image) + np.sum(mask == np.max(mask))));
    return dice


