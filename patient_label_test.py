#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 16:14:53 2019

@author: alexfassone1
"""

no_hospitals = 2
ini_samples_per_hospital = 2

hospitals = [[] for i in range(no_hospitals)]

#populate hospitals with pre-determined haplotypes 
for i in range (0, ini_samples_per_hospital):
    
    if i < ini_samples_per_hospital/2:
        hospitals[0].append('P' + str(i) + ',H1,0')
        hospitals[1].append('P' + str(i+ini_samples_per_hospital) + ',H2,0')
        
    else:
        hospitals[0].append('P' + str(i) + ',H2,0')
        hospitals[1].append('P' + str(i+ini_samples_per_hospital) + ',H3,0')  
        

print(hospitals)