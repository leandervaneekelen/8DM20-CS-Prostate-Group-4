import elastix
import matplotlib.pyplot as plt
import imageio
import numpy as np
import SimpleITK as sitk

from Import_Files import Import_Files_string

def FindMI(txt):
    with open(txt) as f:
        lines = f.readlines()
    MI = lines[len(lines)-1].split('\t')
    MI = float(MI[1])
    return MI

path = 'C:\\Users\\s081992\\Documents\\TUE\\Year 2\\Q3\\Capita Selecta\\Part 2\\TrainingData\\TrainingData'
elastix_path=r'C:\Users\s081992\Documents\TUE\Year 2\Q3\Capita Selecta\Part 2\PracticalSession2019 2\PracticalSession2019\Software\Software\elastix_windows64_v4.7\elastix.exe'
scans , masks = Import_Files_string(path)

E = elastix.ElastixInterface(elastix_path)

MI = np.zeros((len(scans),len(scans)))
MI[:] = np.nan

# Loop over all combinations of images to calculate the registeration.
    for i in range(len(scans)):
        j=0
#    for j in range(len(scans)):
        if i !=j:
            fixed = scans[i]
            moving = scans[j]
            #%% First registration, affine.
            E.register(
                fixed_image = fixed,
                moving_image = moving,
                parameters=[r'MR/Parameters_Affine.txt'],
                output_dir='results')
            #Parameters_Affine.txt
            # Open the logfile into the dictionary L
            L = elastix.logfile('results/IterationInfo.0.R0.txt')
            
#            Plot and store the registration metric vs. the number of iterations?
            plt.figure()
            plt.plot(L['itnr'], L['metric'])
            

            
            #%% Second registration following the affine registration. 
            E.register(
                fixed,
                moving,
                parameters=[r'MR/Parameters_BSpline.txt'], initial_transform = r'results/TransformParameters.0.txt',
                output_dir='results')
            
            # Open the logfile into the dictionary L
            L = elastix.logfile('results/IterationInfo.0.R0.txt')
            
#            Plot and store the registration metric vs. the number of iterations?
            plt.figure()
            plt.plot(L['itnr'], L['metric'])
 
            
            #%% Storing Mutual information in an 15x15 array. 
            MI[i,j] = FindMI('results/IterationInfo.0.R4.txt')

#            **STORE IMAGES ---> MHD file? NP Array?
#            **Calculate the deformations based on the written paramater file


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
#%% Scroll through the fixed, moving and registrated images
#from scrollview import ScrollView
##image = np.load('path/to/image')
##aspect_ratio = [2.3, 0.95, 0.95]  # i.e. the ElementSpacing
#aspect_ratio = [2.3, 2.3, 2.3]  # i.e. the ElementSpacing
## Define viewers for every axis
#viewer1 = ScrollView(im_arr1)
#viewer2 = ScrollView(im_arr2)
#viewer3 = ScrollView(im_arrres)
##viewer2 = ScrollView(im.transpose(1, 0, 2))
##viewer3 = ScrollView(im.transpose(2, 0, 1))
#
## Make three Matplotlib supblots, and populate them with the viewers objects
## The aspect ratios of the different axes need to be defined here as well.
#fig, ax = plt.subplots(1, 3)
#viewer1.plot(ax[0], cmap='gray', aspect=aspect_ratio[1]/aspect_ratio[2])
#viewer2.plot(ax[1], cmap='gray', aspect=aspect_ratio[0]/aspect_ratio[2])
#viewer3.plot(ax[2], cmap='gray', aspect=aspect_ratio[0]/aspect_ratio[1])
