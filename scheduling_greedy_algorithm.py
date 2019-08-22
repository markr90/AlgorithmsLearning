# -*- coding: utf-8 -*-
"""
Created on Thu Aug 22 09:53:49 2019

@author: mraaijmakers
"""

import numpy as np

nJobs = 10

np.random.seed(42)

L = np.random.randint(1,10, size = 10)
w = np.random.randint(1,10, size = 10)

# Creates list of jobs with their job index, length, weight, and score = weight / length

jobs = [(i + 1, L[i], w[i], w[i] / L[i]) for i in range(len(L))]

def calc_weightedCT(J):
    # Sort based on score
    J.sort(key = lambda tup: tup[3])
    # calculate completion time
    ct = 0
    for j in J:
        ct += j[1] * j[2]
        
    # show sorted job list
    print([j[0] for j in J])
        
    return ct
    