import elastix
import matplotlib.pyplot as plt
import imageio
import numpy as np
import SimpleITK as sitk




# Define the paths to the two images you want to register
#im1 = 'MR/patient1.jpg'
#im2 = 'MR/patient2.jpg'
#
#im1 = r'C:\Users\s081992\Documents\TUE\Year 2\Q3\Capita Selecta\Part 2\PracticalSession2019 2\PracticalSession2019\chest_xrays\moving_image.mhd'
#im2 = r'C:\Users\s081992\Documents\TUE\Year 2\Q3\Capita Selecta\Part 2\PracticalSession2019 2\PracticalSession2019\chest_xrays\fixed_image.mhd'



im1 = 'C:\\Users\\s081992\\Documents\\TUE\\Year 2\\Q3\\Capita Selecta\\Part 2\\TrainingData\\TrainingData\\p102\\mr_bffe.mhd'
im2 = 'C:\\Users\\s081992\\Documents\\TUE\\Year 2\\Q3\\Capita Selecta\\Part 2\\TrainingData\\TrainingData\\p107\\mr_bffe.mhd'

#im1 = 'C:\\Users\\s081992\\Documents\\TUE\\Year 2\\Q3\\Capita Selecta\\Part 2\\TrainingData\\TrainingData\\p102\\prostaat.mhd'
#im2 = 'C:\\Users\\s081992\\Documents\\TUE\\Year 2\\Q3\\Capita Selecta\\Part 2\\TrainingData\\TrainingData\\p107\\prostaat.mhd'

#im1raw = r'C:\Users\s081992\Documents\TUE\Year 2\Q3\Capita Selecta\Part 2\PracticalSession2019 2\PracticalSession2019\chest_xrays\moving_image.raw'
#im2raw = r'C:\Users\s081992\Documents\TUE\Year 2\Q3\Capita Selecta\Part 2\PracticalSession2019 2\PracticalSession2019\chest_xrays\fixed_image.raw'

# Define a new elastix object 'E' with the CORRECT PATH to elastix
E = elastix.ElastixInterface(elastix_path=r'C:\Users\s081992\Documents\TUE\Year 2\Q3\Capita Selecta\Part 2\PracticalSession2019 2\PracticalSession2019\Software\Software\elastix_windows64_v4.7\elastix.exe')

# Execute the registration. Make sure the paths below are correct, and
# that the results folder exists from where you are running this script

#%%

#path = r'C:\Users\s081992\Documents\TUE\Year 2\Q3\Capita Selecta\Part 2\TrainingData\TrainingData\p102\mr_bffe.mhd'
#image = sitk.ReadImage(path)
#as_array = sitk.GetArrayFromImage(image)
#
#
#
#import SimpleITK as sitk
#image = sitk.ReadImage(im1raw)
#as_array = sitk.GetArrayFromImage(image)
#plt.imshow(as_array[21],cmap = 'gray') # Shows the 22nd slice of the image
#plt.show()
#
##Dim_size=np.array((1024,1024,4),dtype=np.int) #Or read that from your mhd info File
#
#f = open(im1raw,'rb') #only opensraw the file for reading
#img_arr=np.fromfile(f,dtype=np.float64)
#img_arr=img_arr.reshape(Dim_size[0],Dim_size[1])


#%% Excercise 1.
#E.register(
#    fixed_image=im1,
#    moving_image=im2,
#    parameters=['MR/parameters_samplespace_MR.txt'],
#    output_dir='results')


#%% Excercise 2(Bspline).
#E.register(
#    fixed_image=im1,
#    moving_image=im2,
#    parameters=['MR/parameters_bspline_MR.txt'],
#    output_dir='results')

#%% Excercise 3a multiresolution registration.
#E.register(
#    fixed_image=im1,
#    moving_image=im2,
#    parameters=['MR/parameters_bspline_multires_MR.txt'],
#    output_dir='results')

#%% Excercise 3b multiresolution registration.
#E.register(
#    fixed_image=im1,
#    moving_image=im2,
#    parameters=['MR/parameters_samplespace2_MR.txt'],
#    output_dir='results')


#%% 3D registration

E.register(
    fixed_image=im1,
    moving_image=im2,
    parameters=[r'MR/Parameters_Rigid.txt'],
    output_dir='results')
#Parameters_Affine.txt
# Open the logfile into the dictionary L
L = elastix.logfile('results/IterationInfo.0.R0.txt')
plt.figure()
plt.plot(L['itnr'], L['metric'])
plt.show()
#%% 
E.register(
    fixed_image=im1,
    moving_image=im2,
    parameters=[r'MR/Parameters_BSpline.txt'], initial_transform = r'results/TransformParameters.0.txt',
    output_dir='results')
#%%
L = elastix.logfile('results/IterationInfo.0.R0.txt')

# Plot the 'metric' against the iteration number 'itnr'
plt.figure()
plt.plot(L['itnr'], L['metric'])
plt.show()

# Show the resulting image side by side with the fixed and moving image
#fig, ax = plt.subplots(1, 3)
#ax[0].imshow(imageio.imread(im1), cmap='gray')
#ax[1].imshow(imageio.imread(im2), cmap='gray')
#ax[2].imshow(imageio.imread('results/result.0.tiff'), cmap='gray')
#ax[0].title
#plt.show()


im_arr1 = sitk.GetArrayFromImage(sitk.ReadImage(im1))
im_arr2 = sitk.GetArrayFromImage(sitk.ReadImage(im2))
imres = sitk.ReadImage('results/result.0.mhd')
im_arrres = sitk.GetArrayFromImage(imres)
#
#for n in range(40,50):
##    fig, ax = plt.subplots(1, 2)
##    ax[0].imshow(MRI[p,n], cmap='gray')
##    ax[1].imshow(masks[p,n], cmap='gray')
#    
#    fig, ax = plt.subplots(1, 3)
#    ax[0].imshow(im_arr1[n], cmap='gray')
#    ax[1].imshow(im_arr2[n], cmap='gray')
#    ax[2].imshow(im_arrres[n], cmap='gray')
#
#
#
#


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
#
from scrollview import ScrollView
#image = np.load('path/to/image')
#aspect_ratio = [2.3, 0.95, 0.95]  # i.e. the ElementSpacing
aspect_ratio = [2.3, 2.3, 2.3]  # i.e. the ElementSpacing
# Define viewers for every axis
viewer1 = ScrollView(im_arr1)
viewer2 = ScrollView(im_arr2)
viewer3 = ScrollView(im_arrres)
#viewer2 = ScrollView(im.transpose(1, 0, 2))
#viewer3 = ScrollView(im.transpose(2, 0, 1))

# Make three Matplotlib supblots, and populate them with the viewers objects
# The aspect ratios of the different axes need to be defined here as well.
fig, ax = plt.subplots(1, 3)
viewer1.plot(ax[0], cmap='gray', aspect=aspect_ratio[1]/aspect_ratio[2])
viewer2.plot(ax[1], cmap='gray', aspect=aspect_ratio[0]/aspect_ratio[2])
viewer3.plot(ax[2], cmap='gray', aspect=aspect_ratio[0]/aspect_ratio[1])

plt.show()
