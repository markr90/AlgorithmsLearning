# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from random import randint
import matplotlib.pyplot as plt

def zeroPad(numberString, nZeros, left = True):
    """Return the string with zeros added to the left or right."""
    for i in range(nZeros):
        if left:
            numberString = '0' + numberString
        else:
            numberString = numberString + '0'
    return numberString

def grade_school_mult(x,y):
    x = str(x)
    y = str(y)
    
    total = 0 
    n = 0
    for i in range(1, len(y) + 1):
        val = ""
        for k in range(1, i):
            val = val + "0"
        for j in range(1, len(x) + 1):
            if j == 1:
                takeOver = '0'
            mult = int(y[-1*i]) * int(x[-1*j]) + int(takeOver)
            mult = str(mult)
            digit = mult[-1]
            takeOver = mult[:-1]
            if len(takeOver) == 0:
                takeOver = '0'
            val = digit + val
            n += 1
        total += int(takeOver + val)
    return (total, n)



def karat_mult(x,y):
    global karatN
    x = str(x)
    y = str(y)
    
    if len(x) == 1 and len(y) == 1:
        if x == '0' or y == '0':
            return 0
        else:
            karatN += 1
            return int(x) * int(y)
    
    if len(x) < len(y):
        x = zeroPad(x, len(y)-len(x))
    elif len(y) < len(x):
        y = zeroPad(y, len(x)-len(y))
    n = len(x)
    j = n//2
    if (n % 2) != 0:
        j += 1
    a = int(x[:j])
    b = int(x[j:])
    c = int(y[:j])
    d = int(y[j:])
    ac = karat_mult(a,c)
    bd = karat_mult(b,d)
    adbc = karat_mult(a+b, c+d) - ac - bd
    
    AC = int(zeroPad(str(ac), (n-j)*2, False))
    ADBC = int(zeroPad(str(adbc), n-j, False))
    
    return AC + ADBC + bd

maxN = 100
karatmults = []
grademults = []
n = []
nkarat = []
ngrade = []
for i in range(1,maxN + 1):
    n.append(i)
    nkarat.append(1.5*i**1.58)
    ngrade.append(i**2)
    x = str(randint(1,9))
    y = str(randint(1,9))
    for dig in range(1, i):
        x = x + str(randint(0,9))
        y = y + str(randint(0,9))  
    karatN = 0
    karat_mult(x,y)
    karatmults.append(karatN)
    grademults.append(grade_school_mult(x,y)[1])
    
fig = plt.figure()
plt.plot(n, karatmults, "bs", n, grademults, "g^", n, nkarat, "b--", n, ngrade, "g--")
plt.xlabel("n digits")
plt.ylabel("Number of single digit operations")
plt.title(r"karat $\propto n^{1.58}$ ---- grade $\propto n^2$")
plt.show()
fig.savefig("karat_vs_grade.pdf", bbox_inches = "tight")
    

            
                  
            