import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import graph_helpers
import gui_handlers
import dfs

LIGHT_BLUE = "#d0e0e3"
DARK_BLUE = "#134f5c"

graph = None
graph_panel = None
original_capacities = None  # Initialize globally

def setup_graph_panel(root):
	"""Sets up the graph display panel."""
	global original_capacities
	graph_panel = tk.Frame(root, bg="white", bd=2, width=1100, height=900)
	graph_panel.place(x=350, y=0)

    # Create a Matplotlib figure and axes
	fig, ax = plt.subplots(figsize=(5, 4))

	# Create a canvas to display the figure
	canvas = FigureCanvasTkAgg(fig, master=graph_panel)
	canvas.draw()
	no_graph_message = tk.Text(master=graph_panel, background="white", bd=0, fg="#660000", cursor="arrow", 
                                relief=None, height=2, width=28, font=('Times New Roman', 20, 'italic'),
                                highlightthickness=0)
	no_graph_message.insert(index='insert', chars="No graph currently uploaded.")
	no_graph_message.pack()

	if graph is not None:
		canvas.get_tk_widget().place(x=0, y=0)
	else:
		no_graph_message.place(x=380, y=400)

    # Buttons
	backb = tk.Button(master=graph_panel, width=8, height=2, text="Back", font=("Times New Roman", 20), cursor="hand2",
                  activeforeground="#660000", activebackground="#EA9999", bg="#EA9999", highlightbackground="#EA9999", fg="#660000",
                  command=lambda: gui_handlers.last_augmented_path(root, canvas, ax, graph_panel))  # Set is_bipartite=True here
	backb.place(x=80, y=750)

	forwardb = tk.Button(master=graph_panel, width=8, height=2, text="Next", font=("Times New Roman", 20), cursor="hand2",
                     activeforeground="#660000", activebackground="#EA9999", bg="#EA9999", highlightbackground="#EA9999", fg="#660000",
                     command=lambda: gui_handlers.find_next_augmented_path(root, canvas, ax, graph_panel))  # Set is_bipartite=True here
	forwardb.place(x=820, y=750)


	return graph_panel, canvas, ax, no_graph_message, graph_panel

def setup_left_panel(root, canvas, ax, no_graph_message, graph_panel):
	"""Sets up the left-side panel."""
	left_panel = tk.Frame(root, bg="#d0e0e3", bd=2, width=350, height=900)
	left_panel.grid_propagate(0)
	left_panel.place(x=0, y=0)

	# Import button
	import_button = tk.Button(left_panel, width=9, height=3, font=("Times New Roman", 20), cursor="hand2", text="Import File", 
                              activeforeground="#660000", activebackground="#EA9999", bg="#EA9999", highlightbackground="#EA9999", fg="#660000",
                              command=lambda: gui_handlers.import_file(no_graph_message))
	import_button.place(x=100, y=20)


    # Sink and Source entries
	source_entry = tk.Text(master=left_panel, bg='white', foreground="#660000", font=('Times New Roman', 16, 'italic'), 
                           highlightbackground="#EA9999", width=4, height=1)
	source_entry.pack()
	source_entry.place(x=90, y=140)
	source_label = tk.Text(master=left_panel, bg=LIGHT_BLUE, foreground="#660000", font=('Times New Roman', 16, 'italic'), 
                           bd=0, width=8, height=1, cursor="arrow", highlightthickness=0)
	source_label.insert(tk.END, 'Source')
	source_label.pack()
	source_label.place(x=88, y=170)

	sink_entry = tk.Text(master=left_panel, bg='white', foreground="#660000", font=('Times New Roman', 16, 'italic'), 
                         highlightbackground="#EA9999", width=4, height=1)
	sink_entry.pack()
	sink_entry.place(x=200, y=140)
	sink_label = tk.Text(master=left_panel, bg=LIGHT_BLUE, foreground="#660000", font=('Times New Roman', 16, 'italic'), 
					bd=0, width=8, height=1, cursor="arrow", highlightthickness=0)
	sink_label.insert(tk.END, 'Sink')
	sink_label.pack()
	sink_label.place(x=205, y=170)

    # Ford-Fulkerson and Edmonds-Karp buttons
	ford_fulkerson_button = tk.Button(left_panel, width=16, height=2, font=("Times New Roman", 16), cursor="hand2", text="Ford-Fulkerson",
                             bg="#EA9999", fg="#660000", highlightbackground="#EA9999",
                             activebackground="#EA9999", activeforeground="#660000",
                             command=lambda: gui_handlers.solve_graph(canvas, no_graph_message, ax, source_entry, 
																		 sink_entry, graph_panel, True))
	ford_fulkerson_button.place(x=85, y=220)

	edmonds_karp_button = tk.Button(left_panel, width=16, height=2, font=("Times New Roman", 16), cursor="hand2", text="Edmonds-Karp",
                             bg="#EA9999", fg="#660000", highlightbackground="#EA9999",
                             activebackground="#EA9999", activeforeground="#660000",
                             command=lambda: gui_handlers.solve_graph(canvas, no_graph_message, ax, source_entry, 
																		 sink_entry, graph_panel, False))
	edmonds_karp_button.place(x=85, y=300)

    
    # Bipartite Matching button
	bipartite_button = tk.Button(left_panel, width=16, height=2, font=("Times New Roman", 16), cursor="hand2", text="Bipartite Matching",
                             bg="#EA9999", fg="#660000", highlightbackground="#EA9999",
                             activebackground="#EA9999", activeforeground="#660000",
                             command=lambda: gui_handlers.show_bipartite_scenario(canvas, no_graph_message, ax))
	bipartite_button.place(x=85, y=759)
    
 

	return left_panel