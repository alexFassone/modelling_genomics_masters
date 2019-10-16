#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 30 15:29:24 2019

@author: alexfassone1
"""

import numpy as np
import random 

no_hospitals = 2
ini_samples_per_hospital = 2

hospitals = [[] for i in range(no_hospitals)]

random.seed(30) #create seed for random number generation 

#populate hospitals with pre-determined haplotypes 
for i in range (0, ini_samples_per_hospital):
    
    if i < ini_samples_per_hospital/2:
        hospitals[0].append('H1,0')
        hospitals[1].append('H2,0')
        
    else:
        hospitals[0].append('H2,0')
        hospitals[1].append('H3,0')  

        
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
    transfer_matrix = [[0, 0.3], 
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


def no_mutations_transfers(patient):
    no_transfers = patient.count('T')
    temp_patient = patient.split(sep = ",")
    
    haplotype = temp_patient[0]
    del temp_patient[0]
    
    temp_str = ""
    for i in range(0, len(temp_patient)):
        temp_str = temp_str + temp_patient[i]
        
    temp_patient = temp_str.split(sep = "T")
    
    total_mutations = 0
    for i in range(0, len(temp_patient)):
        total_mutations += int(temp_patient[i])
        
    return haplotype, total_mutations, no_transfers

t_max = 1000
t = 0
while t < t_max:
    samples_per_hospital = np.zeros(no_hospitals)
            
    for i in range(0, no_hospitals):
        samples_per_hospital[i] = len(hospitals[i])
    
    #print(samples_per_hospital)
            
    for i in range(0, no_hospitals):
        j = 0
        while j < int(samples_per_hospital[i]):
            mutation = check_mutation(0.1)
            #print("mutation: " + str(mutation))
            
            transfer = check_transfer(i)
            #print("transfer: " + str(transfer))
            
            #make sure that patients can only gain mutations & transfer once per day
            if ("DAY" in hospitals[i][j]) == True:
                day_check = hospitals[i][j].split(sep = "DAY")
                
                if day_check[1] == t:
                    mutation = False
                    transfer = [False, -1]
               
                hospitals[i][j] = day_check[0]
            
            #if a mutation has occurred update the patient label 
            if mutation == True:
                #print(str(i)+ " " + str(j))
                print(hospitals[i][j])
                        
                patient = hospitals[i][j].split(sep = ",")
                current_mutations = int(patient[len(patient)-1])
                current_mutations += 1
                #print(current_mutations)
                
                new_patient = ""
                
                for k in range(0, len(patient)-1):
                    new_patient = new_patient + patient[k] + ","
                
                new_patient = new_patient + str(current_mutations)
                hospitals[i][j] = new_patient
                print(hospitals[i][j])
                
            #if a transfer has occurred update the patient label
            if transfer[0] == True:
                temp = hospitals[i][j] + "T,0DAY" + str(t)
                
                del hospitals[i][j]
                
                hospitals[transfer[1]].append(temp)
                
                j += -1
                
                #re-calibrate the number of patients in each hospital 
                for k in range(0, no_hospitals):
                    samples_per_hospital[k] = len(hospitals[k])
                    
                #remove transfer tag if on last day of simuation
                if t == t_max - 1:
                    day_check = hospitals[transfer[1]][len(hospitals[transfer[1]]) - 1].split(sep = "DAY")
                    hospitals[transfer[1]][len(hospitals[transfer[1]]) - 1] = day_check[0]
            
            j += 1
    t += 1    




# =============================================================================
# def simulation(no_hospitals, hospitals, mutation_limit, no_days):
#     
#     time = 0
#     
#     while time < no_days:
#         
#         samples_per_hospital = np.zeros(no_hospitals)
#         
#         for i in range(0, no_hospitals):
#             samples_per_hospital[i] = len(hospitals[i])
#         
#         for i in range(0, no_hospitals):
#             for j in range(0, samples_per_hospital[i]):
#                 mutation = check_mutation(mutation_limit)
#                 
#                 print(mutation)
#                 
#                 if mutation == True:
#                     print(hospitals[i][j])
#                     
#                     patient = hospitals[i][j].split(sep = ",")
# =============================================================================
                    
                    
                    

#simulation(0.1, 30)       