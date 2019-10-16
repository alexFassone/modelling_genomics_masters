#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 13:10:27 2019

@author: alexfassone1
"""

import numpy as np

def hospital_setup(no_hospitals, ini_trees_per_hospital, haplotypes, hospital_haplotype_distribution):
    
    hospitals = [[] for i in range(no_hospitals)]
    
    for i in range(no_hospitals):
        for j in range(len(haplotypes)):
            for k in range(int(ini_trees_per_hospital[i] * hospital_haplotype_distribution[i][j])):
                hospitals[i].append([haplotypes[j]])
                
    return hospitals

def haplotype_fraction(hospitals):
    
    no_hospitals = len(hospitals)
    
    hospital_tally = [[] for i in range(no_hospitals)]
    hospital_proportion = [[] for i in range(no_hospitals)]
    hospital_total = np.zeros(no_hospitals)
    haplotype_total = np.zeros(len(haplotypes))
    haplotype_str = []
    system_total_haplotypes = 0
    
    
    #print(haplotypes)
    
    for i in range(len(haplotypes)):
        haplotype_str.append(haplotypes[i].split(sep = ",")[0])
        
    #print(haplotype_str)
    
    
    for i in range (0, len(hospitals)):
        for j in range(0, len(haplotypes)):
            hospital_tally[i].append(0)
            hospital_proportion[i].append(0)
    
    for i in range (0, len(hospitals)):
        for j in range(0, len(hospitals[i])):
            for k in range(0, len(hospitals[i][j])):
                
                for l in range(0, len(haplotypes)):
                    if hospitals[i][j][k].split(sep = ",")[0] == haplotype_str[l]:
                        hospital_tally[i][l] += 1
                        haplotype_total[l] += 1 
                        hospital_total[i] += 1
                               
    for i in range (0, len(hospitals)):
        
        system_total_haplotypes += hospital_total[i]
        
        for j in range(0, len(haplotypes)):
            hospital_proportion[i][j] = hospital_tally[i][j]/hospital_total[i]
    
    return hospital_proportion, system_total_haplotypes, hospital_total, haplotype_total


ini_trees_per_hospital = [10, 5, 4, 20]
no_hospitals = len(ini_trees_per_hospital)

haplotypes = ['H1,0', 'H2,0', 'H3,0', 'H4, 0']
hospital_haplotype_distribution = [[0.3, 0.2, 0.4, 0.1],
                                   [0.2, 0.2, 0.6, 0],
                                   [0.5, 0.25, 0, 0.25],
                                   [0.05, 0.25, 0.2, 0.5]]

#ini_trees_per_hospital = [1, 1]
#no_hospitals = len(ini_trees_per_hospital)

#haplotypes = ['H1,0', 'H2,0']
#hospital_haplotype_distribution = [[1.0, 0],
 #                                  [0, 1.0]]

hospitals = hospital_setup(no_hospitals, ini_trees_per_hospital, haplotypes, hospital_haplotype_distribution)

#proportion_plot = [[] for i in range(no_hospitals * len(haplotypes) + 2)]
proportion_plot = [[] for i in range(2)]
proportion_plot.append([[] for i in range(len(haplotypes))])
proportion_plot.append([[[] for j in range(len(haplotypes) + 1)] for i in range(no_hospitals)])


t = 0
    
haplotype_proportion = haplotype_fraction(hospitals)
proportion_plot[0].append(t)
proportion_plot[1].append(haplotype_proportion[1])
    
for i in range(len(haplotypes)):
    proportion_plot[2][i].append(haplotype_proportion[3][i])
    

#count = 0
for i in range(no_hospitals):

    proportion_plot[3][i][0].append(haplotype_proportion[2][i])
    
    for j in range(len(haplotypes)):
        
        proportion_plot[3][i][j + 1].append(haplotype_proportion[0][i][j])
        #count += 1
            #proportion_plot[3].append(haplotype_proportion[0][1][0])





