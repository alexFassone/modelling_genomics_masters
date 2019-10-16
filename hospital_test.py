#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  4 12:37:58 2019

@author: alexfassone1
"""

import numpy as np

no_hospitals = 2
ini_samples_per_hospital = 1

hospitals = [[] for i in range(no_hospitals)]

#populate hospitals with pre-determined haplotypes 
hospitals[0].append(['H1,0', 'H1,1'])
hospitals[0].append(['H2,0'])
hospitals[0][0].append('H1,2')
hospitals[1].append(['H2,0'])

hospitals = [[['H1,0', 'H1,1', 'H1,1', 'H1,2', 'H1,3', 'H1,4', 'H1,1', 'H1,2', 'H1,5', 'H1,2', 'H1,3', 'H1,2', 'H1,5', 'H1,6', 'H1,6', 'H1,6', 'H1,2', 'H1,7', 'H1,3', 'H1,3', 'H1,3', 'H1,4', 'H1,7', 'H1,8', 'H1,3', 'H1,4', 'H1,3', 'H1,4', 'H1,4', 'H1,5', 'H1,2', 'H1,8', 'H1,2', 'H1,3', 'H1,4', 'H1,9', 'H1,5', 'H1,4', 'H1,5', 'H1,10', 'H1,10', 'H1,6', 'H1,7', 'H1,10', 'H1,10', 'H1,3', 'H1,3', 'H1,4', 'H1,8', 'H1,5', 'H1,5', 'H1,3', 'H1,5', 'H1,9', 'H1,2', 'H1,7', 'H1,4', 'H1,5', 'H1,3', 'H1,6', 'H1,7', 'H1,6', 'H1,7', 'H1,9', 'H1,3', 'H1,11', 'H1,3', 'H1,7', 'H1,9', 'H1,4', 'H1,9', 'H1,5', 'H1,4', 'H1,4'], ['H2,0', 'H2,1', 'H2,2', 'H2,1', 'H2,2', 'H2,3', 'H2,1', 'H2,1', 'H2,4', 'H2,3', 'H2,3', 'H2,2', 'H2,4', 'H2,4', 'H2,2', 'H2,4', 'H2,1', 'H2,4', 'H2,2', 'H2,4', 'H2,4', 'H2,3', 'H2,5', 'H2,5', 'H2,2', 'H2,3', 'H2,3', 'H2,4', 'H2,3', 'H2,4', 'H2,6', 'H2,3', 'H2,6', 'H2,3', 'H2,5', 'H2,7', 'H2,3', 'H2,5', 'H2,4', 'H2,2', 'H2,4', 'H2,8', 'H2,4', 'H2,5', 'H2,6', 'H2,4', 'H2,3', 'H2,4', 'H2,4', 'H2,9', 'H2,3', 'H2,4', 'H2,7', 'H2,4', 'H2,4', 'H2,5', 'H2,4', 'H2,5', 'H2,7', 'H2,4', 'H2,4', 'H2,6'], ['H2,2'], ['H2,3', 'H2,4'], ['H2,2', 'H2,3'], ['H1,1'], ['H2,2'], ['H2,5'], ['H2,2'], ['H1,6'], ['H2,2'], ['H2,7']], [['H2,0', 'H2,1', 'H2,2', 'H2,2', 'H2,3', 'H2,3', 'H2,4', 'H2,4', 'H2,3', 'H2,3', 'H2,4', 'H2,3', 'H2,4', 'H2,4', 'H2,5', 'H2,5', 'H2,4', 'H2,5', 'H2,5', 'H2,5', 'H2,4', 'H2,5', 'H2,6', 'H2,4', 'H2,5', 'H2,5', 'H2,5', 'H2,5', 'H2,1', 'H2,6'], ['H2,2', 'H2,3', 'H2,3', 'H2,4', 'H2,3', 'H2,4', 'H2,5', 'H2,5', 'H2,3', 'H2,6', 'H2,4', 'H2,5', 'H2,6', 'H2,7', 'H2,4', 'H2,4', 'H2,4', 'H2,4', 'H2,4', 'H2,6'], ['H1,1', 'H1,2', 'H1,2'], ['H1,5', 'H1,6', 'H1,6', 'H1,7', 'H1,7', 'H1,7'], ['H2,2', 'H2,3'], ['H2,4'], ['H1,1'], ['H2,1', 'H2,2', 'H2,2', 'H2,2', 'H2,3', 'H2,4'], ['H12,4'], ['H2,0', 'H2,1'], ['H1,1'], ['H1,3', 'H1,4'], ['H5,2']]]

hospital_tally = [[] for i in range(no_hospitals)]
hospital_proportion = [[] for i in range(no_hospitals)]
hospital_total = np.zeros(no_hospitals)
haplotypes = []

for i in range (0, len(hospitals)):
    for j in range(0, len(hospitals[i])):
        
        add = True
        
        if len(haplotypes) == 0:
            add = True    
        else:
            for k in range(0, len(haplotypes)):
                if hospitals[i][j][0].split(sep = ",")[0] == haplotypes[k]:
                    add = False

        if add == True:
            haplotypes.append(hospitals[i][j][0].split(sep = ",")[0])
            
for i in range (0, len(hospitals)):
    for j in range(0, len(haplotypes)):
        hospital_tally[i].append(0)
        hospital_proportion[i].append(0)

for i in range (0, len(hospitals)):
    for j in range(0, len(hospitals[i])):
        for k in range(0, len(hospitals[i][j])):
            
            for l in range(0, len(haplotypes)):
                if hospitals[i][j][k].split(sep = ",")[0] == haplotypes[l]:
                    hospital_tally[i][l] += 1
                    hospital_total[i] += 1
                           
for i in range (0, len(hospitals)):
    for j in range(0, len(haplotypes)):
        hospital_proportion[i][j] = hospital_tally[i][j]/hospital_total[i]
        

            
