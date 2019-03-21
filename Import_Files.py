import matplotlib.pyplot as plt
import SimpleITK as sitk
import glob
import numpy as np



def Import_Files(path):
    """Creates arrays consisting of the image data or image masks. Dimensions of the arrays are [15,86,333,271] consisiting of [patients,slices z direction, x , y] """
    folders = glob.glob(path+r'\p*') 
    folders = glob.glob(folders) 
       
    masks = []
    MRI = []
    for patient in folders:
        files = glob.glob(patient+r'\*')
        im = sitk.ReadImage(files[0])
        m = sitk.ReadImage(files[2])
        im_arr = sitk.GetArrayFromImage(im)
        m_arr = sitk.GetArrayFromImage(m)
        masks.append(m_arr)
        MRI.append(im_arr)
    MRI = np.stack(MRI)
    masks = np.stack(masks)
    return MRI,masks

def Import_Files_string(path):
    """Creates arrays consisting of the directory's for all images"""
    folders = glob.glob(path+r'\p*') 
    
    patient = folders[0]
    
    masks = []
    MRI = []
    for patient in folders:
        files = glob.glob(patient+r'\*')
        masks.append(files[2])
        MRI.append(files[0])
    MRI = np.stack(MRI)
    masks = np.stack(masks)
    return MRI,masks


path= r'C:\Users\s081992\Documents\TUE\Year 2\Q3\Capita Selecta\Part 2\TrainingData\TrainingData'

#%% Optional visualisation of Data
#import random
## Visualise Random patient's Random slice from the centre with corresponding mask.
#fig, ax = plt.subplots(1, 2)
#p = random.randint(0,14)
#n = random.randint(22,50)

#%% Visualise Random patients Mid range prostate
#p = random.randint(0,14)
#for n in range(40,50):
#    fig, ax = plt.subplots(1, 2)
#    ax[0].imshow(MRI[p,n], cmap='gray')
#    ax[1].imshow(masks[p,n], cmap='gray')

