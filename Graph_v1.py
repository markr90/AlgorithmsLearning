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
    
    def __init__(self, vertex_list_arg = None):
        if vertex_list_arg is not None:
            vertex_list = vertex_list_arg[:]
        else:
            vertex_list = []            
        self.vertices = vertex_list
        self.vertex_dict = vertex_dict
        self.nodes = [v.get_id() for v in vertex_list]
        self.num_vertices = len(vertex_list)
        self.merged_vertex_links = {}
        for n in self.nodes:
            self.merged_vertex_links[n] = []
        vertex_list = [] # reset the vertex list
        
    def __iter__(self):
        return iter(self.vertices)

    def get_vertices(self):
        return self.vertices
        
    def add_vertex(self, vert: Vertex):
        for v in self.vertices:
            if v.get_id() == vert.get_id():
                raise ValueError("Vertex " + str(vert.get_id()) + " already exists")
        self.num_vertices += 1
        self.nodes.append(vert.get_id())
        self.merged_vertex_links[vert.get_id()] = []
        self.vertices.append(vert)
    
    def del_vertex(self, node):
        if node not in self.get_nodes():
            raise KeyError("Node " + str(node) + " does not exist")
            
        vert = self.get_vertex(node)
        self.vertices.remove(vert)
        # update other vertices
        for vOther in self.get_vertices():
            if node in vOther.get_adjacent():
                vOther.del_adjacent(node)
        self.num_vertices -= 1
    
    def get_vertex(self, node):
        for v in self.vertices:
            if v.get_id() == node:
                return v
        return None
    
    def get_nodes(self):
        return self.nodes
    
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
        # Add node2 to node1
        self.merged_vertex_links[node1].append(node2)
        # Add all the links to node1 links
        self.merged_vertex_links[node1] += self.merged_vertex_links[node2]
        # Delete node2 merged vertex links as the node no longer exists
        del self.merged_vertex_links[node2]
        # Combine the weights
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
        # update adjacent vertex indices in other vertices
        for vOther in self.get_vertices():
            # Combines the weights of the nodes and updates the adjacent dictionary for
            # the vertex vOther
            if vOther.get_id() not in [node1, node2]:
                w = vOther.get_weight(node1) + vOther.get_weight(node2)
                vOther.set_adjacent_weight(node1, w)
        # Remove the vertex from the graph
        self.del_vertex(node2)
    
    def get_merged_vertex_links(self):
        return self.merged_vertex_links
    
    def _sum_of_weights(nodeSubset, v2):
        sum_of_weights = 0
        for edgeNode in v2.get_adjacent():
            if edgeNode in nodeSubset:
                sum_of_weights += v2.get_weight(edgeNode)
        return sum_of_weights
    
    def _MinimumCutPhase(self):
        """ Method required for the Stoer Wagner minimum cut algorithm. 
        """ 
        # Choose arbitrary vertex (node) from the graph
        a = self.get_vertices()[0]
        A = [a]
        A_nodes = [a.get_id()]
        # ignore first arbitrary vertex
        verts = self.vertices[1:]
        while len(A) != self.num_vertices:
            maxVert = verts[0]
            maxNode = maxVert.get_id()
            maxNode_weight_sum = Graph._sum_of_weights(A_nodes, verts[0])
            # find most tightly connected vertex to A
            for v in verts:
                sum_of_w = Graph._sum_of_weights(A_nodes, v)
                if sum_of_w > maxNode_weight_sum:
                    maxVert = v
                    maxNode = v.get_id()
                    maxNode_weight_sum = sum_of_w
            A.append(maxVert)
            A_nodes.append(maxNode)
            verts.remove(maxVert) # don't loop over it again
        
        # Store cut of the phase??
        C_left = []
        for v in A[:-1]:
            C_left.append(v.get_id())
            C_left += self.merged_vertex_links.get(v.get_id(), [])
        #print(C_left)
        C_right = []
        for v in A[-1:]:
            C_right.append(v.get_id())
            C_right += self.merged_vertex_links[v.get_id()]
        self.merge_vertex(A_nodes[-2], A_nodes[-1])
        return C_left, C_right, maxNode_weight_sum # returns the last sum of the weights
    
    def MinimumCut(self):
        G = Graph(vlist)
    
        C_left_min, C_right_min, minCutWeight = G._MinimumCutPhase()
        while len(G.get_vertices()) > 1:
            C_left, C_right, w = G._MinimumCutPhase()
            # store the cut if it's lighter than the others
            if w < minCutWeight:
                C_left_min, C_right_min, minCutWeight = C_left, C_right, w
                
        return C_left_min, C_right_min
    
    def cut_to_MinCut(self, C_left, C_right):
        verts = self.get_vertices()
        G_left = Graph()
        G_right = Graph()
        for a in C_left:
            
        
        
                
                        
                
        
                
v1 = Vertex(1)
v1.add_adjacent(2, 2)
v1.add_adjacent(5, 3)

v2 = Vertex(2)
v2.add_adjacent(1, 2)
v2.add_adjacent(3, 3)
v2.add_adjacent(5, 2)
v2.add_adjacent(6, 2)

v3 = Vertex(3)
v3.add_adjacent(4, 4)
v3.add_adjacent(7, 2)
v3.add_adjacent(2, 3)

v4 = Vertex(4)
v4.add_adjacent(8, 2)
v4.add_adjacent(7, 2)
v4.add_adjacent(3, 4)

v5 = Vertex(5)
v5.add_adjacent(1, 3)
v5.add_adjacent(2, 2)
v5.add_adjacent(6, 3)

v6 = Vertex(6)
v6.add_adjacent(5, 3)
v6.add_adjacent(2, 2)
v6.add_adjacent(7, 1)

v7 = Vertex(7)
v7.add_adjacent(6, 1)
v7.add_adjacent(3, 2)
v7.add_adjacent(4, 2)
v7.add_adjacent(8, 3)

v8 = Vertex(8)
v8.add_adjacent(4, 2)
v8.add_adjacent(7, 3)

G = Graph([v1, v2, v3, v4, v5, v6, v7, v8])
               
        
    
#        
#        
#        
#v1 = Vertex(1)
#v1.add_adjacent(2)
#v1.add_adjacent(3)
#
#v2 = Vertex(2)
#v2.add_adjacent(1)
#v2.add_adjacent(3)
#
#v3 = Vertex(3)
#v3.add_adjacent(2)
#v3.add_adjacent(1)
#v3.add_adjacent(4)
#
#v4 = Vertex(4)
#v4.add_adjacent(3)
#
#G = Graph()
#G.add_vertex(v1)
#G.add_vertex(v2)
#G.add_vertex(v3)
#G.add_vertex(v4)
#print(G)