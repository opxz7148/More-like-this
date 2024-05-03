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

        self.controller = None
        self.search = Searching(self)

        self.init_component()

    def set_controller(self, controller: 'Controller'):
        self.controller = controller

    def init_component(self):
        """Arrange component"""

        self.search.grid(row=0, column=0, sticky='news')
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.search.search_button.bind('<Button-1>', self.search_handler)
        self.search.detail_button.bind('<Button-1>', self.artist_selected)
        self.search.entry.bind('<Return>', self.search_handler)

    def search_handler(self, *args):
        self.controller.search(self.search.query.get())

    def artist_selected(self, *args):

        result_tree = self.search.result

        selected_artist = result_tree.item(result_tree.selection()[0])['values']

        print(selected_artist)
        self.controller.select_artist(selected_artist[2])

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
            columns=('name', 'genre', 'id'),
            show='headings'
        )

        # Search entry
        self.entry = ttk.Entry(self, textvariable=self.query)

        # Searching button
        self.search_button = tk.Button(self, text='Search')

        # Show detail button
        self.detail_button = tk.Button(self, text='Show detail')

        self.init_component()

    def init_component(self):
        """Arrange component"""

        self.entry.grid(row=0, column=0, columnspan=2, sticky='ew')

        self.search_button.grid(row=0, column=2, sticky='ew')

        self.detail_button.grid(row=0, column=3, sticky='ew')
        self.detail_button['state'] = tk.DISABLED

        self.result.grid(row=1, column=0, columnspan=4, sticky='news')
        self.result['displaycolumns'] = ['name', 'genre']
        self.result.heading('name', text='Name')
        self.result.heading('genre', text='Genres')
        self.result.bind('<<TreeviewSelect>>', self.enable_detail_button)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)

    def disable_detail_button(self, *args):
        self.detail_button['state'] = tk.DISABLED

    def enable_detail_button(self, *args):
        self.detail_button['state'] = tk.NORMAL

    def clear_result(self):
        self.disable_detail_button()
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


