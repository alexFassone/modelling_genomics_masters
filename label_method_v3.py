#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 12:32:13 2019

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


def no_mutations_transfers_current(patient):
    current_patient_label = patient.split(sep = "I")[-1]
    no_transfers = current_patient_label.count('T')
    temp_patient = current_patient_label.split(sep = ",")
    
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


def check_mutation(mutation_limit):
    limit_check = random.random()
    #print(limit_check)
    
    if limit_check < mutation_limit:
        mutation = True
        
    else:
        mutation = False
    
    return mutation 

def check_infection(current_position, hospital_patients):
    haplotype_infectivity = [0, 0.9, 0.1, 0.1]
    
    virulence_matrix = [[0, 0, 0, 0], 
                        [0, 0, 1, 0],
                        [0, 0, 0, 1],
                        [0, 1, 1, 0]]
    
    if ("I" in hospital_patients[current_position]) == True:
        current_patient = hospital_patients[current_position].split(sep = "I")[-1].split(sep = ",")
        
    else:
        current_patient = hospital_patients[current_position].split(sep = ",")
    
    current_haplotype = int(current_patient[0].split(sep = "H")[1])
    #print("currently H" + str(current_haplotype))
    
    limit_check = random.random()
    #print(limit_check)
    #limit_check = 0.05
    
    infected_patient_position = -1
    
    if len(hospital_patients) > 1:
        if limit_check < haplotype_infectivity[current_haplotype]:
            #infect = True 
            
            self_infect = True
            while self_infect == True:
                infected_patient_position = random.randint(0, len(hospital_patients) - 1)
                #infected_patient_position = 1
                
                if infected_patient_position != current_position:
                    self_infect = False
                    
                    
                    if ("I" in hospital_patients[infected_patient_position]) == True:
                        infected_patient = hospital_patients[infected_patient_position].split(sep = "I")[-1].split(sep = ",")
        
                    else:
                        infected_patient = hospital_patients[infected_patient_position].split(sep = ",")
        
                    infected_haplotype = int(infected_patient[0].split(sep = "H")[1])
                    #print("infected with H" + str(infected_haplotype))
                    
                    if virulence_matrix[current_haplotype][infected_haplotype] == 1:
                        infect = True
                        print("currently H" + str(current_haplotype))
                        print("infected an H" + str(infected_haplotype))
                        
                    else:
                        infect = False
        else:
            infect = False
    else: 
        infect = False
    
    return infect, infected_patient_position


def check_transfer(current_hospital):
    
    #potentially make global to stop recalculations 
    transfer_matrix = [[0, 0.1], 
                      [0.05, 0]]
    
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


t_max = 10
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
            
            #infection = check_infection(j, hospitals[i][j], len(hospitals[i]))
            infection = check_infection(j, hospitals[i])
            print("infection: " + str(infection))
            
            transfer = check_transfer(i)
            #print("transfer: " + str(transfer))
            
            #make sure that patients can only gain mutations & transfer once per day
            if ("DAY" in hospitals[i][j]) == True:
                day_check = hospitals[i][j].split(sep = "DAY")
                
                if day_check[1] == t:
                    mutation = False
                    transfer = [False, -1]
                    infect = [False, -1]
               
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
            
            
            #if an infection has occurred find the infected patient and update their patient label
            if infection[0] == True:
                current_patient_label = hospitals[i][j].split(sep = "I")
                #current_haplotype = int(current_patient[0].split(sep = "H")[1])
                
                infected_patient = hospitals[i][infection[1]]
                hospitals[i][infection[1]] = hospitals[i][infection[1]] + "I" + current_patient_label[-1]
                
            
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