# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 11:10:26 2019

@author: s159890, group 4 of 8DM20, Capita Selecta prostate
"""

# A new day, a fresh start

#pipeline.py
# Main script for 8DM20 Capita Selecta of Image Analysis, Prostate, group 4

# Import all necessary methods written by group
from newmethods import decisionfusing as df
from newmethods import Mutualinformation as mi
from Import_Files import Import_Files_string, Import_Files
from Registration import register
from Transform_GT import Transform_GT

# Import all packages relevant for pipeline
import numpy as np
import SimpleITK as sitk
import glob

# CONSTANTS
TRESHOLD = 0.7
RUNREGISTRATION = False

# Define paths: these must be altered to use the script on your local machine! 
DATA_PATH = r'C:\Users\s159890\Documents\Q3 Jaar 1 (BME)\Capita selecta in image analysis (8DM20)\Registration\Assignment 2\Dataset'
ELASTIX_PATH = r'C:\Users\s159890\Documents\Q3 Jaar 1 (BME)\Capita selecta in image analysis (8DM20)\Registration\Assignment 2\Practical\Software\elastix_windows64\elastix.exe'
TRANSFORMIX_PATH = r'C:\Users\s159890\Documents\Q3 Jaar 1 (BME)\Capita selecta in image analysis (8DM20)\Registration\Assignment 2\Practical\Software\elastix_windows64\transformix.exe'
RESULT_PATH = r'D:\Leander\8DM20 Capita Selecta Image Analysis\Run 2'

if RUNREGISTRATION:
    #Perform registration on a leave 1-out basis (i.e. register 14 moving images to 1 fixed image, repeat for all images)
    MI = register(DATA_PATH, RESULT_PATH, TRANSFORMIX_PATH) # Returns nxn MI matrix, writes logs and result (registered) images to disk
    
    # Perform calculated registrations on masks and write them to disk 
    Transform_GT(DATA_PATH, RESULT_PATH, TRANSFORMIX_PATH)

else:
    MI = np.load('Mutualinformation.npy')

# Get 'raw' masks & images for comparisons during atlas filtering & dice evaluation at the end
images, masks = Import_Files(DATA_PATH)

# Collect registered images & masks
images_registered = [] 
masks_registered = []
im_reg_paths = glob.glob(RESULT_PATH + '/*')
for path in im_reg_paths:
    image_registered, mask_registered = Import_Files(path)
    images_registered.append(image_registered)
    masks_registered.append(mask_registered)
images_registered = np.stack(images_registered) # Stack images into numpy array for easy storage
masks_registered = np.stack(masks_registered)   # Idem 

# Calculate which masks survive the treshold (Atlas filtering)
survivors = mi.atlasfiltering(MI, TRESHOLD)

# Derive segmentations of prostate of images via the following four methods:
# 1. Simple majority voting decision fusing
# 2. Weighed decision fusing
# 3. Atlas filtering & method 1
# 2. Atlas filtering & method 2

method_1_segmentation = df.decisionfusion_majority()





