#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  4 11:01:29 2019

@author: alexfassone1
"""

import numpy as np
import random 
import pandas as pd

no_hospitals = 2
ini_samples_per_hospital = 1

hospitals = [[] for i in range(no_hospitals)]

#mutation_log = ["Day", ""]
#infection_log = []
#transfer_log = []

mutation_log = pd.DataFrame(columns = ('Day', 'Original Hap', 'New Hap'))
#print(mutation_log)
infection_log = pd.DataFrame(columns = ('Day', 'Patient', 'Infected Patient', 'New Infected Hap'))
transfer_log = pd.DataFrame(columns = ('Day', 'Patient', 'Transfer From', 'Transfer To'))


random.seed(836) #create seed for random number generation 

#populate hospitals with pre-determined haplotypes 
hospitals[0].append(['H1,0'])
hospitals[1].append(['H2,0'])

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
    transfer_matrix = [[0, 0.001], 
                      [0.001, 0]]
    
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
    
    return haplotypes, hospital_proportion 


t_max = 500
t = 0
while t < t_max:
    
    trees_per_hospital = np.zeros(no_hospitals)
            
    for i in range(0, no_hospitals):
        trees_per_hospital[i] = len(hospitals[i])
    
            
    for i in range(0, no_hospitals):
        for j in range(0, int(trees_per_hospital[i])):
            
            haplotypes_per_tree = len(hospitals[i][j])
            
            for k in range(0, haplotypes_per_tree):
                
                print(t, i, j, k)
                
                mutation = check_mutation(0.01)
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
    
#print(hospitals)
#print(mutation_log)
#print(infection_log)
#print(transfer_log)