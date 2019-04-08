import elastix
import matplotlib.pyplot as plt
import imageio
import numpy as np
import SimpleITK as sitk
import os
from Import_Files import Import_Files_string

def FindMI(txt):
    with open(txt) as f:
        lines = f.readlines()
    MI = lines[-1].split('\t')
    if MI[1]!= '-1.#IND00':
        MI = float(MI[1])
        return MI


def Affine(f, m, p, path,elastix_path,output, plot = False):
    "Peforms affine transformation, using the fixed image, moving image, provided parameter file"
    E = elastix.ElastixInterface(elastix_path)
    E.register(
    fixed_image=f,
    moving_image=m,
    parameters=[p],
    output_dir= output)
    if plot == True:
        for i in range(4):
#            L = elastix.logfile('{}\IterationInfo.0.R{}.txt'.format(path,i))
            # Plot the 'metric' against the iteration number 'itnr'
            plt.figure()
            plt.plot(L['itnr'], L['metric'])
            plt.tight_layout()
            plt.xlabel('Iteration Number', size = 16)
            plt.ylabel('Mattes Mutual Information', size = 16)
            plt.xticks(size = 14)
            plt.yticks(size = 14)
            
def BSpline(f, m, p,intitaltransform, path, elastix_path,output, plot = False):
    "Peforms BSpline transformation, using the fixed image, moving image, provided parameter file"
    E = elastix.ElastixInterface(elastix_path)
    E.register(
    fixed_image=f,
    moving_image=m,
    parameters=[p], 
    initial_transform =intitaltransform,
    output_dir = output)
    if plot == True:
        for i in range(4):
            L = elastix.logfile('{}\IterationInfo.0.R{}.txt'.format(path,i))
            # Plot the 'metric' against the iteration number 'itnr'
            plt.figure()
            plt.plot(L['itnr'], L['metric'])
            plt.tight_layout()
            plt.xlabel('Iteration Number', size = 16)
            plt.ylabel('Mattes Mutual Information', size = 16)
            plt.xticks(size = 14)
            plt.yticks(size = 14)       
            
def BSplineOnly(f, m, p,path,elastix_path, output,  plot = False):
    "Peforms BSpline transformation, using the fixed image, moving image, provided parameter file"
    E = elastix.ElastixInterface(elastix_path)
    E.register(
    fixed_image=f,
    moving_image=m,
    parameters = [p], 
    output_dir = output)
    if plot == True:
        for i in range(4):
            L = elastix.logfile('{}\IterationInfo.0.R{}.txt'.format(path,i))
            # Plot the 'metric' against the iteration number 'itnr'
            plt.figure()
            plt.plot(L['itnr'], L['metric'])
            plt.tight_layout()
            plt.xlabel('Iteration Number', size = 16)
            plt.ylabel('Mattes Mutual Information', size = 16)
            plt.xticks(size = 14)
            plt.yticks(size = 14)       


def CreateFolder(fixed, moving, path):
    """Creates Folders of stucture path/fixed image/moving image/ where the Registration results can be placed. """
    dir_path = r'{}\{}\{}'.format(path,fixed,moving) # New path
    if not os.path.exists(dir_path): # Checks if the folder exists already
        os.makedirs(dir_path)
    return dir_path

def register(fixed_ims_path, moving_ims_path, elastix_path, results_path,registration = 'BSpline'):
    """Registers the moving images present in moving_ims_paths to all fixed images in fixed_ims_path. To do so, register()
    takes as input four paths, to:
         a) data folder containing fixed images
         b) data folder containing moving images
         c) elastix.exe path
         d) path to results folder
         e) OPTIONAL ARGUMENT: specifying what kind of registration via 'registration' parameter
            Options are: 'Affine', 'BSpline', 'Both' - 'BSpline' is default
    If fixed and moving images paths are identical, this function effectively performs leave-1-out registration
    for the entire set.
    
    Writes registered images and logs files to disk, returns a (mxn) MI numpy array containing the mutual information
    between all fixed images (m) and the registered moving images (n)."""
        
    fixed_ims = Import_Files_string(fixed_ims_path, files_to_import = 'images')
    moving_ims = Import_Files_string(moving_ims_path, files_to_import = 'images')
    
    # Create MI array to stop MI's between fixed and moving images in
    MI = np.zeros((len(fixed_ims),len(moving_ims)))
    MI[:] = np.nan
    
    for i in range(len(fixed_ims)):
        fixed = fixed_ims[i]
        for j in range(len(moving_ims)):
            moving = moving_ims[j]
            if fixed != moving: # Do not compare images with themselves
                destination_path = CreateFolder(fixed[-16:-12], moving[-16:-12], results_path)
                #%% First registration option: Affine.
                if registration == 'Affine':
                    p = r'parameterfiles\Parameters_Affine.txt'
                    Affine(fixed, moving, p,results_path, elastix_path,output = destination_path)
                #%% Second registration option: BSpline
                if registration =='BSpline':
                    p = r'parameterfiles\Parameters_BSpline.txt'
                    BSplineOnly(fixed, moving,p,results_path,elastix_path,output = destination_path)        
                #%% Third registration option: Combination of both Affine and BSpline(using the transformation parameters of the affine registration)
                if registration == 'Both':
                    p = r'parameterfiles\Parameters_BSpline.txt'
                    initial_transform = r'{}\TransformParameters.0.txt'.format(destination_path)            
                    BSpline(fixed, moving,p ,initial_transform,results_path,elastix_path,output = destination_path)           
                
                #%% Storing Mutual information in an 15x15 array. 
                MI[i,j] = FindMI(r'{}\IterationInfo.0.R3.txt'.format(destination_path))
    
    # Write MI array to disk
    np.save(results_path + r'\MutualInformation.npy', MI)        
    return MI

if __name__ == '__main__':
    FIXED_IMAGES_PATH = r'C:\Users\s159890\Documents\Q3 Jaar 1 (BME)\Capita selecta in image analysis (8DM20)\Registration\Assignment 2\Dataset'
    MOVING_IMAGES_PATH = r'C:\Users\s159890\Documents\Q3 Jaar 1 (BME)\Capita selecta in image analysis (8DM20)\Registration\Assignment 2\Dataset'
    ELASTIX_PATH = r'C:\Users\s159890\Documents\Q3 Jaar 1 (BME)\Capita selecta in image analysis (8DM20)\Registration\Assignment 2\Practical\Software\elastix_windows64\elastix.exe'
    TRANSFORMIX_PATH = r'C:\Users\s159890\Documents\Q3 Jaar 1 (BME)\Capita selecta in image analysis (8DM20)\Registration\Assignment 2\Practical\Software\elastix_windows64\transformix.exe'
    RESULT_PATH = r'D:\Leander\8DM20 Capita Selecta Image Analysis\Run 4'
    
    MI = register(FIXED_IMAGES_PATH, MOVING_IMAGES_PATH, ELASTIX_PATH, RESULT_PATH, registration='BSpline')
