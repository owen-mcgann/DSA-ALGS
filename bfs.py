import networkx as nx
from collections import deque


# Function to build the graph from an adjacency matrix using networkx
def build_graph_from_matrix(matrix):
    g = nx.DiGraph()  
    vertices = len(matrix)
    for i in range(vertices):
        for j in range(vertices):
            if matrix[i][j] > 0:
                g.add_edge(i, j, capacity=matrix[i][j])  # Add edges with capacities
    return g


# Ford-Fulkerson algorithm (Edmonds-Karp using BFS) 
def edmonds_karp_nx(g, source, sink):
    parent = [-1] * g.number_of_nodes()  # To store the augmenting path
    max_flow = 0  
    
    # Initialize a matrix to track the current flow on each edge
    flow_matrix = [[0] * g.number_of_nodes() for _ in range(g.number_of_nodes())]
    flow_steps = []
    
    # Augment the flow while there is a path from source to sink
    while bfs_nx(g, source, sink, parent):
        # Find the maximum flow through the path by BFS
        path_flow = float('Inf')
        s = sink
        path = []
        while s != source:
            u = parent[s]
            path_flow = min(path_flow, g[u][s]['capacity'])
            path.insert(0, s)
            s = parent[s]


        path.insert(0, source)
        
        # Update the flow along the path
        v = sink
        while v != source:
            u = parent[v]
            
            # Update current flow: add flow if going forward, subtract if going backward
            flow_matrix[u][v] += path_flow  
            flow_matrix[v][u] -= path_flow  
            
            # Update residual capacities 
            g[u][v]['capacity'] -= path_flow
            if not g.has_edge(v, u):
                g.add_edge(v, u, capacity=0)
            g[v][u]['capacity'] += path_flow

            v = parent[v]

        flow_steps.append([row[:] for row in flow_matrix])
        max_flow += path_flow

    return flow_steps, max_flow  


# BFS to find an augmenting path from source to sink using networkx graph
def bfs_nx(g, source, sink, parent):
    visited = [False] * g.number_of_nodes()
    queue = deque([source])
    visited[source] = True

    while queue:
        u = queue.popleft()

        for adj in g.successors(u):
            if not visited[adj] and g[u][adj]['capacity'] > 0:
                queue.append(adj)
                visited[adj] = True
                parent[adj] = u
                if adj == sink:
                    return True
    return False


# Function to load the graph from file
def load_graph_from_file(file_name):
    with open(file_name, 'r') as f:
        graph_matrix = eval(f.read())  # Read and convert the string to a list
    return graph_matrix


# MAIN method to run the Edmonds-Karp BFS using networkx
def main():
    file_name = input("Enter the filename containing the graph: ")
    graph_matrix = load_graph_from_file(file_name)
    
    print("Graph matrix loaded:")
    for row in graph_matrix:
        print(row)
    
    g = build_graph_from_matrix(graph_matrix)
    source = int(input("Enter the source node: "))
    sink = int(input("Enter the sink node: "))
    
    
    flow_steps, max_flow = edmonds_karp_nx(g, source, sink)
    
   
    print(f"\nThe maximum possible flow is: {max_flow}")


if __name__ == "__main__":
    main()
