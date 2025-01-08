import tkinter as tk
from tkinter import filedialog, messagebox
import bfs
import dfs
from graph_helpers import update_graph, update_bipartite_graph
from collections import deque
import numpy as np
import networkx as nx

# Global variables for graph steps
previous_steps = deque()
next_steps = deque()
graph = None
current = []
original_capacities = None 
file_path = None

def import_file(message):
    global file_path
    file_path = filedialog.askopenfilename(title="Select a file", filetypes=[("Text files", "*.txt"), 
										("All files", "*.*")])
    if file_path:
        message.delete("1.0", tk.END)
        message.insert(tk.END, "File successfully uploaded.")


def solve_graph(canvas, message, axes, src_entry, sink_entry, graph_panel, ford_fulkerson):
    global original_capacities
    global file_path
    # Get the source and sink values from the entries
    source_input = src_entry.get("1.0", "end-1c").strip()
    sink_input = sink_entry.get("1.0", "end-1c").strip()

    # Check if source and sink are valid integers
    if not source_input.isdigit() or not sink_input.isdigit():
        messagebox.showerror("Input Error", "Please enter valid integer values for source and sink.")
        return
    
    # Check if source and sink are valid integers
    if int(source_input) > int(sink_input):
        messagebox.showerror("Input Error", "Please enter valid integer values for source and sink. Sink must be greater than Source.")
        return    

    # Convert inputs to integers
    source = int(source_input)
    sink = int(sink_input)

    # Display source and sink on the graph panel
    source_display = tk.Text(master=graph_panel, bg='white', foreground="#660000", font=('Times New Roman', 22,),
                             bd=0, width=13, height=1, cursor="arrow", highlightthickness=0)
    source_display.insert(tk.END, ('Source node: ' + source_input))
    source_display.pack()
    source_display.place(x=65, y=30)

    sink_display = tk.Text(master=graph_panel, bg='white', foreground="#660000", font=('Times New Roman', 22,),
                           bd=0, width=13, height=1, cursor="arrow", highlightthickness=0)
    sink_display.insert(tk.END, ('Sink node: ' + sink_input))
    sink_display.pack()
    sink_display.place(x=65, y=60)
	
    if file_path:
        message.destroy()
        canvas.get_tk_widget().place(x=0, y=0)

        # Process the selected file
        global graph
        if ford_fulkerson:
            messagebox.showinfo("Ford-Fulkerson Algorithm", 
                                "The Ford-Fulkerson algorithm finds the maximum flow in a flow network by iteratively finding augmenting paths from the source to the sink. "
                                "It increases flow along these paths until no more augmenting paths can be found. "
                                "This process is repeated until the maximum flow is achieved. Time complexcity is not polynomial it is = O(F*E)")
            
            # Process the file using DFS (Ford-Fulkerson)
            matrix = dfs.load_graph_from_file(file_path)
            graph = dfs.build_graph_from_matrix(matrix)
        else:
            messagebox.showinfo("Edmonds-Karp Algorithm", 
                                "The Edmonds-Karp algorithm is an implementation of the Ford-Fulkerson method that uses BFS to find augmenting paths. "
                                "It systematically explores the flow network level by level, ensuring that the shortest augmenting path is found in each iteration. "
                                "The algorithm continues until no more augmenting paths can be found, guaranteeing a polynomial time complexity(O(V * E²)).")
            
            # Process the file using BFS (Edmonds-Karp)
            matrix = bfs.load_graph_from_file(file_path)
            graph = bfs.build_graph_from_matrix(matrix)

        # Store the original capacities (which are the same as the loaded matrix)
        original_capacities = np.copy(matrix)

        if source >= len(matrix) or sink >= len(matrix) or source < 0 or sink < 0:
            messagebox.showerror("Input Error", "Please enter valid integer values for source and sink. Node not found in graph.")
            return
        
        graph.graph['source'] = source
        graph.graph['sink'] = sink


        if ford_fulkerson:
            flow_steps, max_flow = dfs.ford_fulkerson_nx(graph, source, sink)
        else: 
            flow_steps, max_flow = bfs.edmonds_karp_nx(graph, source, sink)
        max_flow_label = tk.Text(master=graph_panel, bg='white', foreground="#660000", font=('Times New Roman', 22,), 
                           bd=0, width=13, height=1, cursor="arrow", highlightthickness=0)
        max_flow_label.insert(tk.END, ("Max flow: " + str(max_flow)))
        max_flow_label.pack()
        max_flow_label.place(x=850, y=60)


        for flow_matrix in reversed(list(flow_steps)):
            next_steps.append((graph, flow_matrix))
            
		#Add empty graph to start with
        empty_matrix = [[0] * len(next_steps[0][0]) for _ in range(len(next_steps[0][0]))]
        next_steps.append((graph, empty_matrix))

        (graph, first_flow_matrix) = next_steps.pop()
        current.append((graph, first_flow_matrix))
        # Update the graph visualization with the initial flow matrix and original capacities
        update_graph(graph, canvas, graph_panel, axes, first_flow_matrix, original_capacities)

    else: 
        messagebox.showerror("Error", "Please upload a file containing a graph matrix.")   
        return



