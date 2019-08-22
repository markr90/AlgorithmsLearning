# -*- coding: utf-8 -*-
"""
Created on Thu Aug 22 13:17:09 2019

@author: mraaijmakers
"""

from Graph import Vertex, Graph

data = open("data/mst_data.txt")

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
    node = int(vertex_line[0])
    neighbor = int(vertex_line[1])
    w = int(vertex_line[2])
    G.add_edge(node, neighbor, weight = w)
    lineNo += 1
    
msf = G.MSF_prims()
mst = msf[0]

for node in mst.get_nodes():
    visited = {node: True}
    v = mst.get_vertex(node)
    totalCost = 0
    for neighbor in v.get_neighbors():
        if visited.get(neighbor):
            continue
        else:
            visited[neighbor] = True
            totalCost += v.get_weight(neighbor)

print(totalCost)