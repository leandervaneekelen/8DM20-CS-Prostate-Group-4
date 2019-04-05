# 8DM20-CS-Prostate-Group-4
Repository for project work of Group 4 on 8DM20, Capita Selecta in Medical Image Analysis

-----------------
TABLE OF CONTENTS
-----------------

#1. Introduction
#2. Contents of this package
#3. Installation guide
#4. Getting started
#5. Changing Parameters and Functions

-----------------
#1 - Introduction
-----------------

This script package was written for Capita Selecta in Medical Image Analysis (8QC00), a project
running in Q3 of academic year 2018-2019 for ME. The scripts were written by 
group 4 for the case 'Evaluating the Effects of Atlas Filtering and Different Methods of Decision Fusing
 on Atlas Based Image Segmentation of Prostate Images'. 

Members of group 7:
* Leander van Eekelen (0966869, l.v.eekelen@student.tue.nl)
* Kees van Dorp (0653884, a.c.v.dorp@student.tue.nl)
* Merel Eussen (0964211, m.j.a.eussen@student.tue.nl)
* Milan Gillissen (0861128, m.gillissen@student.tue.nl)
* Teun van de Meerakker (0865482 t.v.d.meerakkker@student.tue.nl)

This script package offers the Python scripts necessary to perform Image Registration,
 Mask Deformation and different descision fusing techniques.

-----------------------------
#2 - Contents of this package
-----------------------------

The package the user has received from group 4 should contain the following scripts and parameterfiles.

Scripts:
* pipeline.py
* Import_Files.py
* Registration.py
* Transform_GT.py
* decisionfusing.py
* Mutualinformation.py

Moreover, it should contain the following data set:
* a prostate image set, containing 15 patients. For each patient a MRI with mhd and raw file, and a prostate segmentation with its own mhd and raw file.
And finally the parameter Files for the registration:
* Parameters_BSpline.txt
* Parameters_Affine.txt

If one or more items on this list are missing, please contact one of the group members,
mentioned in #1 - Introduction.

------------------------
#3 - Installation guide
------------------------

To function, the user should extract all the scripts to the same directory.
The scripts require the standard software for project subject (8QC00).

Furthermore the script uses the elasix and transformix software:
S. Klein, M. Staring, K. Murphy, M. A. Viergever and J. P. W. Pluim, "elastix: A Toolbox for Intensity-Based Medical Image Registration," in IEEE Transactions on Medical Imaging, vol. 29, no. 1, pp. 196-205, Jan. 2010.
doi: 10.1109/TMI.2009.2035616

--------------------
#4 - Getting Started
--------------------
To start the script the user should run the 'pipeline.py' Python file. 
- The Threshold value has a default value of 0.7
- RUNREGISTRATION should be set to True
- The following paths should be set to the users own paths
  - DATA_PATH: path to the data provided (described in #2). Path should contain the p*** folders. 
  - ELASTIX_PATH : path to the elasix execute file. 
  - RESULTS_PATH : path were the resulting data is saved. 
  - TRANSFORMIX_PATH : path to the transformix execute file. 
  
When commands have been successfully filled in, the program will start the registration. This will register every moving image to a fixed image. 
This process takes around 2.5 hours. 
In the results_path folders structures of fixed_image/moving_images will occur. With:
- IterationInfo.0.R#: The iteration information for all 4 resolutions. 
- results.0.mhd: The deformed moving MRI image 
- results: The deformed ground truth of the moving MRI image
- TransformParameters.0.R# : The transform parameters for all 4 resolutions.

For each of the voting methods a binary masks will be returned as an mhd file, in the results subfolder: Results_method_#
Each folder contains a binary mhd file, consisting of the segmentation of the prostate. 

--------------------------------------
#5 - Changing Parameters and Functions
--------------------------------------

#5.1 Registration
Changes in Registration can be made in de following line, by adding registration = 'Affine', 'BSpline'(default) or 'Both').
MI = register(DATA_PATH, ELASTIX_PATH, RESULT_PATH)
To alter the registration parameters, changes can be made in the corresponding parameterfiles: Parameters_BSpline.txt or Parameters_Affine.txt located in the parameterfiles folder. 

#5.2 Decision fusing
Treshold can be set between 0 and 1, as a float. This responds to the normalised value for each image. Set to 0 is equal to major voting, but is reccomended to be set at a fairy high level.

