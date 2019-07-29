# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import random
import time
import matplotlib.pyplot as plt


def bruteForce(points):
    
    minDist = distance(points[0], points[1])
    (p, q) = (points[0], points[1])
    n = len(points)
    
    for i in range(n):
        for j in range(i+1, n):
            dist = distance(points[i], points[j])
            if dist < minDist:
                minDist = dist
                (p, q) = (points[i], points[j])
    return (p, q, minDist)

    
def distance(a,b):
    return ((a[0]-b[0])**2 + (a[1] - b[1])**2)**0.5


def closest_split_pair(pointsX, pointsY, delta, bestPair):
    pBest = bestPair[0]
    qBest = bestPair[1]
    
    nX = len(pointsX)
    midpoint = pointsX[nX//2][0]
    
    subDeltaY = []
    for py in pointsY:
        if py[0] < midpoint + delta and py[0] > midpoint - delta:
            subDeltaY.append(py)
    
    best = delta
    nSy = len(subDeltaY)
    for i in range(nSy - 1):
        for j in range(i+1, min(i+7, nSy)):
            p, q = subDeltaY[i], subDeltaY[j]
            dist = distance(p, q)
            if dist < best:
                pBest, qBest = p, q
                best = dist
    return (pBest, qBest, best)               
    

def closestPair(pointsX, pointsY):
    n = len(pointsX)
    mid = n//2   
        
    if len(pointsX) < 4:
        return bruteForce(pointsX)
    else:
        Xleft = pointsX[:mid]
        Xright = pointsX[mid:]
    
        midpoint = pointsX[mid][0]
        Yleft = []
        Yright = []
        for py in pointsY:
            if py[0] < midpoint:
                Yleft.append(py)
            else:
                Yright
                
        (pLbest, qLbest, dLmin) = closestPair(Xleft, Yleft)
        (pRbest, qRbest, dRmin) = closestPair(Xright, Yright)
        
        if dLmin < dRmin:
            (p, q) = (pLbest, qLbest)
            minDist = dLmin
        else:
            (p, q) = (pRbest, qRbest)
            minDist = dRmin
                
        (pLRbest, qLRbest, dLRmin) = closest_split_pair(pointsX, pointsY, minDist, (p, q))
        
        if dLRmin < minDist:
            (p, q) = (pLRbest, qLRbest)
            minDist = dLRmin
            
        return (p, q, minDist)
    
    
    
if __name__ == "__main__":
    
    nLim = 1000
    stepSize = nLim // 50
    nList = list(range(stepSize, nLim, stepSize))
    recursiveData = []
    bruteforceData = []
    
    coords = []
    for i in range(nLim):
        coords.append([random.random(), random.random()])
    
    for n in nList:
        
        coordsSubSet = coords[:n]
        
        start = time.time()
        coordsX = sorted(coordsSubSet, key = lambda x: x[0])
        coordsY = sorted(coordsSubSet, key = lambda x: x[1])
        (p, q, minDist) = closestPair(coordsX, coordsY)
        runTime = time.time() - start
        recursiveData.append(runTime)
        
        #print("Recursive algorithm: best pair of points:", p, "and", q, ", distance =", minDist)
        
        start = time.time()
        (p, q, minDist) = bruteForce(coordsSubSet) 
        runTime = time.time() - start
        bruteforceData.append(runTime)
        
        #print("Bruteforce algorithm: best pair of points:", p, "and", q, ", distance =", minDist)
    
    plt.plot(nList, recursiveData, 'r')
    plt.plot(nList, bruteforceData, 'g')
    plt.xlabel("N points")
    plt.ylabel("runtime (seconds)")
    plt.title("Divide and conquer closest pair (red) vs bruteforce (green)")
    plt.savefig("closest_pair_performance.pdf")
    plt.show()