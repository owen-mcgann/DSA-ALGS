import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk

LIGHT_BLUE = "#d0e0e3"
DARK_BLUE = "#134f5c"
LIGHT_RED = "#ea9999"
MID_RED = "#990000"
DARK_RED = "#660000"
WORKER_COLOR = "#b6d7a8"  
JOB_COLOR = "#fff2cc"  

node_positions = None
prev_flow_matrix = None

def update_graph(graph, canvas, graph_panel, axes, flow_matrix, original_capacities, labels=None):
    """Redraws the graph on the canvas with flows and capacities from the matrix."""

    global prev_flow_matrix
    global node_positions
    if node_positions is None:
        node_positions = nx.spring_layout(graph)
    
    axes.clear()

    # Add source and sink labels if provided
    if labels:
        labels[0] = "Source"  
        labels[max(labels) + 1] = "Sink"  

    # Draw the graph nodes
    source = graph.graph.get('source')
    sink = graph.graph.get('sink')
    
    # Color nodes based on whether they are workers or jobs
    node_colors = []
    for node in graph.nodes:
        if node == source:
            node_colors.append(LIGHT_RED)  # Super-source
        elif node == sink:
            node_colors.append(LIGHT_RED)  # Super-sink
        elif labels and 'Worker' in labels.get(node, ''):
            node_colors.append(WORKER_COLOR)  # Workers
        elif labels and 'Job' in labels.get(node, ''):
            node_colors.append(JOB_COLOR)  # Jobs
        else:
            node_colors.append(LIGHT_BLUE)  # Default color

    nx.draw(graph, node_color=node_colors, edge_color='white', font_color=DARK_BLUE, font_size=10, ax=axes, pos=node_positions, with_labels=True, labels=labels)
    
    # Highlight edges with non-zero flow (matches)

    if prev_flow_matrix is not None:
        path_edges = [(u, v) for u, v in graph.edges() if flow_matrix[u][v] > 0 or ((flow_matrix[u][v] != prev_flow_matrix[u][v]) and original_capacities[u][v] > 0)]
        curr_path_edges = [(u, v) for u, v in graph.edges() if flow_matrix[u][v] != prev_flow_matrix[u][v] and flow_matrix[u][v] >= 0]
        nx.draw_networkx_edges(graph, node_positions, edgelist=curr_path_edges, edge_color=MID_RED, width=2)

        prev_path_edges = [(u, v) for u, v in graph.edges() if original_capacities[u][v] > 0 and flow_matrix[u][v] == prev_flow_matrix[u][v]]
        nx.draw_networkx_edges(graph, node_positions, edgelist=prev_path_edges, edge_color=MID_RED, width=1)

    else:
        path_edges = [(u, v) for u, v in graph.edges() if flow_matrix[u][v] > 0]
        nx.draw_networkx_edges(graph, node_positions, edgelist=path_edges, edge_color=MID_RED, width=2)


    # Create labels for the edges (flow/capacity)
    path_edge_labels = {}
    for u, v in path_edges:
        flow = flow_matrix[u][v]
        capacity = original_capacities[(u, v)]  # Use original capacities from the dictionary
        path_edge_labels[(u, v)] = f'{int(flow)}/{int(capacity)}'  # Show flow/capacity

    nx.draw_networkx_edge_labels(graph, pos=node_positions, edge_labels=path_edge_labels, font_color=DARK_RED, font_size=8)
    
    # Prepare edge labels for non-highlighted edges (with zero flow)
    non_path_edges = []
    for u, v in graph.edges():
        # Check if the edge exists in original_capacities before accessing it
        if prev_flow_matrix is not None:
            if flow_matrix[u][v] == 0 and original_capacities[u][v] > 0 and flow_matrix[u][v] == prev_flow_matrix[u][v]:
                non_path_edges.append((u, v))
        else:
            if flow_matrix[u][v] == 0 and original_capacities[u][v] > 0:
                non_path_edges.append((u, v))
    nx.draw_networkx_edges(graph, node_positions, edgelist=non_path_edges, edge_color=DARK_BLUE, width=1)
    
    edge_labels = {}
    for u, v in non_path_edges:
        capacity = original_capacities[(u, v)]  # Ensure you are using the original capacities here as well
        edge_labels[(u, v)] = f'0/{int(capacity)}'
    nx.draw_networkx_edge_labels(graph, pos=node_positions, edge_labels=edge_labels, font_color=DARK_BLUE, font_size=8)
    
    # Highlight matched worker-job pairs in red
    if labels:
        matched_edges = [(u, v) for u, v in path_edges if 'Worker' in labels.get(u, '') and 'Job' in labels.get(v, '')]
        # Draw matched edges in red to visually highlight them
        nx.draw_networkx_edges(graph, node_positions, edgelist=matched_edges, edge_color='red', width=2)


    # Update current total flow out of sink
    flow = int(abs(sum(flow_matrix[sink])))

    flow_label = tk.Text(master=graph_panel, bg='white', foreground="#660000", font=('Times New Roman', 22, 'bold'), 
                           bd=0, width=15, height=1, cursor="arrow", highlightthickness=0)
    flow_label.insert(tk.END, ("Current flow: " + str(flow)))
    flow_label.pack()
    flow_label.place(x=850, y=30)


    prev_flow_matrix = flow_matrix
    canvas.draw()
    


