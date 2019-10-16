#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 12:08:12 2019

@author: alexfassone1
"""

import numpy as np
import random 
import pandas as pd
import matplotlib.pyplot as plt

#no_hospitals = 2
#ini_samples_per_hospital = 1

ini_trees_per_hospital = [1, 1]
no_hospitals = len(ini_trees_per_hospital)

haplotypes = ['H1,0', 'H2,0']
hospital_haplotype_distribution = [[1.0, 0],
                                   [0, 1.0]]


def hospital_setup(no_hospitals, ini_trees_per_hospital, haplotypes, hospital_haplotype_distribution):
    
    hospitals = [[] for i in range(no_hospitals)]
    
    for i in range(no_hospitals):
        for j in range(len(haplotypes)):
            for k in range(int(ini_trees_per_hospital[i] * hospital_haplotype_distribution[i][j])):
                hospitals[i].append([haplotypes[j]])
                
    return hospitals

#hospitals = [[] for i in range(no_hospitals)]


mutation_log = pd.DataFrame(columns = ('Day', 'Original Hap', 'New Hap'))
infection_log = pd.DataFrame(columns = ('Day', 'Patient', 'Infected Patient', 'New Infected Hap'))
transfer_log = pd.DataFrame(columns = ('Day', 'Patient', 'Transfer From', 'Transfer To'))


random.seed(3897) #create seed for random number generation 

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


def check_transfer(current_hospital):
    
    #potentially make global to stop recalculations 
    transfer_matrix = [[0, 0.1], 
                      [0.1, 0]]
    
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
                print("Transfer to hospital " + str(count))
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
    haplotypes = []
    total_haplotypes = 0
    
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
        
        total_haplotypes += hospital_total[i]
        
        for j in range(0, len(haplotypes)):
            hospital_proportion[i][j] = hospital_tally[i][j]/hospital_total[i]
    
    return haplotypes, hospital_proportion, total_haplotypes


def simulation():
    proportion_plot = [[] for i in range(no_hospitals + 2)]
    
    t_max = 15
    t = 0
    
    haplotype_proportion = haplotype_fraction(hospitals)
    proportion_plot[0].append(t)
    proportion_plot[1].append(haplotype_proportion[1][0][0])
    proportion_plot[2].append(haplotype_proportion[1][1][0])
    proportion_plot[3].append(haplotype_proportion[2])
        
    while t < t_max:
        
        print(hospitals)
        
        trees_per_hospital = np.zeros(no_hospitals)
                
        for i in range(0, no_hospitals):
            trees_per_hospital[i] = len(hospitals[i])
        
                
        for i in range(0, no_hospitals):
            for j in range(0, int(trees_per_hospital[i])):
                
                haplotypes_per_tree = len(hospitals[i][j])
                
                for k in range(0, haplotypes_per_tree):
                    
                    print(t, i, j, k)
                    
                    mutation = check_mutation(0.1)
                    #print("mutation: " + str(mutation))
                    
                    transfer = check_transfer(i)
                    #print("transfer: " + str(transfer))
                    
                    #if a mutation has occurred update the patient label 
                    if mutation == True:
                        #print(str(i)+ " " + str(j))
                        #print(hospitals[i][j][k])
                                
                        patient = hospitals[i][j][k].split(sep = ",")
                        current_mutations = int(patient[len(patient)-1])
                        current_mutations += 1
                        #print(current_mutations)
                        
                        new_patient = ""
                        
                        for l in range(0, len(patient)-1):
                            new_patient = new_patient + patient[l] + ","
                        
                        new_patient = new_patient + str(current_mutations)
                        
                        hospitals[i][j].append(new_patient)
                        #print(hospitals[i][j])
                        
                    
                    #if a transfer has occurred update the patient label
                    if transfer[0] == True:
                        hospitals[transfer[1]].append([hospitals[i][j][k]])
        
        t += 1                 
        
        haplotype_proportion = haplotype_fraction(hospitals)
        proportion_plot[0].append(t)
        proportion_plot[1].append(haplotype_proportion[1][0][0])
        proportion_plot[2].append(haplotype_proportion[1][1][0])
        proportion_plot[3].append(haplotype_proportion[2])
        
           
     
        
    fig, ax1 = plt.subplots()

    #color = 'tab:red'
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Haplotype Proportion')
    ax1.plot(proportion_plot[0],proportion_plot[1])
    ax1.plot(proportion_plot[0],proportion_plot[2])
    ax1.tick_params(axis='y')
    
    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    
    #color = 'tab:blue'
    ax2.set_ylabel('Total Haplotypes')  # we already handled the x-label with ax1
    ax2.plot(proportion_plot[0],proportion_plot[3], color = "black")
    ax2.tick_params(axis='y')
    
    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.show()

simulation()