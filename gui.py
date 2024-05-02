"""
View part of MVC design pattern
Take responsibility about rendering GUI
"""

import tkinter as tk
from tkinter import ttk
from controller import Controller

class GUI(tk.Tk):
    """Main GUI class"""

    def __init__(self):
        super().__init__()

        self.search = Searching(self)

        self.init_component()

        self.controller = None

    def set_controller(self, controller: 'Controller'):
        self.controller = controller

    def init_component(self):
        """Arrange component"""

        self.search.grid(row=0, column=0, sticky='news')
        self.search.button.bind('<Button-1>', self.search_handler)
        self.search.entry.bind('<Return>', self.search_handler)


    def search_handler(self, *args):
        self.controller.search(self.search.query.get())

    def run(self):
        self.mainloop()


class Searching(tk.Frame):
    """Class contain component relate to searching"""

    def __init__(self, root):

        super().__init__(root)

        # Variable for keep track of search entry
        self.query = tk.StringVar()

        # Tree view for showing searching result
        self.result = ttk.Treeview(
            self,
            columns=('name', 'genre'),
            show='headings'
        )

        # Search entry
        self.entry = ttk.Entry(self, textvariable=self.query)

        # Searching button
        self.button = tk.Button(self, text='Search')

        self.init_component()

    def init_component(self):
        """Arrange component"""

        self.entry.grid(row=0, column=0, columnspan=2, sticky='ew')
        self.button.grid(row=0, column=2, sticky='ew')

        self.result.grid(row=1, column=0, columnspan=3, sticky='news')
        self.result.heading('name', text='Name')
        self.result.heading('genre', text='Genres')

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

    def clear_result(self):
        self.result.delete(*self.result.get_children())


class Dicography(tk.Frame):
    """Class contain component relate to discography list"""
    pass


class ArtistInfo(tk.Frame):
    """Class contain component relate to artist information"""
    pass


class DataStoryTelling(tk.Frame):
    """Class contain component relate to data storytelling"""
    pass


