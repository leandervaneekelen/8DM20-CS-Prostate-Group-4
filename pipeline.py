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
import os

# CONSTANTS
TRESHOLD = 0.7
RUNREGISTRATION = False

# Define paths: these must be altered to use the script on your local machine! 
DATA_PATH = r'C:\Users\s159890\Documents\Q3 Jaar 1 (BME)\Capita selecta in image analysis (8DM20)\Registration\Assignment 2\Dataset'
ELASTIX_PATH = r'C:\Users\s159890\Documents\Q3 Jaar 1 (BME)\Capita selecta in image analysis (8DM20)\Registration\Assignment 2\Practical\Software\elastix_windows64\elastix.exe'
TRANSFORMIX_PATH = r'C:\Users\s159890\Documents\Q3 Jaar 1 (BME)\Capita selecta in image analysis (8DM20)\Registration\Assignment 2\Practical\Software\elastix_windows64\transformix.exe'
RESULT_PATH = r'D:\Leander\8DM20 Capita Selecta Image Analysis\Run 3'

if RUNREGISTRATION:
    #Perform registration on a leave 1-out basis (i.e. register 14 moving images to 1 fixed image, repeat for all images)
    MI = register(DATA_PATH, ELASTIX_PATH, RESULT_PATH) # Returns nxn MI matrix, writes logs and result (registered) images to disk
    
    # Perform calculated registrations on masks and write them to disk 
    Transform_GT(DATA_PATH, RESULT_PATH, TRANSFORMIX_PATH)

else:
    MI = np.load(RESULT_PATH + r'\Mutualinformation.npy')

# Get 'raw' masks & images for comparisons during atlas filtering & dice evaluation at the end
images, masks = Import_Files(DATA_PATH)

# Collect registered images & masks
images_registered = [] 
masks_registered = []
im_reg_paths = glob.glob(RESULT_PATH + '/p*')
for i, path in zip(range(len(im_reg_paths)), im_reg_paths):
    image_registered, mask_registered = Import_Files(path)
    
    # Add dummy images to image/mask_registered to compensate for lack of diagonal 
    # to ease with indexing
    image_registered = np.insert(image_registered, i, np.zeros(image_registered.shape[1:]), axis = 0)
    mask_registered = np.insert(mask_registered, i, np.zeros(mask_registered.shape[1:]), axis = 0)

    images_registered.append(image_registered)
    masks_registered.append(mask_registered)
images_registered = np.stack(images_registered) # Stack images into numpy array for easy storage
masks_registered = np.stack(masks_registered)   # Idem 

# Derive segmentations of prostate of images via the following four methods:
# 1. Simple majority voting decision fusing
# 2. Weighed decision fusing
# 3. Atlas filtering & method 1
# 4. Atlas filtering & method 2

# Calculate which masks survive the treshold (Atlas filtering)
survivors = mi.atlasfiltering(MI, TRESHOLD)

# Execute methods
method_1_segmentations = []
method_2_segmentations = []
method_3_segmentations = []
method_4_segmentations = []

for i, fixed_im, im_regs, im_segs in zip(range(len(image_registered)), images, images_registered, masks_registered):
    # Method 3
    majority_vote_filter = df.decisionfusion_majority(im_segs[survivors[i]])
    method_3_segmentations.append(majority_vote_filter)
    # Method 4
    weighted_vote_filter = df.decisionfusing_weighted(fixed_im, im_regs[survivors[i]], im_segs[survivors[i]])
    method_4_segmentations.append(weighted_vote_filter)
    
    # Delete dummies for the methods that do not include filtering and accidentally include dummies
    #im_regs = np.delete(im_segs, i, axis = 0)
    #im_segs = np.delete(im_segs, i, axis = 0)
    
    # Method 1
    majority_vote = df.decisionfusion_majority(im_segs)
    method_1_segmentations.append(majority_vote)
    # Method 2
    weighted_vote = df.decisionfusing_weighted(fixed_im, im_regs, im_segs)
    method_2_segmentations.append(weighted_vote)

# Merge segmentations into numpy arrays that are convenient to use
method_1_segmentations = np.stack(method_1_segmentations)
method_2_segmentations = np.stack(method_2_segmentations)
method_3_segmentations = np.stack(method_3_segmentations)
method_4_segmentations = np.stack(method_4_segmentations)

# Write images to .mhd in result folder
if not os.path.exists(RESULT_PATH + r"\Results method 1"):
    os.mkdir(RESULT_PATH + r"\Results method 1")
    os.mkdir(RESULT_PATH + r"\Results method 2")
    os.mkdir(RESULT_PATH + r"\Results method 3")
    os.mkdir(RESULT_PATH + r"\Results method 4")

writer = sitk.ImageFileWriter()
for i in range(1, len(method_1_segmentations) + 1):
    # Method 1
    image = sitk.GetImageFromArray(method_1_segmentations[i])
    writer.SetFileName(RESULT_PATH + r"\Results method 1" + r"\segmentation_{}".format(i))
    writer.execute()
    
    # Method 2
    image = sitk.GetImageFromArray(method_2_segmentations[i])
    writer.SetFileName(RESULT_PATH + r"\Results method 2" + r"\segmentation_{}".format(i))
    writer.execute()
    
    # Method 3
    image = sitk.GetImageFromArray(method_3_segmentations[i])
    writer.SetFileName(RESULT_PATH + r"\Results method 3" + r"\segmentation_{}".format(i))
    writer.execute()
    
    # Method 4
    image = sitk.GetImageFromArray(method_4_segmentations[i])
    writer.SetFileName(RESULT_PATH + r"\Results method 4" + r"\segmentation_{}".format(i))
    writer.execute()
    
    
# Issues:
# 2. Writing mhd files from bools
# 3. methods 1 and 2 dummies
    
    
    
    
