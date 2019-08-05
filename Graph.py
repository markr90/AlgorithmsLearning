# -*- coding: utf-8 -*-
"""
Created on Sun Jul 28 23:00:28 2019

Implementation of a Graph class
For now all the functionality assumes that the graph is nondirectional
The graph is represented as a dictionary of vertices structured like
{node_label: class Vertex(node_label), ...}

This allows for easy access to each Vertex without having to iterate over 
the entire vertex list to be able to access a specific node

Vertices are created with the Vertex class and consister of a dictionary
and an id (node label) the dictionary consists of all the nodes its connected to
with weights
{neighbor_1: weight_1, neighbor_2: weight_2, ...} 

Assumes weight = 1 if no weight is given

Final structure of the graph is represented like this

<node -> {neighbor_1: weight_1, neighbor_2: weight_2, ...}, ... >

When merging a vertex with another it keeps track of all the vertices a vertex
has been merged with through the merged_vertex_links dictionary. But merging is
irreversible! For example if 1 has been merged with 2,3,4 the dictionary will show
{1: [2,3,4]} 

@author: Mark
"""

from collections import deque
import heapq

class Vertex(object):
    def __init__(self, node):
        self.id = node
        self.neighbor_dict = {}
    
    def set_id(self, node):
        self.id = node
    
    def CreateCopy(self):
        vCopy = Vertex(self.get_id())
        for neighbor in self.get_neighbors():
            vCopy.set_neighbor(neighbor, self.get_weight(neighbor))
        return vCopy
    
    def __str__(self):
        return str(self.id) + ' -> ' + str(self.neighbor_dict)
    
    def set_neighbor_dict(self, neighbor_dict):
        self.neighbor = neighbor_dict
    
    def set_neighbor(self, neighbor, weight = 1):
        self.neighbor_dict[neighbor] = weight
    
    def set_neighbor_weight(self, neighbor, weight):
        self.neighbor_dict[neighbor] = weight
        
    def del_neighbor(self, neighbor):
        try:
            del self.neighbor_dict[neighbor]
        except:
            pass
        
    def get_neighbors(self):
        return list(self.neighbor_dict)
    
    def get_connections(self):
        return self.neighbor_dict.keys()
    
    def get_id(self):
        return self.id
    
    def get_weight(self, neighbor):
        if self.neighbor_dict.get(neighbor, 0) == 0:
            return 0
        else:
            return self.neighbor_dict[neighbor]
    
    

