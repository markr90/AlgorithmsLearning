# -*- coding: utf-8 -*-
"""
Created on Sat Jul 27 12:55:28 2019

My implementation of quicksort

@author: Mark
"""

import random

def QuickSort(A):
    low = 0
    high = len(A)
    
    QuickSortAlgo(A, low, high)


def QuickSortAlgo(A, low, high):
    
    if low == high:
        return
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
        
        QuickSortAlgo(A, low, split - 1)
        QuickSortAlgo(A, split, high)
        
        
if __name__ == "__main__":
    A = [1, 3, 8, 2, 5, 1, 1, 1, 1, 1, 4, 9, 7, 0, 6]
    QuickSort(A)