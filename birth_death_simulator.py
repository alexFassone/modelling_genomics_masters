#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 13:24:21 2019

@author: alexfassone1
"""

import numpy as np
import random 
import matplotlib.pyplot as plt

ini_trees_per_hospital = [1]
no_hospitals = len(ini_trees_per_hospital)

haplotypes = ['H1,0', 'H2,0']
hospital_haplotype_distribution = [[1.0, 0]]


def hospital_setup(no_hospitals, ini_trees_per_hospital, haplotypes, hospital_haplotype_distribution):
    
    hospitals = [[] for i in range(no_hospitals)]
    
    for i in range(no_hospitals):
        for j in range(len(haplotypes)):
            for k in range(int(ini_trees_per_hospital[i] * hospital_haplotype_distribution[i][j])):
                hospitals[i].append([haplotypes[j]])
                
    return hospitals

random.seed(756) #create seed for random number generation 

#populate hospitals with pre-determined haplotypes 
hospitals = hospital_setup(no_hospitals, ini_trees_per_hospital, haplotypes, hospital_haplotype_distribution)
#print(hospitals)


def check_mutation(mutation_limit):
    limit_check = random.random()
    #print(limit_check)
    
    if limit_check < mutation_limit:
        mutation = True
        
    else:
        mutation = False
    
    return mutation 


def check_removal(removal_limit):
    limit_check = random.random()
    #print(limit_check)
    
    if limit_check < removal_limit:
        removal = True
        
    else:
        removal = False
    
    return removal 


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
            if hospital_total[i] != 0:
                hospital_proportion[i][j] = hospital_tally[i][j]/hospital_total[i]
            else:
                hospital_proportion[i][j] = 0.0
    
    return hospital_proportion, system_total_haplotypes, hospital_total, haplotype_total


def birth_death_probability(n_max, t_max, mutation_rate, removal_rate):
    mutation_time = mutation_rate
    removal_time = removal_rate
    
    r = mutation_time - removal_time
    epsilon = removal_time/mutation_time
    
    alpha = epsilon*(np.exp(r*t_max) - 1)/(np.exp(r*t_max) - epsilon)
    beta = (np.exp(r*t_max) - 1)/(np.exp(r*t_max) - epsilon)
    
    prob_str = [[],[]]
    prob_str[0].append(0)
    prob_str[1].append(alpha)
    
    for n in range(1, n_max + 1):
        prob_str[0].append(n)
        prob_str[1].append((1-alpha)*(1 - beta)*beta**(n - 1))
        
    return prob_str


def birth_death_probability_2(n_max, t_max, mutation_rate, removal_rate, a):
    mu = removal_rate
    lamda = mutation_rate
    
    alpha = (mu*(np.exp((lamda - mu)*t_max) - 1))/(lamda*np.exp((lamda - mu)*t_max) - mu)
    beta = (lamda/mu)*alpha
    
    prob_str = [[],[]]
    
    if a == 1 and lamda == mu:
        prob_str[0].append(0)
        prob_str[1].append((lamda*t_max)/(1 + lamda*t_max))
        
        for n in range(1, n_max + 1):
            prob_str[0].append(n)
            prob_str[1].append((lamda*t_max)**(n - 1)/(1 + lamda*t_max)**(n + 1))

    if a == 1 and lamda != mu:
        prob_str[0].append(0)
        prob_str[1].append(alpha)
        
        for n in range(1, n_max + 1):
            prob_str[0].append(n)
            prob_str[1].append((1-alpha)*(1 - beta)*beta**(n - 1))
            
    if a > 1 and lamda == mu:
        prob_str[0].append(0)
        prob_str[1].append(((lamda*t_max)/(1 + lamda*t_max))**a)
        
        for n in range(1, n_max + 1):
            temp = 0
            
            for j in range(1, min(a, n) + 1):
                temp += (a*(n - 1) + j*(j - 1)) * (lamda*t_max)**(-2*j)

            temp = temp * ((lamda*t_max)/(1 + lamda*t_max))**(a+n)
            
            prob_str[0].append(n)
            prob_str[1].append(temp)
        
    return prob_str


def simulation(hospitals, t_max, mutation_rate, removal_rate, symmetric_transfer_rate, transfer_rate):
    proportion_plot = [[] for i in range(2)]
    proportion_plot.append([[] for i in range(len(haplotypes))])
    proportion_plot.append([[[] for j in range(len(haplotypes) + 1)] for i in range(no_hospitals)])

    t = 0
    
    haplotype_proportion = haplotype_fraction(hospitals)
    proportion_plot[0].append(t)
    proportion_plot[1].append(haplotype_proportion[1])
        
    for i in range(len(haplotypes)):
        proportion_plot[2][i].append(haplotype_proportion[3][i])
        
    for i in range(no_hospitals):
        proportion_plot[3][i][0].append(haplotype_proportion[2][i])
        
        for j in range(len(haplotypes)):
            proportion_plot[3][i][j + 1].append(haplotype_proportion[0][i][j])
   
        
    while t < t_max:
        
        trees_per_hospital = np.zeros(no_hospitals)
                
        for i in range(0, no_hospitals):
            trees_per_hospital[i] = len(hospitals[i])
        
                
        for i in range(0, no_hospitals):
            for j in range(0, int(trees_per_hospital[i])):
                
                count = 0
                k = 0
                haplotypes_per_tree = len(hospitals[i][j])
                
                while count < haplotypes_per_tree:
                    
                    #print(t, i, j, k)
                    
                    mutation = check_mutation(mutation_rate)
                    #print("mutation: " + str(mutation))
                    
                    removal = check_removal(removal_rate)
                    #print("removal: " + str(removal))
                    
                    transfer = check_transfer(no_hospitals, i, symmetric_transfer_rate, transfer_rate)
                    #print("transfer: " + str(transfer))
                    
                    #if a mutation has occurred update the patient label 
                    if mutation == True:
                        patient = hospitals[i][j][k].split(sep = ",")
                        current_mutations = int(patient[len(patient)-1])
                        current_mutations += 1
                        
                        new_patient = ""
                        
                        for l in range(0, len(patient)-1):
                            new_patient = new_patient + patient[l] + ","
                        
                        new_patient = new_patient + str(current_mutations)
                        
                        hospitals[i][j].append(new_patient)
        
                    
                    if removal == True:
                        del hospitals[i][j][k]
                        
                        k += -1
                        
                    
                    #if a transfer has occurred update the patient label
                    if transfer[0] == True:
                        hospitals[transfer[1]].append([hospitals[i][j][k]])
                        
                    k += 1
                    count += 1
        t += 1   
        
        haplotype_proportion = haplotype_fraction(hospitals)
        proportion_plot[0].append(t)
        proportion_plot[1].append(haplotype_proportion[1])
            
        for i in range(len(haplotypes)):
            proportion_plot[2][i].append(haplotype_proportion[3][i])
            
            
        for i in range(no_hospitals):
            proportion_plot[3][i][0].append(haplotype_proportion[2][i])
            
            for j in range(len(haplotypes)):
                proportion_plot[3][i][j + 1].append(haplotype_proportion[0][i][j])
     
    return proportion_plot


no_tests = 10000

hist_str = [[] for i in range(2)]
t_max = 15
mutation_rate = 0.1
removal_rate = 0.1

for i in range(no_tests): 
    print("test: " + str(i))
    
    ini_trees_per_hospital = [100]
    no_hospitals = len(ini_trees_per_hospital)
    
    haplotypes = ['H1,0', 'H2,0']
    hospital_haplotype_distribution = [[1.0, 0]]
    
    #populate hospitals with pre-determined haplotypes 
    hospitals = hospital_setup(no_hospitals, ini_trees_per_hospital, haplotypes, hospital_haplotype_distribution)
    
    temp = simulation(hospitals, t_max, mutation_rate, removal_rate, True, 0.0)
    
    hist_str[0].append(i)
    hist_str[1].append(temp[3][0][0][t_max])

max_n = int(max(hist_str[1]))

prob_dist = birth_death_probability_2(max_n, t_max, mutation_rate, removal_rate, 100)


ax1 = plt.subplot()

ax1.set_xlabel('Remaining Haplotypes at time: ' + str(t_max))
ax1.set_ylabel('Probability')

ax1.plot(prob_dist[0],prob_dist[1], "ro", label = "Probability Distribution")
ax1.plot(prob_dist[0],prob_dist[1], "k")
ax1.hist(hist_str[1], density = True, bins = max_n, label = "Simulated Histogram")

ax1.legend(loc = "upper center", bbox_to_anchor=(0.5, 1.14), ncol = 5)
ax1.tick_params(axis='y')

plt.show()