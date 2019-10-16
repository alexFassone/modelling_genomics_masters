#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 15:51:23 2019

@author: alexfassone1
"""

import numpy as np
import random 
#import pandas as pd
import matplotlib.pyplot as plt

#no_hospitals = 2
#ini_samples_per_hospital = 1

ini_trees_per_hospital = [100, 100, 100, 100]
no_hospitals = len(ini_trees_per_hospital)

haplotypes = ['H1,0', 'H2,0', 'H3,0', 'H4, 0']
hospital_haplotype_distribution = [[0.3, 0.2, 0.4, 0.1],
                                   [0.2, 0.2, 0.6, 0],
                                   [0.5, 0.25, 0, 0.25],
                                   [0.05, 0.25, 0.2, 0.5]]

ini_trees_per_hospital = [1, 1]
no_hospitals = len(ini_trees_per_hospital)

haplotypes = ['0|0H1,0', '0|0H2,0']

hospital_haplotype_distribution = [[1.0, 0],
                                   [0, 1.0]]


def hospital_setup(no_hospitals, ini_trees_per_hospital, haplotypes, hospital_haplotype_distribution):
    
    hospitals = [[] for i in range(no_hospitals)]
    
    for i in range(no_hospitals):
        for j in range(len(haplotypes)):
            for k in range(int(ini_trees_per_hospital[i] * hospital_haplotype_distribution[i][j])):
                hospitals[i].append([haplotypes[j]])
                
    return hospitals

random.seed(423874) #create seed for random number generation 

#populate hospitals with pre-determined haplotypes 
hospitals = hospital_setup(no_hospitals, ini_trees_per_hospital, haplotypes, hospital_haplotype_distribution)
#hospitals[0].append(['H1,0'])
#hospitals[1].append(['H2,0'])

print(hospitals)


def check_mutation(mutation_limit):
    limit_check = random.random()
    #print(limit_check)
    
    if limit_check < mutation_limit:
        mutation = True
        
    else:
        mutation = False
    
    return mutation 


def check_transfer(no_hospitals, current_hospital, symmetric_rate, rate_value):
    
    #potentially make global to stop recalculations
    
    if symmetric_rate == True:
        
        ident = np.identity(no_hospitals)
        transfer_matrix = [[] for i in range(no_hospitals)]
        
        for i in range(no_hospitals):
            for j in range(no_hospitals):
                
                if ident[i][j] == 0:
                    transfer_matrix[i].append(rate_value)
                else:
                    transfer_matrix[i].append(0)
    else:
        transfer_matrix = [[0, 0.1], 
                           [0.1, 0]]
    
    #print(transfer_matrix)
    
    transfer_probability = 0
    for i in range(0, len(transfer_matrix[current_hospital])):
        transfer_probability += transfer_matrix[current_hospital][i]

    #print(transfer_probability)
    
    limit_check = random.random()
    transfer_hospital = -1
    
    if limit_check < transfer_probability:
        transfer = True
        
        transfer_check = False
        count = 0
        position_sum = 0
        
        while transfer_check == False:
            position_sum += transfer_matrix[current_hospital][count]
    
            if limit_check <= position_sum:
                #print("Transfer to hospital " + str(count))
                transfer_hospital = count
                transfer_check = True
    
            count += 1
       
    else:
        transfer = False
     
    return transfer, transfer_hospital 


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


def simulation(hospitals, t_max, mutation_rate, symmetric_transfer_rate, transfer_rate):
    #proportion_plot = [[] for i in range(2)]
    #proportion_plot.append([[] for i in range(len(haplotypes))])
    #proportion_plot.append([[[] for j in range(len(haplotypes) + 1)] for i in range(no_hospitals)])


    t = 0
    print(hospitals)
    
    #haplotype_proportion = haplotype_fraction(hospitals)
    #proportion_plot[0].append(t)
   ## proportion_plot[1].append(haplotype_proportion[1])
        
    #for i in range(len(haplotypes)):
    #    proportion_plot[2][i].append(haplotype_proportion[3][i])
        
    #for i in range(no_hospitals):
    #    proportion_plot[3][i][0].append(haplotype_proportion[2][i])
        
     #   for j in range(len(haplotypes)):
      #      proportion_plot[3][i][j + 1].append(haplotype_proportion[0][i][j])
   
        
    while t < t_max:
        
        #print(hospitals)
        
        trees_per_hospital = np.zeros(no_hospitals)
                
        for i in range(0, no_hospitals):
            trees_per_hospital[i] = len(hospitals[i])
        
                
        for i in range(0, no_hospitals):
            for j in range(0, int(trees_per_hospital[i])):
                
                haplotypes_per_tree = len(hospitals[i][j])
                
                for k in range(0, haplotypes_per_tree):
                    
                    #print(t, i, j, k)
                    
                    mutation = check_mutation(mutation_rate)
                    #print("mutation: " + str(mutation))
                    
                    transfer = check_transfer(no_hospitals, i, symmetric_transfer_rate, transfer_rate)
                    #print("transfer: " + str(transfer))
                    
                    #if a mutation has occurred update the patient label 
                    if mutation == True:
                        #print(str(i)+ " " + str(j))
                        #print(hospitals[i][j][k])
                        print(hospitals[i][j][k])
                        patient = hospitals[i][j][k].split(sep = ",")
                        print(patient)
                        current_mutations = int(patient[len(patient)-1])
                        current_mutations += 1
                        
                        print(patient[0])
                        
                        current_generation = int(patient[0].split(sep = "|")[0])
                        current_generation += 1
                        #print(current_mutations)
                        
                        patient[0] = str(current_generation) + "|" + str(current_generation) + "H" + patient[0].split(sep = "H")[1]
                        
                        #new_patient = str(current_generation)
                        new_patient = ""
                        
                        for l in range(0, len(patient)-1):
                            new_patient = new_patient + patient[l] + ","
                        
                        new_patient = new_patient + str(current_mutations)
                        
                        hospitals[i][j].append(new_patient)
                        
                        hospitals[i][j][k] = str(current_generation) + "|" + hospitals[i][j][k].split(sep = "|")[1]
                        #print(hospitals[i][j])
                        
                    
                    #if a transfer has occurred update the patient label
                    if transfer[0] == True:
                        temp = hospitals[i][j][k].split(sep = "H")[1]
                        temp = str(0) + "H" + temp
                
                        hospitals[transfer[1]].append([temp])
        
        t += 1                 
        
        #haplotype_proportion = haplotype_fraction(hospitals)
        #proportion_plot[0].append(t)
        #proportion_plot[1].append(haplotype_proportion[1])
            
        #for i in range(len(haplotypes)):
          #  proportion_plot[2][i].append(haplotype_proportion[3][i])
            
        #for i in range(no_hospitals):
          #  proportion_plot[3][i][0].append(haplotype_proportion[2][i])
            
           # for j in range(len(haplotypes)):
             #   proportion_plot[3][i][j + 1].append(haplotype_proportion[0][i][j])
     
    return hospitals


test = simulation(hospitals, 30, 0.1, True, 0.0)