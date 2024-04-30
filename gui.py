"""
View part of MVC design pattern
Take responsibility about rendering GUI
"""

import tkinter as tk
from tkinter import ttk


class GUI(tk.Tk):
    """Main GUI class"""

    def __init__(self):
        super().__init__()

    def init_component(self):
        pass


class ArtistInfo:
    pass
