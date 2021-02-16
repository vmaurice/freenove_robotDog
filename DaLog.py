#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 10:57:55 2021
For Robodog Project
@author: Blaise
"""

class Log :
    def __init__(self):
        self.log = []
    
    def write(self,something):
        self.log.append(something)
        
    def reverse(self):
        def change(order):
            if (order == "TR" ):
                order = "TL"
            elif (order == "TL"):
                order = "TR"
            elif (order == "SL"):
                order = "SR"
            elif (order == "SR"):
                order = "SL"
            return order
        self.log = [change(x) for x in self.log]
    
    def getLastOrder(self):
        return self.log.pop()
    
    def isEmpty(self):
        return (len(self.log) == 0) 
        
    def show(self):
        for x in self.log :
            print(x)
        
"""log = Log()
log.write("F")
log.write("F")
log.write("TL")
log.write("F")
log.write("TL")
log.write("F")
log.show()


print ("Je me retourne . J'exécute :")
log.reverse()
while ( not log.isEmpty()):
    print(log.getLastOrder())"""