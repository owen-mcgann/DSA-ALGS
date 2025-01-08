import networkx as nx
import numpy as np

# Function to build the graph from an adjacency matrix using networkx
def build_graph_from_matrix(matrix):
    """Build a directed graph from an adjacency matrix with capacities."""
    graph = nx.DiGraph()
    n = len(matrix)

    for i in range(n):
        for j in range(n):
            if matrix[i][j] > 0:
                graph.add_edge(i, j, capacity=matrix[i][j])  # Add capacity from matrix

    return graph


# Ford-Fulkerson algorithm using networkx graph
def ford_fulkerson_nx(g, source, sink):
    parent = [-1] * g.number_of_nodes()
    max_flow = 0
    num_vertices = g.number_of_nodes()
    
    # Initialize flow matrix to keep track of the flow values
    flow_matrix = np.zeros((num_vertices, num_vertices))
    flow_steps = []

    # DFS loop to find augmenting paths
    while dfs_nx(g, source, sink, [False] * num_vertices, parent):
        # Find the maximum flow through the path found by DFS
        path_flow = float('Inf')
        s = sink
        while s != source:
            u = parent[s]
            path_flow = min(path_flow, g[u][s]['capacity'])  # Min capacity in path
            s = parent[s]

        # Update flow and residual capacities along the path
        v = sink
        while v != source:
            u = parent[v]
            
            # Update flow values and reverse flow values
            flow_matrix[u][v] += path_flow
            flow_matrix[v][u] -= path_flow  
            
            # Update the residual capacities, not the original
            g[u][v]['capacity'] -= path_flow  # Forward edge residual capacity
            if not g.has_edge(v, u):
                g.add_edge(v, u, capacity=0)  # Add reverse edge if it does not exist
            g[v][u]['capacity'] += path_flow  # Reverse edge residual capacity
            
            # Move to the next node in the path
            v = parent[v]
        
        # Save flow 
        flow_steps.append(flow_matrix.copy())
        max_flow += path_flow
    
    return flow_steps, max_flow


# DFS to find an augmenting path from source to sink using networkx graph
def dfs_nx(g, source, sink, visited, parent):
    visited[source] = True
    if source == sink:
        return True
    
    # Explore all adjacent vertices
    for adj in g.successors(source):
        # If not visited and there is remaining capacity in the edge
        if not visited[adj] and g[source][adj]['capacity'] > 0:
            parent[adj] = source
            if dfs_nx(g, adj, sink, visited, parent):
                return True
    return False


# Function to load graph from file
def load_graph_from_file(file_name):
    with open(file_name, 'r') as f:
        graph_matrix = eval(f.read())  # Read and convert the string to a list
    return graph_matrix


# Main function to run the Ford-Fulkerson algorithm using networkx
def main():
    file_name = input("Enter the filename containing the graph: ")
    graph_matrix = load_graph_from_file(file_name)
    

    
    g = build_graph_from_matrix(graph_matrix)
    source = int(input("Enter the source node: "))
    sink = int(input("Enter the sink node: "))
    
    flow_steps, max_flow = ford_fulkerson_nx(g, source, sink)
    
 
if __name__ == "__main__":
    main()
