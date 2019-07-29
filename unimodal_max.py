# -*- coding: utf-8 -*-
"""
Created on Fri Jul 26 19:13:32 2019

Two different algorithms for finding the max of a unimodal array
An array is unimodal when it is strictly increasing for all i < iMax
and strictly decreasing for all i > iMax

The first algorithm in this file is many times faster than the second one due
the list being copied over everytime in function calls
This adds extra time complexity that can be avoided by defining the algorithm
through indices i and j that determine the region the recursive call is 
working on.


Functions are both called recursively through a bimodal search in O(nlogn) 
runtime.

@author: Mark
"""

import time
import matplotlib.pyplot as plt

def unimodal_max(A):
    n = len(A)
    
    def unimodal_max_algo(A, i, j):
    
        if i == j:
            return A[i]
        elif i + 1 == j and A[i] >= A[j]:
            return A[i]
        elif i + 1 == j and A[i] < A[j]:
            return A[j]
        else:
            midpoint = (i + j) // 2
            
            if A[midpoint - 1] <= A[midpoint]:
                return unimodal_max_algo(A, midpoint, j)
            else:
                return unimodal_max_algo(A, i, midpoint - 1)
    
    return unimodal_max_algo(A, 0, n-1)


        
        
def unimodal_max_2(A):
    # This function has a lot of overhead due to having to copy the list all the time
    # The unimodal_max_algo has much lower runtime!!
    n = len(A)
    
    if n == 1:
        return A[0]
    else:
        midpoint = n//2
        
        if A[midpoint - 1] < A[midpoint]:
            return unimodal_max_2(A[midpoint:])
        else:
            return unimodal_max_2(A[:midpoint])
        
    
if __name__ == "__main__":
    
    nMax = 1000000
    nSteps = 100
    
    nList = list(range(nMax // nSteps, nMax, nMax // nSteps))
    
    algo1 = []
    algo2 = []
    
    for n in nList:
        left = list(range(n // 2))
        right = list(range(n // 2, 0, -1))
        A = left + right
        
        start = time.time()
        unimodal_max(A)
        runtime = time.time() - start
        algo1.append(runtime)
        
        start = time.time()
        unimodal_max_2(A)
        runtime = time.time() - start
        algo2.append(runtime)
    
    
    plt.plot(nList, algo1, 'r')
    plt.plot(nList, algo2, 'g')
    plt.show()
        
        
        
        