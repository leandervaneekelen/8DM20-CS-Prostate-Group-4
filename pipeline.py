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
from newmethods import Import_Files as imp_fs
from newmethods.dice import dice
from newmethods.Transform_GT import Transform_GT
from newmethods.Registration import register

# Import all packages relevant for pipeline
from scipy.stats import wilcoxon
import numpy as np
import SimpleITK as sitk
import matplotlib.pyplot as plt
import glob
import os

# CONSTANTS
TRESHOLD = 0.7
RUNREGISTRATION = True

# Define paths: these must be altered to use the script on your local machine! 
DATA_PATH = r'C:\Users\s159890\Documents\Q3 Jaar 1 (BME)\Capita selecta in image analysis (8DM20)\Registration\Assignment 2\Dataset'
ELASTIX_PATH = r'C:\Users\s159890\Documents\Q3 Jaar 1 (BME)\Capita selecta in image analysis (8DM20)\Registration\Assignment 2\Practical\Software\elastix_windows64\elastix.exe'
TRANSFORMIX_PATH = r'C:\Users\s159890\Documents\Q3 Jaar 1 (BME)\Capita selecta in image analysis (8DM20)\Registration\Assignment 2\Practical\Software\elastix_windows64\transformix.exe'
RESULT_PATH = r'D:\Leander\8DM20 Capita Selecta Image Analysis\Run 4'

if RUNREGISTRATION:
    #Perform registration on a leave 1-out basis (i.e. register 14 moving images to 1 fixed image, repeat for all images)
    MI = register(DATA_PATH, ELASTIX_PATH, RESULT_PATH) # Returns nxn MI matrix, writes logs and result (registered) images to disk
    
    # Perform calculated registrations on masks and write them to disk 
    Transform_GT(DATA_PATH, RESULT_PATH, TRANSFORMIX_PATH)

else:
    MI = np.load(RESULT_PATH + r'\Mutualinformation.npy')

# Get 'raw' masks & images for comparisons during atlas filtering & dice evaluation at the end
images, masks = imp_fs.Import_Files(DATA_PATH)

# Collect registered images & masks
images_registered = [] 
masks_registered = []
im_reg_paths = glob.glob(RESULT_PATH + '/p*')
for i, path in zip(range(len(im_reg_paths)), im_reg_paths):
    image_registered, mask_registered = imp_fs.Import_Files(path)
    
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
# 2. Weighted decision fusing
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
    im_regs = np.delete(im_segs, i, axis = 0)
    im_segs = np.delete(im_segs, i, axis = 0)
    
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
for i in range(len(method_1_segmentations)):
    # Multiply image segmentations by 255 to convert from bool to int (0..255)
    # Method 1
    image = sitk.GetImageFromArray(method_1_segmentations[i] * 255)
    writer.SetFileName(RESULT_PATH + r"\Results method 1" + r"\segmentation_{}.mhd".format(i+1))
    writer.Execute(image)
    
    # Method 2
    image = sitk.GetImageFromArray(method_2_segmentations[i] * 255)
    writer.SetFileName(RESULT_PATH + r"\Results method 2" + r"\segmentation_{}.mhd".format(i+1))
    writer.Execute(image)
    
    # Method 3
    image = sitk.GetImageFromArray(method_3_segmentations[i] * 255)
    writer.SetFileName(RESULT_PATH + r"\Results method 3" + r"\segmentation_{}.mhd".format(i+1))
    writer.Execute(image)
    
    # Method 4
    image = sitk.GetImageFromArray(method_4_segmentations[i] * 255)
    writer.SetFileName(RESULT_PATH + r"\Results method 4" + r"\segmentation_{}.mhd".format(i+1))
    writer.Execute(image)
    
# Performing 'evaluation' of segmentations via calculation of dice score
dice_scores_method_1 = []
dice_scores_method_2 = []
dice_scores_method_3 = []
dice_scores_method_4 = []
for i in range(len(images)):
    gt = masks[i].flatten()
    
    dice_method_1_i = dice(gt, method_1_segmentations[i].flatten())
    dice_scores_method_1.append(dice_method_1_i)
    dice_method_2_i = dice(gt, method_2_segmentations[i].flatten())
    dice_scores_method_2.append(dice_method_2_i)
    dice_method_3_i = dice(gt, method_3_segmentations[i].flatten())
    dice_scores_method_3.append(dice_method_3_i)
    dice_method_4_i = dice(gt, method_4_segmentations[i].flatten())
    dice_scores_method_4.append(dice_method_4_i)

# PROBABLY BEST TO DELETE EVERYTHING UNDER THIS

# Making boxplots
methods= [dice_scores_method_1, dice_scores_method_2, dice_scores_method_3, dice_scores_method_4]

fig, ax = plt.subplots()
bp= ax.boxplot(methods)
ax.set_xticklabels(["Majority voting", "Weighted voting", "Atlas filtering, \n majority voting", "Atlas filtering,\n weighted voting"],
                   rotation = 0, fontsize = 11)
ax.set_xlabel('Methods', fontsize = 11)
ax.set_ylabel('Dice score', fontsize = 11)
ax.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
ax.set_axisbelow(True)
ax.set_ylim(-0.05, 1.0)
plt.show()

# Test significance of difference between results
T1, p1 = wilcoxon(dice_scores_method_1, dice_scores_method_2)
T2, p2 = wilcoxon(dice_scores_method_1, dice_scores_method_3)    
T3, p3 = wilcoxon(dice_scores_method_1, dice_scores_method_4)
# Outcome: Methods 2, 3, 4 all differe significantly from 1

T4, p4 = wilcoxon(dice_scores_method_2, dice_scores_method_3)
T5, p5 = wilcoxon(dice_scores_method_2, dice_scores_method_4)    
# Outcome: Methods 3 and 4 do not vary significantly from 2

T6, p6 = wilcoxon(dice_scores_method_3, dice_scores_method_4)


