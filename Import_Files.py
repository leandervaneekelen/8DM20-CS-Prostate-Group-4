import matplotlib.pyplot as plt
import SimpleITK as sitk
import glob
import numpy as np

def Import_Files(path, files_to_import = 'both'):
    """Creates arrays consisting of the image data or image masks. 
    Dimensions of the arrays are [15,86,333,271] consisiting of [patients,slices z direction, x , y] 
    Optional 'files_to_import' parameter specifies whether the function should import 
    the images ('images'), the masks 'masks', or both ('both').
    """
    folders = glob.glob(path+r'\p*') 
       
    masks = []
    MRI = []
    
    if files_to_import == 'images':
        for patient in folders:
            files = glob.glob(patient+r'\*.mhd')
            im = sitk.ReadImage(files[0])
            MRI.append(sitk.GetArrayFromImage(im))
        MRI = np.stack(MRI)
        return MRI
    
    if files_to_import == 'masks':
        for patient in folders:
            files = glob.glob(patient+r'\*.mhd')
            m = sitk.ReadImage(files[1])
            masks.append(sitk.GetArrayFromImage(m))
        masks = np.stack(masks)
        return masks
    
    if files_to_import == 'both':
        for patient in folders:
            files = glob.glob(patient+r'\*.mhd')
            im = sitk.ReadImage(files[0])
            MRI.append(sitk.GetArrayFromImage(im))
            m = sitk.ReadImage(files[1])
            masks.append(sitk.GetArrayFromImage(m)) 
        MRI = np.stack(MRI)
        masks = np.stack(masks)
        return MRI,masks

def Import_Files_string(path, files_to_import = 'both'):
    """Creates arrays consisting of the directory's for all images
    Optional 'files_to_import' parameter specifies whether the function should import the paths to
    images ('images'), the masks 'masks', or both ('both').
    """
    folders = glob.glob(path+r'\p*') 

    masks = []
    MRI = []
    
    if files_to_import == 'images':
        for patient in folders:
            files = glob.glob(patient+r'\*.mhd')
            MRI.append(files[0])
        MRI = np.stack(MRI)
        return MRI
    
    if files_to_import == 'masks':
        for patient in folders:
            files = glob.glob(patient+r'\*.mhd')
            masks.append(files[1])
        masks = np.stack(masks)
        return masks
    
    if files_to_import == 'both':
        for patient in folders:
            files = glob.glob(patient+r'\*.mhd')
            MRI.append(files[0])
            masks.append(files[1])
        MRI = np.stack(MRI)
        masks = np.stack(masks)
        return MRI, masks

if __name__ == '__main__':
    path= r'C:\Users\s159890\Documents\Q3 Jaar 1 (BME)\Capita selecta in image analysis (8DM20)\Registration\Assignment 2\DatasetValidatie'
    images_validation = Import_Files(path, files_to_import='images')

#%% Optional visualisation of Data
#import random
## Visualise Random patient's Random slice from the centre with corresponding mask.
#fig, ax = plt.subplots(1, 2)
#p = random.randint(0,14)
#n = random.randint(22,50)
#ax[0].imshow(MRI[p,n], cmap='gray')
#ax[1].imshow(masks[p,n], cmap='gray')

#%% Visualise Random patients Mid range prostate
#p = random.randint(0,14)
#for n in range(40,50):
#    fig, ax = plt.subplots(1, 2)
#    ax[0].imshow(MRI[p,n], cmap='gray')
#    ax[1].imshow(masks[p,n], cmap='gray')

