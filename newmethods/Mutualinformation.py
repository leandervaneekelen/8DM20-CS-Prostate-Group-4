# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 14:22:35 2019

@author: s154994/s159890
"""

import numpy as np

def atlasfiltering(mat_mi, treshold = 0.7):
    """Takes as input a 2 dimensional numpy array describing for all leave-n-out iterations what the
    mutual information is of image i with all registered images. Diagonal is filled with NaNs (images
    are not compared with themselves). Optional argument treshold describes treshold (alpha, see 
    Klein et al.) that needs to be met for the atlas to pass the filtering.
    
    Returns a list with, per row, a 1 dimensional numpy array describing what atlases met the treshold."""
    
    atlasselection = list()
    
    for i in range(mat_mi.shape[0]):
        # Normalise all MI's with the maximum out of that row, then treshold
        tresholded_mat_mi = np.abs(mat_mi[i,:]) / np.nanmax(np.abs(mat_mi[i,:])) > treshold
        coord_atlases = np.nonzero(tresholded_mat_mi)
        atlasselection.append(coord_atlases[0])
    
    return atlasselection


