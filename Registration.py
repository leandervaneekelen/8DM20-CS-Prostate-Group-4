#import elastix
import matplotlib.pyplot as plt
import imageio
import numpy as np
import SimpleITK as sitk
import os
from Import_Files import Import_Files_string

def FindMI(txt):
    with open(txt) as f:
        lines = f.readlines()
    MI = lines[len(lines)-1].split('\t')
<<<<<<< HEAD
    if MI[1] is not '-1.#IND00':
        MI = float(MI[1])
        return MI

def Affine(f, m, p,path, output, plot = False):
=======
    MI = float(MI[1])
    return MI

def Affine(f, m, p, output,path, plot = False):
>>>>>>> d09163fc4aabc1ca92e0b7e52a7be024d8743d01
    "Peforms affine transformation, using the fixed image, moving image, provided parameter file"
    E.register(
    fixed_image=f,
    moving_image=m,
    parameters=[p],
    output_dir= output)
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
            
<<<<<<< HEAD
def BSpline(f, m, p,intitaltransform, path, output, plot = False):
=======
def BSpline(f, m, p,intitaltransform, output, path, plot = False):
>>>>>>> d09163fc4aabc1ca92e0b7e52a7be024d8743d01
    "Peforms BSpline transformation, using the fixed image, moving image, provided parameter file"
    E.register(
    fixed_image=f,
    moving_image=m,
    parameters=[p], 
    initial_transform =intitaltransform,
    output_dir = output)
    if plot == True:
        for i in range(4):
            L = elastix.logfile('{}\IterationInfo.0.R{}.txt'.format(path,i))
<<<<<<< HEAD
            # Plot the 'metric' against the iteration number 'itnr'
            plt.figure()
            plt.plot(L['itnr'], L['metric'])
            plt.tight_layout()
            plt.xlabel('Iteration Number', size = 16)
            plt.ylabel('Mattes Mutual Information', size = 16)
            plt.xticks(size = 14)
            plt.yticks(size = 14)       
            
def BSplineOnly(f, m, p,path, output,  plot = False):
    "Peforms BSpline transformation, using the fixed image, moving image, provided parameter file"
    E.register(
    fixed_image=f,
    moving_image=m,
    parameters=[p], 
    output_dir = output)
    if plot == True:
        for i in range(4):
            L = elastix.logfile('{}\IterationInfo.0.R{}.txt'.format(path,i))
=======
>>>>>>> d09163fc4aabc1ca92e0b7e52a7be024d8743d01
            # Plot the 'metric' against the iteration number 'itnr'
            plt.figure()
            plt.plot(L['itnr'], L['metric'])
            plt.tight_layout()
            plt.xlabel('Iteration Number', size = 16)
            plt.ylabel('Mattes Mutual Information', size = 16)
            plt.xticks(size = 14)
            plt.yticks(size = 14)       
            
