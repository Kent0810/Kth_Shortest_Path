# Python program to print all paths from a source to destination.
  
from collections import defaultdict
  
# This class represents a directed edges
# using adjacency list representation
class Graph: 
    # function to add an edge to edges
    def __init__(self,vertices):
        """
        self.edges is a dict of all possible next nodes
        e.g. {'X': ['A', 'B', 'C', 'E'], ...}
        self.weights has all the weights between two nodes,
        with the two nodes as a tuple as the key
        e.g. {('X', 'A'): 7, ('X', 'B'): 2, ...}
        """
        
        self.V = vertices
        self.edges = defaultdict(list)
        self.results = defaultdict(list)
        self.weights = {}
        index_dict = dict(zip(list(self.edges.keys()), range(len(self.edges.keys()))))
        self.new_dict = []

    
    def add_edge(self, from_node, to_node, weight):
        # Note: assumes edges are bi-directional
        self.edges[from_node].append(to_node)
        self.edges[to_node].append(from_node)
        self.weights[(from_node, to_node)] = weight
        self.weights[(to_node, from_node)] = weight


  
    '''A recursive function to print all paths from 'u' to 'd'.
    visited[] keeps track of vertices in current path.
    path[] stores actual vertices and path_index is current
    index in path[]'''
    def AllPathsUtil(self, u, d, visited, path):
 
        # Mark the current node as visited and store in path
        index_dict = dict(zip(list(self.edges.keys()), range(len(self.edges.keys()))))
        visited[index_dict[u]]= True
        path.append(u)
        
        # If current vertex is same as destination, then print
        # current path[]
        if u == d:
            total_weight = 0
            for i in range(len(path) - 1):
                total_weight += self.weights[path[i], path[i + 1]]
            new_list = path.copy()
            self.new_dict.append((total_weight, new_list)) 
            
        else:
            # If current vertex is not destination
            # Recur for all the vertices adjacent to this vertex
            for i in self.edges[u]:
                if visited[index_dict[i]]== False:
                    self.AllPathsUtil(i, d, visited, path)
                     
        # Remove current vertex from path[] and mark it as unvisited
        path.pop()
        visited[index_dict[u]]= False
  
  
    # Prints all paths from 's' to 'd'
    def AllPaths(self, s, d):
        
        # Mark all the vertices as not visited
        visited =[False]*(self.V)
 
        # Create an array to store paths
        path = []

        

        # Call the recursive helper function to print all paths
        self.AllPathsUtil(s, d, visited, path)
    
    def k_shortestPath(self,k, traversed_egdes):
#       
        result_list =[]
        for weight, path in self.new_dict :
            num_path = 0
            for traversed_egde in traversed_egdes:
                if traversed_egde[0] in path and traversed_egde[1] in path:
                    if(path[path.index(traversed_egde[0])+1] == traversed_egde[1]) or (path[path.index(traversed_egde[1])+1] == traversed_egde[0]): num_path+=1
            if num_path == len(traversed_egdes):
                result_list.append((weight, path))

        sorted_result_list = sorted(result_list, key = lambda k: k[0])
        if k > 0 and k <= len(sorted_result_list):
            print(sorted_result_list[k-1])
        else:
            print("No result.")

  

if __name__ == '__main__':
    #add edges
    edges = [
        ('X', 'A', 7),
        ('X', 'B', 2),
        ('X', 'C', 3),
        ('X', 'E', 4),
        ('A', 'B', 3),
        ('A', 'D', 4),
        ('B', 'D', 4),
        ('B', 'H', 5),
        ('C', 'L', 2),
        ('D', 'F', 1),
        ('F', 'H', 3),
        ('G', 'H', 2),
        ('G', 'Y', 2),
        ('I', 'J', 6),
        ('I', 'K', 4),
        ('I', 'L', 4),
        ('J', 'L', 1),
        ('K', 'Y', 5),
        ]
    
    
    #input
    n_0 = 14
    #edges=list()
    # n_0 = int(input("Enter the number edges: "))
    # for i in range(n_0):
    #     input_edge = input(f"Enter edge {i}: ").split(" ")
    #     edges.append(*(input_edge[0], input_edge[1], input_edge[2]))


    x = input("Enter initial point: ")
    y = input("Enter the teminal point: ")

    traversed_egdes=[]
    n_1 = int(input("Enter the number edges to traverse: "))
    if n_1 > 0:
        for i in range(n_1):
            traversed_egdes.append(input(f"Enter edge {i+1}: "))
    # Create a edges given in the above diagram
    graph = Graph(n_0)
    for edge in edges:
        graph.add_edge(*edge)

    print ("Following are all different paths from %s to %s :" %(x, y))
    graph.AllPaths(x, y)

    k = int(input("Enter k:"))
    graph.k_shortestPath(k,traversed_egdes)
