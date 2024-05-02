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


class Searching(tk.Frame):
    """Class contain component relate to searching"""
    pass


class Dicrography(tk.Frame):
    """Class contain component relate to discography list"""
    pass


class ArtistInfo(tk.Frame):
    """Class contain component relate to artist information"""
    pass


class DataStoryTelling(tk.Frame):
    """Class contain component relate to data storytelling"""
    pass


