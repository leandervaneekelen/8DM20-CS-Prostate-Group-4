# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 14:22:35 2019

@author: s154994
"""
if __name__ == '__main__':
    user = 'Merel'
    
    if user == 'Merel':
        path = r'C:\Users\s154994\Documents\8DM20_Capita_selecta_EHV\TrainingData'

        
import SimpleITK as sitk
import matplotlib.pyplot as plt
import numpy as np



#mat_mi= #15x15 matrix met de mutual information over de gehele tabel
mat_mi=np.arange(225).reshape(15, 15)

atlasselection=list()
for i in range(mat_mi.shape[0]):
    coord_atlasel=np.nonzero(mat_mi[i,:]/mat_mi[i,:].max()>0.7)
    atlasselection.append(coord_atlasel)
    
    