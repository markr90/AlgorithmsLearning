# -*- coding: utf-8 -*-
"""
Created on Sat Jul 27 12:55:28 2019

Finds the ith smallest element of an array with 0th smallest element
corresponding to the minimum. A modified quicksort algorithm

@author: Mark
"""

import random

def RSelect(A, st):
    low = 0
    high = len(A)
    
    return Find_Statistic_Algo(A, st, low, high)

def Find_Median(A):
    n = len(A)
    middle = n // 2
    if n % 2 == 0:
        median1 = RSelect(A, middle - 1)
        median2 = RSelect(A, middle)
        return (median1 + median2) / 2
    else:
        return RSelect(A, middle)


def Find_Statistic_Algo(A, st, low, high):
    
    if low == high:
        return A[low]
    else:
        pivotPoint = random.randint(low, high - 1)        
        pivot = A[pivotPoint]        
        A[low], A[pivotPoint] = A[pivotPoint], A[low]
        
        split = low + 1
        
        for i in range(low + 1, high):
            if A[i] <= pivot:
                A[split], A[i] = A[i], A[split]
                split += 1
            else:
                # do nothing
                continue
        A[low], A[split - 1] = A[split - 1], A[low]
        
        if split - 1 == st:
            return A[split-1]
        elif st < split - 1:
            return Find_Statistic_Algo(A, st, low, split - 1)
        elif st > split - 1:
            return Find_Statistic_Algo(A, st, split, high)
        
        
if __name__ == "__main__":
    A = [1,9,2,7,3,4,8,6,5,0]
    print(RSelect(A, 0))
    print(Find_Median(A))