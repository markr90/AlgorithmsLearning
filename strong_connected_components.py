# -*- coding: utf-8 -*-
"""
Created on Sat Aug 17 14:15:06 2019

@author: Mark
"""


from Graph import Vertex, Graph

data = open("data/SCC.txt")

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
    vertex_line = list(map(int, vertex_line))
    
    G.add_edge(vertex_line[0], vertex_line[1], weight = 1, directional=True)
    
    lineNo += 1
    

g_scc = G.SCC(verbose = 1)

sizes = []
for scc in g_scc:
    sizes.append(len(scc))
    
sizes.sort()

print("5 largest SCC components have sizes:", sizes[-5:])