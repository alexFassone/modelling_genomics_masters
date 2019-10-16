#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 11:44:00 2019

@author: alexfassone1
"""

hospitals = [['H2,1', 'H3,0T,0DAY1'], ['H2,2', 'H1,0T,0DAY0T,0DAY2T,0DAY4']]

if ('DAY' in hospitals[0][1]) == True:
    print("we're in")
    day_check = hospitals[0][1].split(sep = "DAY")
                
    if day_check[1] == 1:
        mutation = False
               
    hospitals[0][1] = day_check[0]

print(hospitals[0][1])