def show_bipartite_scenario(canvas, message, axes):
    """Bipartite Matching scenario input fields and graph generation."""
    message.destroy()
    canvas.get_tk_widget().place(x=0, y=0)

    # Create a new window for inputs
    bipartite_window = tk.Toplevel()
    bipartite_window.geometry("500x450")
    bipartite_window.title("Bipartite Matching Input")

    # Labels and input fields for number of workers and jobs
    explanation_label = tk.Label(bipartite_window, text="Bipartite Matching finds the maximum matching between two groups (workers and jobs) by using the Ford-Fulkerson Algorithm.", wraplength=400)
    explanation_label.pack()

    workers_label = tk.Label(bipartite_window, text="Number of Workers:")
    workers_label.pack()
    workers_entry = tk.Entry(bipartite_window)
    workers_entry.pack()

    jobs_label = tk.Label(bipartite_window, text="Number of Jobs:")
    jobs_label.pack()
    jobs_entry = tk.Entry(bipartite_window)
    jobs_entry.pack()

    def generate_bipartite_matrix():
        try:
            num_workers = int(workers_entry.get())
            num_jobs = int(jobs_entry.get())
            if num_workers <= 0 or num_jobs <= 0:
                messagebox.showerror("Input Error", "Number of workers and jobs must be positive integers.")
                return
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid integer values for workers and jobs.")
            return

        # Create the matrix for bipartite matching (with super-source and super-sink)
        matrix = np.zeros((num_workers + num_jobs + 2, num_workers + num_jobs + 2))

        # Randomly assign qualifications between workers and jobs
        for i in range(num_workers):
            for j in range(num_jobs):
                matrix[i + 1][num_workers + j + 1] = np.random.randint(0, 2)  # Random binary qualifications

        # Ensure at least one qualification is assigned
        while not np.any(matrix[1:num_workers+1, num_workers+1:num_workers+num_jobs+1]):
            messagebox.showerror("Qualification Error", "No valid worker-job qualifications. Re-assigning qualifications.")
            for i in range(num_workers):
                for j in range(num_jobs):
                    matrix[i + 1][num_workers + j + 1] = np.random.randint(0, 2)

        # Connect super-source to all workers
        for i in range(num_workers):
            matrix[0][i + 1] = 1  # Capacity of 1 from super-source to workers

        # Connect all jobs to the super-sink
        for j in range(num_jobs):
            matrix[num_workers + j + 1][-1] = 1  # Capacity of 1 from jobs to super-sink

        # Explanation of the matrix representation
        messagebox.showinfo("Matrix Explanation", "The adjacency matrix represents workers on the left side, jobs on the right side, and binary values showing qualifications.")

        # Print the adjacency matrix after creation
        print("Generated Adjacency Matrix:")
        for row in matrix:
            print(row)
        print()  # Add a blank line for better readability

        # Build the graph from the adjacency matrix and run the Ford-Fulkerson algorithm
        global graph, next_steps, previous_steps, current, original_capacities  # Ensure original_capacities is global
        graph = dfs.build_graph_from_matrix(matrix)
        source = 0  # Super-source
        sink = num_workers + num_jobs + 1  # Super-sink

        # Initialize original_capacities correctly
        original_capacities = { (u, v): graph[u][v]['capacity'] for u, v in graph.edges() }

        # Run the Ford-Fulkerson algorithm to get the flow and max flow
        flow_steps, max_flow = dfs.ford_fulkerson_nx(graph, source, sink)

        # Test/Check for number of matches
        expected_matches = min(num_workers, num_jobs)
        if max_flow < expected_matches:
            messagebox.showwarning("Matching Warning", f"Only {max_flow} matches found. Maximum possible matches are {expected_matches}.")
        else:
            messagebox.showinfo("Success", f"{max_flow} matches found. This is the maximum possible number of matches.")

        # Print max flow and details of each step
        print(f"Max Flow (number of matches): {max_flow}")
        
        # Clear previous steps and set up for Next/Back functionality
        next_steps.clear()
        previous_steps.clear()  # Ensure clean state
        current.clear()  # Make sure current is cleared before adding any steps

        # Store graph and flow matrix in next_steps
        for flow_matrix_step in reversed(list(flow_steps)):
            next_steps.append((graph, flow_matrix_step))  # Store both graph and matrix together

        # Set up the first flow matrix for visualization
        (graph, first_flow_matrix) = next_steps.pop()
        current.append((graph, first_flow_matrix))  # Add the first step to `current`
        previous_steps.append((graph, first_flow_matrix))

        # Print flow details at each step
        print_flow_details(first_flow_matrix, original_capacities)

        # Add worker and job labels for visualization
        worker_job_labels = {}
        for i in range(1, num_workers + 1):
            worker_job_labels[i] = f"Worker {i}"
        for j in range(1, num_jobs + 1):
            worker_job_labels[num_workers + j] = f"Job {j}"

        # Update the graph with worker-job labels and original capacities
        update_bipartite_graph(graph, canvas, axes, first_flow_matrix, original_capacities, labels=worker_job_labels)

        # Close the input window
        bipartite_window.destroy()

    # Button to generate the bipartite matching matrix
    generate_button = tk.Button(bipartite_window, text="Generate Matrix", command=generate_bipartite_matrix)
    generate_button.pack()

