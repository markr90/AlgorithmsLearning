# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

def count_splitInv(A,B):
    i = j = 0
    nSplitInversions = 0
    while i < len(A) and j < len(B):
        if A[i] < B[j]:
            # no inversion
            i += 1
        else:
            nSplitInversions += len(A) - i
            j += 1
    
    return nSplitInversions
    


def countInv(A):
    n = len(A)
    if n <= 1:
        return 0
    else:
        B = A[:int(n/2)]
        C = A[int(n/2):]
        x = countInv(B)
        y = countInv(C)
        z = count_splitInv(sorted(B), sorted(C))
        return x + y + z