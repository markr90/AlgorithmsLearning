# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from random import randint
import time

n = 1000

def minIndex(numbers, i, j):
    """ find minimum of list of numbers in range(i, j) """
    # return i if end of list gets reached
    if i == j - 1:
        return i
    # find minimum of remaining i+1 : j elements
    k = minIndex(numbers, i+1, j)   
    # return index of current if it's smaller than remaining numbers
    return (i if numbers[i] < numbers[k] else k)

def selection_sort(unsorted):
    numbers = unsorted[:]
    for i in range(len(numbers)):
        minI = i
        for j in range(i, len(numbers)):
            if numbers[j] < numbers[minI]:
                minI = j
        # Swap the found numbers
        numbers[i], numbers[minI] = numbers[minI], numbers[i]
    return numbers

def rec_selection_sort(unsorted, index = 0):
    nMax = len(unsorted) 
    numbers = unsorted[:]
    
    # Return the sorted list when index reaches end)
    if index == nMax - 1:
        return numbers 
    
    # find index of minimum number between index and end of list
    k = minIndex(numbers, index, nMax)
    
    # swap if minimum index is not equal to current index
    if k != index:
        numbers[k], numbers[index] = numbers[index], numbers[k]
    
    # recursively sort the remaining elements index + 1 : ....
    return rec_selection_sort(numbers, index + 1)

def insertion_sort(unsorted):
    numbers = unsorted[:]
    for i in range(1, len(numbers)):
        if numbers[i] >= numbers[i-1]:
            continue
        for j in range(i):
            if numbers[i] < numbers[j]:
                numbers[j], numbers[j+1:i+1] = numbers[i], numbers[j:i]
                break
    return numbers

def bubble_sort(unsorted):
    numbers = unsorted[:]
    nMax = len(numbers)
    for i in range(nMax):
        for j in range(0, nMax-i-1):
            if numbers[j] > numbers[j+1]:
                numbers[j], numbers[j+1] = numbers[j+1], numbers[j]
                
def merge_sort(unsorted):
    out = []
    if len(unsorted) == 1:
        return unsorted
    if len(unsorted) == 0:
        return []
    else:
        splitPoint = len(unsorted)//2
        A = unsorted[:splitPoint]
        B = unsorted[splitPoint:]
        A = merge_sort(A)
        B = merge_sort(B)
        
        
        i = j = 0
        
        while i < len(A) and j < len(B):
            if A[i] < B[j]:
                out.append(A[i])
                i += 1
            else:
                out.append(B[j])
                j += 1
        
        while i < len(A):
            out.append(A[i])
            i += 1
        while j < len(B):
            out.append(B[j])
            j += 1
            
        return out
                
        
A = []
for i in range(n):
    A.append(randint(0,n))        
        
start = time.time()
selection_sort(A)
end = time.time()
print("Selection sort algorithm completed in:", end - start)

start = time.time()
rec_selection_sort(A, index = 0)
end = time.time()
print("Recursive Selection sort algorithm completed in:", end - start)

start = time.time()
insertion_sort(A)
end = time.time()
print("Insertion sort algorithm completed in:", end - start)

start = time.time()
bubble_sort(A)
end = time.time()
print("Bubble sort algorithm completed in:", end - start)

start = time.time()
test = merge_sort(A)
end = time.time()
print("Merge sort algorithm completed in:", end - start)
            
                  
            