class Graph(object):
    
    def __init__(self, vertex_list_arg = None):
        if vertex_list_arg is not None:
            vertex_dict = {}
            for v in vertex_list_arg:
                vertex_dict[v.get_id()] = v
        else:
            vertex_dict = {}          
        self.vertices = vertex_dict
        self.num_vertices = len(self.vertices)
        self.merged_vertex_links = {}
        for n in self.vertices:
            self.merged_vertex_links[n] = []
            
    def node_exists(self, node):
        return (self.vertices.get(node, None) is not None)
            
    def CreateCopy(self):
        """ Creates a copy of the graph """
        GCopy = Graph()
        for n in self.vertices:
            vCopy = self[n].CreateCopy()
            GCopy.add_vertex(vCopy)
        return GCopy
        
    def __iter__(self):
        return iter(self.vertices)
    
    def __getitem__(self, n):
        try:
            v = self.vertices[n]
        except:
            raise KeyError("Node " + str(n) + " not in graph")
        return v
    
    def __len__(self):
        return len(self.vertices)

    def get_vertices(self):
        return [self.vertices[n] for n in self.vertices]
        
    def add_vertex(self, vert: Vertex):
        # check if vertex exists
        if self.node_exists(vert.get_id()):
            raise ValueError("Vertex with label " + str(vert.get_id()) + " already exists")
        self.num_vertices += 1
        self.merged_vertex_links[vert.get_id()] = []
        self.vertices[vert.get_id()] = vert
        
    def get_vertex(self, node):
        try:
            v = self.vertices[node]
        except:
            raise KeyError("Node " + str(node) + " does not exist in graph")
        return v
    
    def del_vertex(self, node):
        try:
            del self.vertices[node]
            # update other vertices
            for nOther in self.vertices:
                if node in self.vertices[nOther].get_neighbors():
                    self.vertices[nOther].del_neighbor(node)
            self.num_vertices -= 1
        except:
            raise KeyError("Node " + str(node) + " does not exist") 
            
    def get_nodes(self):
        return [n for n in self.vertices]
    
    def add_edge(self, frm, to, weight = 1, directional = False):
        if frm not in self.get_nodes():
            new_vertex = Vertex(frm)
            new_vertex.set_neighbor(to, weight)
            self.add_vertex(new_vertex)
        else:
            self[frm].set_neighbor(to, weight)
        if to not in self.get_nodes():
            new_vertex = Vertex(to)
            if not directional:
                new_vertex.set_neighbor(frm, weight)
            self.add_vertex(new_vertex)
        else:
            if not directional:
                self[to].set_neighbor(frm, weight)
                
    def __str__(self):
        toPrint = ""
        for n in self.vertices:
            v = self.vertices[n]
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
        v1 = self[node1]
        v2 = self[node2]
        
        # Keep track of merged vertices
        # Add node2 to node1
        self.merged_vertex_links[node1].append(node2)
        # Add all the links to node1 links
        self.merged_vertex_links[node1] += self.merged_vertex_links[node2]
        # Delete node2 merged vertex links as the node no longer exists
        del self.merged_vertex_links[node2]
        # Combine the weights
        for neighbor2 in v2.get_neighbors():
            if neighbor2 in v1.get_neighbors():
                w = v1.get_weight(neighbor2) + v2.get_weight(neighbor2)
                v1.set_neighbor_weight(neighbor2, w)
            else:
                w = v2.get_weight(neighbor2)
                v1.set_neighbor(neighbor2, w)
        # remove selfloops
        v1.del_neighbor(node1)
        v1.del_neighbor(node2)
        # update neighbor vertex indices in other vertices
        for vOther in self.get_vertices():
            # Combines the weights of the nodes and updates the neighbor dictionary for
            # the vertex vOther
            if vOther.get_id() not in [node1, node2]:
                w = vOther.get_weight(node1) + vOther.get_weight(node2)
                vOther.set_neighbor_weight(node1, w)
        # Remove the vertex from the graph
        self.del_vertex(node2)
    
    def get_merged_vertex_links(self):
        return self.merged_vertex_links
    
    def _sum_of_weights(nodeSubset, v2):
        sum_of_weights = 0
        for edgeNode in v2.get_neighbors():
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
        verts = self.get_vertices()[1:]
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
    
    def MinimumCut(self, print_cut_size = False):
        GR = self.CreateCopy()
    
        C_left_min, C_right_min, minCutWeight = GR._MinimumCutPhase()
        while len(GR) > 1:
            C_left, C_right, w = GR._MinimumCutPhase()
            # store the cut if it's lighter than the others
            if w < minCutWeight:
                C_left_min, C_right_min, minCutWeight = C_left, C_right, w
        if print_cut_size:        
            return C_left_min, C_right_min, minCutWeight
        else:
            return C_left_min, C_right_min
            
    
    def cut_to_MinCut(self, C_left, C_right):
        verts = self.vertices
        G_left = Graph()
        G_right = Graph()
        
        for cleft in C_left:
            v = verts[cleft].CreateCopy()
            for cright in C_right:
                v.del_neighbor(cright)
            G_left.add_vertex(v)
        
        for cright in C_right:
            v = verts[cright].CreateCopy()
            for cleft in C_left:
                v.del_neighbor(cleft)
            G_right.add_vertex(v)
            
        return G_left, G_right
    
    def BFS(self, start, goal):
        """ Returns list of nodes that create a path from start to goal """ 
        if (not self.node_exists(start) or not self.node_exists(goal)):
            raise KeyError("Start " + str(start) + " or goal " +  str(goal) + " node does not exist")
        if start == goal:
            return [start]
        Q = deque()
        Q.append(start)
        parentDict = {}
        explored = {start: True}
        while len(Q) > 0:
            current = Q.pop()
            currentVert = self.get_vertex(current)
            for neighbor in currentVert.get_neighbors():
                if neighbor == goal:
                    parent = current
                    path = [neighbor, current]
                    while parent != start:
                        parent = parentDict[parent]
                        path.append(parent)
                    path.reverse()
                    return path
                if explored.get(neighbor, False) == False:  
                    parentDict[neighbor] = current
                    explored[neighbor] = True
                    Q.append(neighbor)
        return None

    def Dijkstra(self, start, goal):
        """ Returns list of nodes that create shortest path from start to goal
        @param: start and goal nodes by label
        @returns: [nodes], distance
        Returns None if path does not exist"""
        if (not self.node_exists(start) or not self.node_exists(goal)):
            raise KeyError("Start " + str(start) + " or goal " +  str(goal) + " node does not exist")
        if start == goal:
            return [start]
        Q = []
        dist = {}
        for n in self.get_nodes():
            dist[n] = float('inf')
        dist[start] = 0
        heapq.heappush(Q, (0, start))
        parentDict = {}
        while len(Q) > 0:
            d, current = heapq.heappop(Q)
            currentVert = self.get_vertex(current)
            
            if current == goal:
                parent = parentDict[current]
                path = [current, parent]
                while parent != start:
                    parent = parentDict[parent]
                    path.append(parent)
                path.reverse()
                return path, d
            
            for neighbor in currentVert.get_neighbors():
                alt = d + currentVert.get_weight(neighbor)
                if alt < dist[neighbor]:
                    parentDict[neighbor] = current
                    dist[neighbor] = alt
                    heapq.heappush(Q, (alt, neighbor))

        return None
    
    def reverse(self):
        """ Reverses the graph, returns a new Graph with all the arcs reversed. Leaves old graph as is."""
        Grev = Graph()
        for node in self.get_nodes():
            nodeVertex = self.get_vertex(node)
            for neighbor in nodeVertex.get_neighbors():
                Grev.add_edge(neighbor, node, weight = nodeVertex.get_weight(neighbor), directional = True)
        return Grev     
    
    
    def _DFSLoop(self):
        
        """ Subroutine for the kosaraju algorithm 
        Assumption: All nodes are labeled from 1 to n with no with n the number of nodes
        Returns two dictionaries, one the finishing time for each node: the ith loop that was needed to encounter 
        the final node in the single DFS, other for the node leaders: the node that the DFS started from"""
        n = len(self)
        
        global count
        count = 1
        global s
        s = None
        
        explored = {}
        leaders = {}
        finishing_times = {}
        for i in range(n, 0, -1):
            if explored.get(i, False) == False:
                s = i
                explored = self._DFSalgo(i, explored = explored, finishing_times = finishing_times, leaders = leaders)
        return finishing_times, leaders
    
    def _DFSalgo(self, start, explored = None, finishing_times = None, leaders = None):
        """ DFS algorithm returns a list dictionary of all the nodes that the DFS
        has explored in format {i: True, j: True, ...} All entries will be true by definition
        of them being explored at the end
        @params: explored, finishing times, and leaders are all dictionaries that keep track of 
        the leader of a node and when that node was explored in the kosaraju algorithm
        """
        global count
        global s
        if not self.node_exists(start):
            raise KeyError("Start " + str(start) + " node does not exist")
        if explored == None:
            explored = {}
        if finishing_times == None:
            finishing_times = {}
        if leaders == None:
            leaders = {}
        explored[start] = True
        leaders[start] = s
        currentVert = self.get_vertex(start)
        for neighbor in currentVert.get_neighbors():
            if explored.get(neighbor, False) == False:
                explored[neighbor] = True
                self._DFSalgo(neighbor, explored = explored, finishing_times = finishing_times, leaders = leaders)
        finishing_times[start] = count
        count += 1     
        return explored
    
    def SCC(self):
        """ Creates list of strongly connected components i.e list of lists 
        Returns [[SCC1], [SCC2], ...] with SCCx the list of nodes that are strongly
        connected to each other
        Implemented using the Kosaraju algorithm
        Keeps a matrix to keep track of all the index labels so that the final
        result can be converted back to node labels that are identical to the original graph
        """
        Grev = self.reverse()
        Gori = self.CreateCopy()
        # Dictionary to convert back all the labels that are swapped
        convBack = {}
        # calculate the finishing times for each node in the reversed graph
        finishing_times = Grev._DFSLoop()[0]
        for node in finishing_times:
            convBack[finishing_times[node]] = node
            Gori.get_vertex(node).set_id(finishing_times[node])
        leaders = Gori._DFSLoop()[1]
        connected_sets = {}
        # Compute all the sets that have the same leader
        for ft in leaders:
            l = convBack[leaders[ft]]
            if len(connected_sets.get(l, [])) > 0:
                connected_sets[l].append(convBack[ft])
            else:
                connected_sets[l] = [convBack[ft]]
        return [connected_sets[i] for i in connected_sets]
            
        
        
        
        
        
        
        
    
            
