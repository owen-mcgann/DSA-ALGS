from collections import deque
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import layout_helpers as lay

# Global variables to manage graph states
graph = None
previous_steps = deque()
next_steps = deque()

def main():
    root = tk.Tk()
    root.geometry("1400x900")

    # Set up GUI panels
    graph_panel, canvas, ax, no_graph_message, graph_panel = lay.setup_graph_panel(root)
    lay.setup_left_panel(root, canvas, ax, no_graph_message, graph_panel)

    root.mainloop()

if __name__ == "__main__":
    main()
