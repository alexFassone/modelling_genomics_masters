#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 12:37:38 2019

@author: alexfassone1
"""


no_hospitals = 2
ini_trees_per_hospital = [2, 2, 10, 4]

haplotypes = ['H1,0', 'H2,0', 'H3,0']
hospital_haplotype_distribution = [[0.5, 0.5, 0],
                                   [0, 0.5, 0.5],
                                   [0.3, 0.4, 0],
                                   [0.5, 0, 0.5]]

hospitals = [[] for i in range(no_hospitals)]


for i in range(no_hospitals):
    for j in range(len(haplotypes)):
        for k in range(int(ini_trees_per_hospital[i] * hospital_haplotype_distribution[i][j])):
            #print(int(ini_trees_per_hospital * hospital_haplotype_distribution[i][j]))
            hospitals[i].append([haplotypes[j]])
 
           


def hospital_setup(no_hospitals, ini_trees_per_hospital, haplotypes, hospital_haplotype_distribution):
    
    hospitals = [[] for i in range(no_hospitals)]
    
    for i in range(no_hospitals):
        for j in range(len(haplotypes)):
            for k in range(int(ini_trees_per_hospital[i] * hospital_haplotype_distribution[i][j])):
                hospitals[i].append([haplotypes[j]])
                
    return hospitals

test_hosp = hospital_setup(4, ini_trees_per_hospital, haplotypes, hospital_haplotype_distribution)