def print_flow_details(flow_matrix, capacities):
    """Print flow details for each edge."""
    print("\nFlow Details (Flow/Capacity) on each edge:")
    total_flow = 0
    for (u, v), capacity in capacities.items():
        flow = flow_matrix[u][v]
        print(f"Edge {u} -> {v}: Flow = {flow}, Capacity = {capacity}")
        total_flow += flow
    print(f"Total flow in this step: {total_flow}")
    print("-" * 40)


def last_augmented_path(root, canvas, axes, graph_panel):
    """Handles going back one step in the flow augmentation process."""
    root.focus_set()
    global original_capacities
    if len(previous_steps) > 0:
        (g, flow_matrix) = previous_steps.pop()
        next_steps.append(current.pop(0))
        current.append((g, flow_matrix))
        update_graph(g, canvas, graph_panel, axes, flow_matrix, original_capacities)
    else:
        messagebox.showinfo("End of Steps", "No previous steps available.")


def find_next_augmented_path(root, canvas, axes, graph_panel):
    """Handles going forward one step in the flow augmentation process."""
    root.focus_set()
    global original_capacities
    if len(next_steps) > 0:
        (g, flow_matrix) = next_steps.pop()
        previous_steps.append(current.pop(0))
        current.append((g, flow_matrix))
        update_graph(g, canvas, graph_panel, axes, flow_matrix, original_capacities)
    else:
        messagebox.showinfo("End of Steps", "No more steps available.")