def update_bipartite_graph(graph, canvas, axes, flow_matrix, original_capacities, labels=None):
    """Redraws the bipartite graph on the canvas with flows and capacities from the matrix."""
    
    global node_positions
    if node_positions is None:
        node_positions = nx.spring_layout(graph)
    
    axes.clear()

    # Preserve source, sink, and worker/job labels if provided
    if labels:
        labels[0] = "Source"  # Super-source node
        labels[max(labels) + 1] = "Sink"  # Super-sink node

    # Draw the graph nodes with preserved colors and labels
    source = graph.graph.get('source')
    sink = graph.graph.get('sink')
    
    # Color nodes based on whether they are workers or jobs
    node_colors = []
    for node in graph.nodes:
        if node == source:
            node_colors.append(LIGHT_RED)  # Super-source
        elif node == sink:
            node_colors.append(LIGHT_RED)  # Super-sink
        elif labels and 'Worker' in labels.get(node, ''):
            node_colors.append(WORKER_COLOR)  # Workers
        elif labels and 'Job' in labels.get(node, ''):
            node_colors.append(JOB_COLOR)  # Jobs
        else:
            node_colors.append(LIGHT_BLUE)  # Default color

    nx.draw(graph, node_color=node_colors, edge_color='white', font_color=DARK_BLUE, font_size=10, ax=axes, pos=node_positions, with_labels=True, labels=labels)
    
    # Highlight edges with non-zero flow (matches)
    path_edges = [(u, v) for u, v in graph.edges() if flow_matrix[u][v] > 0]
    nx.draw_networkx_edges(graph, node_positions, edgelist=path_edges, edge_color=MID_RED, width=2)
    
    # Create labels for the edges (flow/capacity)
    path_edge_labels = {}
    for u, v in path_edges:
        flow = flow_matrix[u][v]
        if (u, v) in original_capacities:
            capacity = original_capacities[(u, v)]  # Use original capacities from the dictionary
            path_edge_labels[(u, v)] = f'{int(flow)}/{int(capacity)}'  # Show flow/capacity
        else:
            path_edge_labels[(u, v)] = f'{int(flow)}/NA'

    # Draw edge labels with preserved information
    nx.draw_networkx_edge_labels(graph, pos=node_positions, edge_labels=path_edge_labels, font_color=DARK_RED, font_size=8)
    
    # Prepare edge labels for non-highlighted edges (with zero flow)
    non_path_edges = [(u, v) for u, v in graph.edges() if flow_matrix[u][v] == 0 and (u, v) in original_capacities]
    nx.draw_networkx_edges(graph, node_positions, edgelist=non_path_edges, edge_color=DARK_BLUE, width=1)
    
    edge_labels = { (u, v): f'0/{int(original_capacities[(u, v)])}' for u, v in non_path_edges }
    nx.draw_networkx_edge_labels(graph, pos=node_positions, edge_labels=edge_labels, font_color=DARK_BLUE, font_size=8)
    
    # Highlight matched worker-job pairs in red
    if labels:
        matched_edges = [(u, v) for u, v in path_edges if 'Worker' in labels.get(u, '') and 'Job' in labels.get(v, '')]
        nx.draw_networkx_edges(graph, node_positions, edgelist=matched_edges, edge_color='red', width=2)

    canvas.draw()
