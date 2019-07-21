# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import random
import time
import matplotlib.pyplot as plt

def createZeroMatrix(n):
    mat = []
    for i in range(n):
        row = []
        for j in range(n):
            row.append(0)
        mat.append(row)
    return mat

def matrixAdd(X,Y):
    n = len(X)
    result = createZeroMatrix(n)
    
    for i in range(n):
        for j in range(n):
            result[i][j] = X[i][j] + Y[i][j]
    return result

def matrixSub(X,Y):
    n = len(X)
    result = createZeroMatrix(n)
    
    for i in range(n):
        for j in range(n):
            result[i][j] = X[i][j] - Y[i][j]
    return result

def splitMatr(X):
    n = len(X)
    
    X11 = [X[i][:n//2] for i in range(n//2)]
    X12 = [X[i][n//2:] for i in range(n//2)]
    X21 = [X[i][:n//2] for i in range(n//2, n)]
    X22 = [X[i][n//2:] for i in range(n//2, n)] 
    
    return (X11, X12, X21, X22)

def padZeros(X):
    n = len(X)
    next2n = 0
    i = 0
    while next2n < len(X):
        next2n = 2**i
        i += 1
        
    for i in range(n):
        for j in range(n, next2n):
            X[i].append(0)
    for i in range(n, next2n):
        row = []
        for j in range(next2n):
            row.append(0)
        X.append(row)
    return X

def combineMatr(X11, X12, X21, X22):
    n = len(X11)
    res = []
    
    for i in range(n):
        res.append(X11[i] + X12[i])
    for i in range(n):
        res.append(X21[i] + X22[i])
    return res

def col(X,j):
    n = len(X)
    return [X[i][j] for i in range(n)]




def dotProd(x,y):
    n = len(x)
    dp = 0
    for i in range(n):
        dp += x[i]*y[i]
    return dp

def strassenMult(X,Y):
    originalN = len(X)
    A = padZeros(X)
    B = padZeros(Y)
    
    if len(A) < 32:
#        ab = A[0][0] * B[0][0]
        return defaultMult(A,B)
    else:
        (A11, A12, A21, A22) = splitMatr(A)
        (B11, B12, B21, B22) = splitMatr(B)
        P1 = strassenMult(matrixAdd(A11, A22), matrixAdd(B11, B22))
        P2 = strassenMult(matrixAdd(A21, A22), B11)
        P3 = strassenMult(A11, matrixSub(B12, B22))
        P4 = strassenMult(A22, matrixSub(B21, B11))
        P5 = strassenMult(matrixAdd(A11, A12), B22)
        P6 = strassenMult(matrixSub(A21, A11), matrixAdd(B11, B12))
        P7 = strassenMult(matrixSub(A12, A22), matrixAdd(B21, B22))
        
        (C11, C12, C21, C22) = (matrixAdd(matrixSub(matrixAdd(P1, P4), P5), P7),
                                 matrixAdd(P3, P5), 
                                 matrixAdd(P2, P4), 
                                 matrixAdd(matrixAdd(matrixSub(P1,P2), P3), P6))
        
        C = combineMatr(C11, C12, C21, C22)
        C = [C[i][:originalN] for i in range(originalN)]
        return C
    
    
def defaultMult(X,Y):
    n = len(X)
    C = []
    for i in range(n):
        row = []
        for j in range(n):
            row.append(dotProd(X[i], col(Y, j)))
        C.append(row)
    return C
            


def buildRandMatrix(n):
    A = []
    for i in range(n):
        row = []
        for j in range(n):
            row.append(random.randint(-1,1))
        A.append(row)
    return A


if __name__ = "__main__":
    
    nLim = 100
    stepSize = nLim // 10
    
    nList = [n for n in range(stepSize, nLim, stepSize)]
    strassList = []
    defList = []
    
    for n in nList:
        A = buildRandMatrix(n)
        B = buildRandMatrix(n)
        start = time.time()
        strassenMult(A,B)
        duration = time.time() - start
        
        strassList.append(duration)
        
        start = time.time()
        defaultMult(A,B)
        duration = time.time() - start
        
        defList.append(duration)
        
    plt.plot(nList, strassList, 'r')
    plt.plot(nList, defList, 'g')
    plt.show()

          
    
    
        
        
