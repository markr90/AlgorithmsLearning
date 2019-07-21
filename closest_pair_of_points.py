# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

class C(object):
    def __init__(self, value):
        self.value = value
        
    def rerun(self, value):
        if value > 0:
            self.__init__(value)