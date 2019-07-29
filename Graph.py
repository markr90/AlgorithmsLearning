# -*- coding: utf-8 -*-
"""
Created on Sun Jul 28 23:00:28 2019

@author: Mark
"""

class Vertex(object):
    def __init__(self, node):
        self.id = node
        self.adjacent = {}
    
    def __str__(self):
        return str(self.id) + ' -> ' + str([x for x in self.adjacent])
    
    def add_neighbor(self, neighbor, weight = 1):
        self.adjacent[neighbor] = weight
        
    def get_adjacent(self):
        return self.adjacent
    
    def get_connections(self):
        return self.adjacent.keys()
    
    def get_id(self):
        return self.id
    
    def get_weight(self, neighbor):
        return self.adjacent[neighbor]

class Graph(object):
    
    def __init__(self):
        self.vertices = set()
        self.num_vertices = 0
        
    def __iter__(self):
        return iter(self.vertices)

    def get_vertices(self):
        return self.vertices
        
    def add_vertex(self, vert: Vertex):
        for v in self.vertices:
            if v.get_id() == vert.get_id():
                raise ValueError("Vertex " + str(vert.get_id()) + " already exists")
        self.num_vertices += 1
        self.vertices.add(vert)
    
    def get_vertex(self, node):
        for v in self.vertices:
            if v.get_id() == node:
                return v
        return None
    
    def get_nodes(self):
        nodes = []
        for v in self.vertices:
            nodes.append(v.get_id())
        return nodes
    
    def add_edge(self, frm, to, weight = 1, bidirectional = False):
        if frm not in self.get_nodes():
            new_vertex = Vertex(frm)
            new_vertex.add_neighbor(to, weight)
            self.add_vertex(new_vertex)
        else:
            self.get_vertex(frm).add_neighbor(to, weight)
        if to not in self.get_nodes():
            new_vertex = Vertex(to)
            if bidirectional:
                new_vertex.add_neighbor(frm, weight)
            self.add_vertex(new_vertex)
        else:
            if bidirectional:
                self.get_vertex(to).add_neighbor(frm, weight)
            
    
    def __str__(self):
        toPrint = ""
        for v in self.vertices:
            toPrint = toPrint + Vertex.__str__(v) + ", "
        return "<" + toPrint[:-2] + ">"
    
        
        
v1 = Vertex(1)
v1.add_neighbor(2)
v1.add_neighbor(3)

v2 = Vertex(2)
v2.add_neighbor(1)
v2.add_neighbor(3)

v3 = Vertex(3)
v3.add_neighbor(2)
v3.add_neighbor(1)
v3.add_neighbor(4)

v4 = Vertex(4)
v4.add_neighbor(3)

G = Graph()
G.add_vertex(v1)
G.add_vertex(v2)
G.add_vertex(v3)
G.add_vertex(v4)
print(G)