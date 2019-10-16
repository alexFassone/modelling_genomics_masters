#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 14:14:04 2019

@author: alexfassone1
"""
import random

hospitals = [['H1,99', 'H2,23', 'H2,32'], ['H3,46T', 'H2,86T,17IH2,0', 'H1,67', 'H2,1IH1,0T,0T,0']]

def check_infect(current_position, hospital_patients):
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
    print(current_haplotype)
    
    limit_check = random.random()
    print(limit_check)
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
                    print(infected_haplotype)
                    
                    if virulence_matrix[current_haplotype][infected_haplotype] == 1:
                        infect = True
                        
                    else:
                        infect = False
        else:
            infect = False
    else: 
        infect = False
    
    return infect, infected_patient_position

test = check_infect(1, hospitals[0])


def check_infect2(current_position, current_patient, no_hospital_patients):
    current_patient = current_patient.split(sep = ",")
    current_haplotype = int(current_patient[0].split(sep = "H")[1])

    haplotype_infectivity = [0, 0.9, 0.1, 0.1]
    
    #limit_check = random.random()
    #print(limit_check)
    limit_check = 0.05
    
    infected_patient = -1
    
    if no_hospital_patients > 1:
        if limit_check < haplotype_infectivity[current_haplotype]:
            infect = True 
            
            self_infect = True
            while self_infect == True:
                infected_patient = random.randint(0, no_hospital_patients - 1)
                
                if infected_patient != current_position:
                    self_infect = False
        else:
            infect = False
    else: 
        infect = False
    
    
    return infect, infected_patient

#test = check_infect2(0, hospitals[0][0], len(hospitals[0]))
print(test)


def check_infection(current_position, hospital_patients):
    current_patient = hospital_patients[current_position].split(sep = ",")
    current_haplotype = int(current_patient[0].split(sep = "H")[1])

    haplotype_infectivity = [0, 0.1, 0.1, 0.1]
    
    limit_check = random.random()
    #print(limit_check)
    #limit_check = 0.05
    
    infected_patient = -1
    
    if len(hospital_patients) > 1:
        if limit_check < haplotype_infectivity[current_haplotype]:
            infect = True 
            
            self_infect = True
            while self_infect == True:
                infected_patient = random.randint(0, len(hospital_patients) - 1)
                
                if infected_patient != current_position:
                    self_infect = False
        else:
            infect = False
    else: 
        infect = False
    
    
    return infect, infected_patient

def check_transfer(current_hospital):
    
    #potentially make global to stop recalculations 
    transfer_matrix = [[0, 0.001], 
                      [0.0005, 0]]
    
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
