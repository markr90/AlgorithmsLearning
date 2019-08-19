# -*- coding: utf-8 -*-
"""
Created on Mon Aug 19 16:01:46 2019

@author: mraaijmakers
"""

import heapq

class median_maintenance(object):
    """ Class that keeps track of the median of a sequence of numbers by repeatedly feeding
    it values of the sequence. Uses two heaps a max and min heap for left of the median and right
    of the median respectively. """
    def __init__(self):
        self.left = [] # max heap (will be inverted i.e x -> -x due to heapq limitations)
        self.right = [] # min heap
        self.median = None
        
    def insert(self, x):
        # base case
        if (len(self.left) + len(self.right)) == 0:
            heapq.heappush(self.left, -1 * x)
            self.median = self._recalcMedian()
            return
        
        # insert
        if x <= -1*(self.left[0]):
            heapq.heappush(self.left, -1 * x)
        else:
            heapq.heappush(self.right, x)
            
        # Rebalance
        if len(self.right) - len(self.left) > 1: # 2 elements extra in the right heap
            a = heapq.heappop(self.right)
            heapq.heappush(self.left, -1 * a)
        elif len(self.left) - len(self.right) > 1: # 2 elements extra in left heap
            a = -1 * heapq.heappop(self.left)
            heapq.heappush(self.right, a)
            
        # recalculate median
        self.median = self._recalcMedian()
        
    def getMedian(self):
        return self.median
    
    def _recalcMedian(self):
        if len(self.left) == len(self.right): # even length case
            m = (-1*self.left[0] + self.right[0]) / 2
        else:
            if len(self.left) > len(self.right):
                m = -1 * self.left[0]
            else:
                m = self.right[0]
        return m
    
    def getList(self):
        lf = [-1 * x for x in self.left]
        xList = lf + self.right
        return xList
            
        
        
    