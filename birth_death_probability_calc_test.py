#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 11:17:05 2019

@author: alexfassone1
"""

import numpy as np
import random 
import matplotlib.pyplot as plt




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
    
    #alpha = (mu*(np.exp((lamda - mu)*t_max) - 1))/(lamda*np.exp((lamda - mu)*t_max) - mu)
    #beta = (lamda/mu)*alpha
    
    alpha = (mu*(np.exp((lamda-mu)*t_max) - 1))/(lamda*(np.exp((lamda-mu)*t_max) - mu))
    beta = (lamda*(np.exp((lamda-mu)*t_max) - 1))/(lamda*np.exp((lamda-mu)*t_max) - mu)
    
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
            
            for j in range(1, min(a,n) + 1):
                temp += (a*(n - 1) + j*(j - 1)) * (lamda*t_max)**(-2*j)
                
            print("before: " + str(temp))

            temp = temp * ((lamda*t_max)/(1 + lamda*t_max))**(a+n)
            
            print("after: " + str(temp))
            
            prob_str[0].append(n)
            prob_str[1].append(temp)
            
    if a > 1 and lamda != mu:
        prob_str[0].append(0)
        prob_str[1].append(alpha**a)
        
        for n in range(1, n_max + 1):
            temp = 0
            
            for j in range(0, min(a,n) + 1):
                temp += (a*(a+n-j-1) + j*(a-1)) * alpha**(a-j) * beta**(n-j) * (1-alpha-beta)**j
            
            print("after: " + str(temp))
            
            prob_str[0].append(n)
            prob_str[1].append(temp)
        
        
    return prob_str

def birth_death_probability_3(n_max, t_max, mutation_rate, removal_rate, a):
    mu = removal_rate
    lamda = mutation_rate
    
    #alpha = (mu*(np.exp((lamda - mu)*t_max) - 1))/(lamda*np.exp((lamda - mu)*t_max) - mu)
    #beta = (lamda/mu)*alpha
    
    alpha = (mu*(np.exp((lamda-mu)*t_max) - 1))/(lamda*(np.exp((lamda-mu)*t_max) - mu))
    beta = (lamda*(np.exp((lamda-mu)*t_max) - 1))/(lamda*np.exp((lamda-mu)*t_max) - mu)
    
    print(alpha)
    print(beta)
    
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
            
    if a > 1:
        prob_str[0].append(0)
        prob_str[1].append(alpha**a)
        
        for n in range(1, n_max + 1):
            temp = 0
            
            for j in range(0, min(a,n) + 1):
                temp += (a*(a+n-j-1) + j*(a-1)) * alpha**(a-j) * beta**(n-j) * (1-alpha-beta)**j
            
            #print("after: " + str(temp))
            
            prob_str[0].append(n)
            prob_str[1].append(temp)
        
        
    return prob_str

t_max = 9
mutation_rate = 0.2
removal_rate = 0.6

#test = birth_death_probability_2(100, t_max, 0.20, 0.1, 1)
test_2 = birth_death_probability_3(200, t_max, 0.1, 0.1, 100)

#print(sum(test[1]))
print(sum(test_2[1]))

#plt.plot(test[0], test[1])
plt.plot(test_2[0], test_2[1])
plt.show