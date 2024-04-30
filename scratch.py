import tkinter as tk
from tkinter import ttk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np


def hide1(comp: tk.Widget):
    comp.grid_remove()


def show1(comp: tk.Widget):
    comp.grid()


root = tk.Tk()


frame1 = tk.Frame(root)
frame2 = tk.Frame(root)

frame1.grid(row=0, column=0, sticky='NEWS')
frame2.grid(row=0, column=1, sticky='NEWS')

root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)

tree1 = ttk.Treeview(frame1)
tree2 = ttk.Treeview(frame2)

tree1.pack(expand=True)
tree2.pack(expand=True)

button1 = tk.Button(root, text='hide', command=lambda: hide1(tree1))
button2 = tk.Button(root, text='show', command=lambda: show1(tree1))

button1.grid(row=1, column=0)
button2.grid(row=1, column=1)

tk.mainloop()