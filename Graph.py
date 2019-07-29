# -*- coding: utf-8 -*-
"""
Created on Sun Jul 28 23:00:28 2019

@author: Mark
"""

class Vertex(object):
    def __init__(self, node):
        self.id = node
        self.adjacent = {}
    
    def set_id(self, node):
        self.id = node
    
    def __str__(self):
        return str(self.id) + ' -> ' + str(self.adjacent)
    
    def set_adjacent_dict(self, adj_dict):
        self.adjacent = adj_dict
    
    def add_adjacent(self, neighbor, weight = 1):
        if neighbor in self.adjacent:
            self.adjacent[neighbor] += weight
        else:
            self.adjacent[neighbor] = weight
    
    def set_adjacent_weight(self, adj, weight):
        self.adjacent[adj] = weight
        
    def del_adjacent(self, adj):
        del self.adjacent[adj]
        
    def get_adjacent(self):
        return self.adjacent
    
    def get_connections(self):
        return self.adjacent.keys()
    
    def get_id(self):
        return self.id
    
    def get_weight(self, neighbor):
        if neighbor not in self.adjacent:
            return 0
        else:
            return self.adjacent[neighbor]
    
    

class Graph(object):
    
    def __init__(self, vertex_list = []):
        self.vertices = vertex_list
        self.num_vertices = 0
        self.merged_vertex_links = {}
        
    def __iter__(self):
        return iter(self.vertices)

    def get_vertices(self):
        return self.vertices
        
    def add_vertex(self, vert: Vertex):
        for v in self.vertices:
            if v.get_id() == vert.get_id():
                raise ValueError("Vertex " + str(vert.get_id()) + " already exists")
        self.num_vertices += 1
        self.vertices.append(vert)
    
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
    
    def add_edge(self, frm, to, weight = 1, directional = False):
        if frm not in self.get_nodes():
            new_vertex = Vertex(frm)
            new_vertex.add_adjacent(to, weight)
            self.add_vertex(new_vertex)
        else:
            self.get_vertex(frm).add_adjacent(to, weight)
        if to not in self.get_nodes():
            new_vertex = Vertex(to)
            if not directional:
                new_vertex.add_adjacent(frm, weight)
            self.add_vertex(new_vertex)
        else:
            if not directional:
                self.get_vertex(to).add_adjacent(frm, weight)
    
    def del_vertex(self, v: Vertex):
        if v.get_id() in self.get_nodes():
            self.vertices.remove(v)
    
    def __str__(self):
        toPrint = ""
        for v in self.vertices:
            toPrint = toPrint + Vertex.__str__(v) + ", "
        return "<" + toPrint[:-2] + ">"
    
    def merge_vertex(self, node1, node2):
        """ 
        WARNING: This modifies the graph irreversably!! Can not retrieve the original graph 
        after doing this.
        
        Merges node2 in to node1, i.e node1 <--- node2 
        Keeps track of the merged vertices in the merged_vertex_links dictionary
        Deletes self loops
        Deletes the vertex node2
        Merges all the nodes in the vertices i != 1,2 and updates weights accordingly"""
        v1 = self.get_vertex(node1)
        v2 = self.get_vertex(node2)
        
        if node2 not in v1.get_adjacent() and node1 not in v2.get_adjacent():
            raise KeyError("Nodes " + str(node1) + " and " + str(node2) + " are not adjacent")
        
        # Keep track of merged vertices
        if node1 not in self.merged_vertex_links:
            self.merged_vertex_links[node1] = [node2]
        else:
            self.merged_vertex_links[node1].append(node2)
        
        for adj2 in v2.get_adjacent():
            if adj2 in v1.get_adjacent():
                w = v1.get_weight(adj2) + v2.get_weight(adj2)
                v1.set_adjacent_weight(adj2, w)
            else:
                w = v2.get_weight(adj2)
                v1.add_adjacent(adj2, w)
                
        # remove selfloops
        v1.del_adjacent(node1)
        v1.del_adjacent(node2)
        
        self.del_vertex(v2)
        
        # update links in other vertices
        for v in self.get_vertices():
            new_adjacent_dict = {}
            for adj in v.get_adjacent():
                if adj == node2 or adj == node1:
                    w = v.get_weight(node1) + v.get_weight(node2)
                    new_adjacent_dict[node1] = w
                elif adj not in [node1, node2]:
                    w = v.get_weight(adj)
                    new_adjacent_dict[adj] = w
            v.set_adjacent_dict(new_adjacent_dict)
    
    def get_merged_vertex_links(self):
        return self.merged_vertex_links
                
                
        
         
        
        
        
v1 = Vertex(1)
v1.add_adjacent(2)
v1.add_adjacent(3)

v2 = Vertex(2)
v2.add_adjacent(1)
v2.add_adjacent(3)

v3 = Vertex(3)
v3.add_adjacent(2)
v3.add_adjacent(1)
v3.add_adjacent(4)

v4 = Vertex(4)
v4.add_adjacent(3)

G = Graph()
G.add_vertex(v1)
G.add_vertex(v2)
G.add_vertex(v3)
G.add_vertex(v4)
print(G)