def BSplineOnly(f, m, p, output, path, plot = False):
    "Peforms BSpline transformation, using the fixed image, moving image, provided parameter file"
    E.register(
    fixed_image=f,
    moving_image=m,
    parameters=[p], 
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

<<<<<<< HEAD
def CreateFolder(fixed, moving, path):
    """Creates Folders of stucture path/fixed image/moving image/ where the Registration results can be placed. """
    dir_path = r'{}\{}\{}'.format(path,fixed,moving) # New path
    if not os.path.exists(dir_path): # Checks if the folder exists already
        os.makedirs(dir_path)
    return dir_path

=======
>>>>>>> d09163fc4aabc1ca92e0b7e52a7be024d8743d01
# TRAINING DATA PATH
data_path = 'C:\\Users\\s081992\\Documents\\TUE\\Year 2\\Q3\\Capita Selecta\\Part 2\\TrainingData\\TrainingData'
# ELASTIX PATH
elastix_path=r'C:\Users\s081992\Documents\TUE\Year 2\Q3\Capita Selecta\Part 2\PracticalSession2019 2\PracticalSession2019\Software\Software\elastix_windows64_v4.7\elastix.exe'
# OUTPUT FOLDER
results_path = r'C:\Users\s081992\Documents\TUE\Year 2\Q3\Capita Selecta\Part 2\pythonforelastix\python'


scans , masks = Import_Files_string(data_path)

E = elastix.ElastixInterface(elastix_path)

MI = np.zeros((len(scans),len(scans)))
MI[:] = np.nan
#%%
# Loop over all combinations of images to calculate the registeration.
# Currently the 2 options are still "implemented in comments". 
#1. Just running the BSpline.
#2. appending the MI to a dict with key = p###
# Both can be deleted, however the np array was giving me a lot of trouble. 

#mi = {}
for i in range(len(scans)):
#    j=0
    fixed = scans[i]
#    mi[fixed[-16:-12]]=[]
    
    for j in range(len(scans)):
        if i !=j:
            
            moving = scans[j]
            destination_path = CreateFolder(fixed[-16:-12],moving[-16:-12], results_path)
            #%% First registration, affine.
<<<<<<< HEAD
#            p = r'Parameters_Affine.txt'
#            Affine(fixed, moving, p,results_path, output = destination_path)


            #%% Second registration, BSpline(using the affine registration).
#            initial_transform = r'{}\TransformParameters.0.txt'.format(destination_path)
            p = r'Parameters_BSpline.txt'
#            BSpline(fixed, moving,p ,initial_transform,results_path,output = destination_path)
            BSplineOnly(fixed, moving,p,results_path,output = destination_path)        
            #%% Storing Mutual information in an 15x15 array. 
            
=======
            p = r'Parameters_Affine.txt'
            Affine(fixed, moving, p,results_path, output = destination_path)
                        
            #%% Second registration, BSpline(using the affine registration).
            initial_transform = r'{}\TransformParameters.0.txt'.format(destination_path)
            p = r'Parameters_BSpline.txt'
            BSpline(fixed, moving,p ,initial_transform,results_path,output = destination_path)
    #        BSplineOnly(fixed, moving,p,results_path,output = destination_path)        
            #%% Storing Mutual information in an 15x15 array. 
>>>>>>> d09163fc4aabc1ca92e0b7e52a7be024d8743d01
            MI[i,j] = FindMI(r'{}\IterationInfo.0.R3.txt'.format(destination_path))
#            mi[fixed[-16:-12]].append(FindMIdict(r'{}\IterationInfo.0.R3.txt'.format(destination_path)))
            
            
            
            
#!!!!STILL TO BE DONE: **Calculate the deformations based on the written paramater file
np.save('MutualInformation.npy',MI)


#%% Calculate average, taking the annoying error into account. 
# appending (image_indes, threshold) into thresh
# Can be deleted as well, but might be useful to look at the MI output. 
avlist = []
thresh = []

<<<<<<< HEAD
arr =np.load('Affine_BSpline_MI.npy')
#arr = np.load('Affine_BSpline.npy')
=======
arr = np.load('Affine_BSpline.npy')
>>>>>>> d09163fc4aabc1ca92e0b7e52a7be024d8743d01
for i in range(arr.shape[0]):
    row = arr[i]
    s = 0
    n = 0
    for j in range(len(row)):
<<<<<<< HEAD
#        if arr[i][j] != '-1.#IND00':
        if i!=j:
=======
        if arr[i][j] != '-1.#IND00':
>>>>>>> d09163fc4aabc1ca92e0b7e52a7be024d8743d01
            s += float(arr[i][j])
            n +=1
            if float(arr[i][j]) <avlist[i]:
                thresh.append((i,float(arr[i][j])))
<<<<<<< HEAD
#    print(n)
=======
    print(n)
>>>>>>> d09163fc4aabc1ca92e0b7e52a7be024d8743d01
    avlist.append(s/n)

#
#im_arr1 = sitk.GetArrayFromImage(sitk.ReadImage(im1))
#im_arr2 = sitk.GetArrayFromImage(sitk.ReadImage(im2))
#imres = sitk.ReadImage('results/result.0.mhd')
#im_arrres = sitk.GetArrayFromImage(imres)

# Make a new transformix object T with the CORRECT PATH to transformix
#T = elastix.TransformixInterface(parameters='results/TransformParameters.0.txt',
#                                 transformix_path=r'C:\Users\s081992\Documents\TUE\Year 2\Q3\Capita Selecta\Part 2\PracticalSession2019 2\PracticalSession2019\Software\Software\elastix_windows64_v4.7\transformix.exe')

# Transform a new image with the transformation parameters
#path_to_transformed_image = T.transform_image(im1, output_dir='results')
#
## Get the Jacobian matrix
#path_to_jacobian_matrix = T.jacobian_matrix(output_dir='results')
#
## Get the Jacobian determinant
#path_to_jacobian_determinant = T.jacobian_determinant(output_dir='results')
#
## Get the full deformation field
#path_to_deformation_field = T.deformation_field(output_dir='results')
