# -*- coding: utf-8 -*-
"""
Created on Mon Aug 19 16:39:50 2019

@author: mraaijmakers
"""

from median_maintenance import median_maintenance

data = open("data/median.txt")

lineNo = 0
medMaint = median_maintenance()
medSum = 0
while True:
    if lineNo % 100000 == 0 and lineNo > 0:
        print("Line " + str(lineNo) + " read")
    x = data.readline()
    if not x: break
    x = int(x)
    medMaint.insert(x)
    medSum += medMaint.getMedian()
    
    lineNo += 1
    
print(medSum)