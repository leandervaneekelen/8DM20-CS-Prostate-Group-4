import numpy as np
import glob
import elastix
from Import_Files import Import_Files_string
# Make a new transformix object T with the CORRECT PATH to transformix

# TRAINING DATA PATH
data_path = 'C:\\Users\\s081992\\Documents\\TUE\\Year 2\\Q3\\Capita Selecta\\Part 2\\TrainingData\\TrainingData'
# ELASTIX PATH
elastix_path=r'C:\Users\s081992\Documents\TUE\Year 2\Q3\Capita Selecta\Part 2\PracticalSession2019 2\PracticalSession2019\Software\Software\elastix_windows64_v4.7\elastix.exe'
# OUTPUT FOLDER
results_path = r'C:\Users\s081992\Documents\TUE\Year 2\Q3\Capita Selecta\Part 2\pythonforelastix\python'

transformix_path = r'C:\Users\s081992\Documents\TUE\Year 2\Q3\Capita Selecta\Part 2\PracticalSession2019 2\PracticalSession2019\Software\Software\elastix_windows64_v4.7\transformix.exe'

def Transform_GT(data_path, results_path, transformix_path):
    mri, masks_paths = Import_Files_string(data_path)
    
    masks_dict = {}
    for path in masks_paths:
        masks_dict[path[-17:-13]]=path
    
    
    files = glob.glob(results_path+r'\MMI\p*\p*\TransformParameters.0.txt')
    
    for parameterfile in files:
        current_path = parameterfile[:-25]
        T = elastix.TransformixInterface(parameters=parameterfile,
                                     transformix_path=transformix_path)
        # Transform a new image with the transformation parameters
        path_to_transformed_image = T.transform_image(masks_dict[parameterfile[-30:-26]], output_dir=current_path)    
