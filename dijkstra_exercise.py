# -*- coding: utf-8 -*-
"""
Created on Sat Aug 17 14:15:06 2019

@author: Mark
"""


from Graph import Vertex, Graph

data = open("data/dijkstra_data.txt")

""" data is in following format "node   neighbor,weight"""

G = Graph()

lineNo = 0
previousNode = 1
v = Vertex(1)
while True:
    if lineNo % 100000 == 0 and lineNo > 0:
        print("Line " + str(lineNo) + " read")
    vertex_line = data.readline()
    if not vertex_line: break
    vertex_line = vertex_line.split()
    neighbors = vertex_line[1:]
    node = int(vertex_line[0])
    
    for neighbor in neighbors:
        nw = neighbor.split(',')
        n = int(nw[0])
        w = int(nw[1])
        G.add_edge(node, n, weight = w, directional = True)
    
    lineNo += 1
    
    
nodesToCalc = [7,37,59,82,99,115,133,165,188,197]

for n in nodesToCalc:
    _, d = G.Dijkstra(1, n)
    print(d)
    