#            
#v1 = Vertex(1)
#v1.set_neighbor(2, 2)
#v1.set_neighbor(5, 3)
#
#v2 = Vertex(2)
#v2.set_neighbor(1, 2)
#v2.set_neighbor(3, 3)
#v2.set_neighbor(5, 2)
#v2.set_neighbor(6, 2)
#
#v3 = Vertex(3)
##v3.set_neighbor(4, 4)
#v3.set_neighbor(7, 2)
#v3.set_neighbor(2, 3)
#
#v4 = Vertex(4)
##v4.set_neighbor(8, 2)
##v4.set_neighbor(7, 2)
##v4.set_neighbor(3, 4)
#
#v5 = Vertex(5)
#v5.set_neighbor(1, 3)
#v5.set_neighbor(2, 2)
#v5.set_neighbor(6, 3)
#
#v6 = Vertex(6)
#v6.set_neighbor(5, 3)
#v6.set_neighbor(2, 2)
#v6.set_neighbor(7, 1)
#
#v7 = Vertex(7)
#v7.set_neighbor(6, 1)
#v7.set_neighbor(3, 2)
##v7.set_neighbor(4, 2)
#v7.set_neighbor(8, 3)
#
#v8 = Vertex(8)
##v8.set_neighbor(4, 2)
##v8.set_neighbor(7, 3)            
#
#G = Graph([v1, v2, v3, v4, v5, v6, v7, v8])            


v1 = Vertex(1)
v1.set_neighbor(2)
#v1.set_neighbor(3)

v2 = Vertex(2)
#v2.set_neighbor(1)
v2.set_neighbor(3)
v2.set_neighbor(4)

v3 = Vertex(3)
v3.set_neighbor(1)
#v3.set_neighbor(2)

v4 = Vertex(4)
v4.set_neighbor(5)

v5 = Vertex(5)
v5.set_neighbor(6)

v6 = Vertex(6)
v6.set_neighbor(7)

v7 = Vertex(7)
v7.set_neighbor(5)


G = Graph([v1, v2, v3, v4, v5, v6, v7])
    



            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            