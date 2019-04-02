import numpy as np
import glob
import elastix
from Import_Files import Import_Files_string
# Make a new transformix object T with the CORRECT PATH to transformix

def Transform_GT(data_path, results_path, transformix_path):
    """Takes as input a file path to:
        1. Folder where data is stored
        2. Folder where results are stored
        3. Path to transformix.exe file
        
        This function applies the registration found for moving -> fixed image to the masks (groundtruth, GT) of the
        moving image, then writes this as .mhd & .raw files to the same folder as where the registration result & 
        parameter file was written. """

    mri, masks_paths = Import_Files_string(data_path)
    
    # Store all path names in a dictionary according to their patient ID for easy referencing
    # via slicing out path names
    masks_dict = {}
    for path in masks_paths:
        masks_dict[path[-17:-13]]=path
    
    # Collect a list of all transform parameter files
    files = glob.glob(results_path + r'\p*\p*\TransformParameters.0.txt')
    
    # Apply transformation of parameterfile i to its respective mask, then write to file
    for parameterfile in files:
        current_path = parameterfile[:-25]
        T = elastix.TransformixInterface(parameters=parameterfile,
                                     transformix_path=transformix_path)
        path_to_transformed_image = T.transform_image(image_path = masks_dict[parameterfile[-30:-26]], output_dir=current_path)


if __name__ == '__main__':
        # TRAINING DATA PATH
    data_path = 'C:\\Users\\s081992\\Documents\\TUE\\Year 2\\Q3\\Capita Selecta\\Part 2\\TrainingData\\TrainingData'
    # ELASTIX PATH
    elastix_path=r'C:\Users\s081992\Documents\TUE\Year 2\Q3\Capita Selecta\Part 2\PracticalSession2019 2\PracticalSession2019\Software\Software\elastix_windows64_v4.7\elastix.exe'
    # OUTPUT FOLDER
    results_path = r'C:\Users\s081992\Documents\TUE\Year 2\Q3\Capita Selecta\Part 2\pythonforelastix\python'
    
    transformix_path = r'C:\Users\s081992\Documents\TUE\Year 2\Q3\Capita Selecta\Part 2\PracticalSession2019 2\PracticalSession2019\Software\Software\elastix_windows64_v4.7\transformix.exe'