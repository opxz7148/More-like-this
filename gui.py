"""
View part of MVC design pattern
Take responsibility about rendering GUI
"""
import tkinter as tk
from tkinter import ttk
from controller import Controller
from threading import Thread
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class GUI(tk.Tk):
    """Main GUI class"""

    def __init__(self):
        super().__init__()

        self.controller = None
        self.search = Searching(self)
        self.info = ArtistInfo(self)
        self.data = DataStoryTelling(self)
        self.progress = ttk.Progressbar(
            self,
            orient='horizontal',
            mode='indeterminate',
        )

        self.init_component()

    def set_controller(self, controller: 'Controller'):
        self.controller = controller

    def init_component(self):
        """Arrange component"""

        self.title('More like this')

        # search section arrange
        # ========================================================================================
        self.search.grid(row=0, column=0, sticky='news', rowspan=2)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=20)

        self.search.search_button.bind('<Button-1>', self.search_handler)
        self.search.detail_button.bind('<Button-1>', self.artist_selected)
        self.search.detail_button2.bind('<Button-1>', self.artist_selected)

        self.search.entry.bind('<Return>', self.search_handler)

        # info section arrange
        # ========================================================================================
        self.info.grid(row=0, column=1, rowspan=2, sticky='news')
        self.grid_columnconfigure(1, weight=1)

        # Data story telling section arrange
        # ========================================================================================
        self.data.grid(row=0, column=2, rowspan=3, sticky='news')
        self.grid_columnconfigure(2, weight=2)

    def show_progress(self):
        self.progress.grid(row=2, column=0, columnspan=2, sticky='news')
        self.rowconfigure(2, weight=1)
        self.progress.start(10)

    def finish_progress(self):
        self.progress.grid_forget()
        self.progress.stop()

    def search_handler(self, *args):
        print('Search press')
        self.controller.search(self.search.query.get())

    def artist_selected(self, event, *args):

        def thread_check(running_thread: Thread, progress_bar: ttk.Progressbar):

            if running_thread.is_alive():
                self.after(10, lambda: thread_check(thread, progress_bar))
            else:
                self.finish_progress()
                self.search.enable_detail_button()

        self.search.disable_detail_button()
        self.search.disable_relate_detail_button()

        caller = event.widget

        if caller['text'] == 'Show detail':
            result_tree = self.search.result
        else:
            result_tree = self.search.relate

        try:
            selected_artist = result_tree.item(result_tree.selection()[0])['values']
        except IndexError:
            self.search.enable_relate_detail_button()
            return

        self.show_progress()

        print(selected_artist)

        thread = Thread(target=lambda: self.controller.select_artist(selected_artist[2]))
        thread.start()

        thread_check(thread, self.progress)

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

        # Tree view for showing relate artist
        self.relate = ttk.Treeview(
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

        # Show detail button
        self.detail_button2 = tk.Button(self, text='Show relate artist detail')


        self.init_component()

    def init_component(self):
        """Arrange component"""

        self.entry.grid(row=0, column=0, columnspan=2, sticky='news')

        self.search_button.grid(row=0, column=2, sticky='news')

        self.detail_button.grid(row=0, column=3, sticky='news')
        self.detail_button['state'] = tk.DISABLED

        self.result.grid(row=1, column=0, columnspan=4, sticky='news')
        self.result['displaycolumns'] = ['name', 'genre']
        self.result.heading('name', text='Name')
        self.result.heading('genre', text='Genres')

        tk.Label(self, text="Related Artist", font=('Ariel', 15)).grid(row=2, column=0, sticky='news')
        self.detail_button2.grid(row=2, column=3, sticky='news')
        self.detail_button2['state'] = tk.DISABLED


        self.relate.grid(row=3, column=0, columnspan=4, sticky='news')
        self.relate['displaycolumns'] = ['name', 'genre']
        self.relate.heading('name', text='Name')
        self.relate.heading('genre', text='Genres')

        self.result.bind('<<TreeviewSelect>>', self.enable_detail_button)
        self.relate.bind('<<TreeviewSelect>>', self.enable_relate_detail_button)


        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=10)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=10)


        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)

    def disable_relate_detail_button(self, *args):
        self.detail_button2['state'] = tk.DISABLED

    def enable_relate_detail_button(self, *args):
        self.detail_button2['state'] = tk.NORMAL

    def disable_detail_button(self, *args):
        self.detail_button['state'] = tk.DISABLED

    def enable_detail_button(self, *args):
        self.detail_button['state'] = tk.NORMAL

    def clear_result(self):
        self.disable_detail_button()
        self.result.delete(*self.result.get_children())

    def clear_relate(self):
        self.disable_detail_button()
        self.relate.delete(*self.relate.get_children())


class ArtistInfo(tk.Frame):
    """Class contain component relate to artist information"""

    def __init__(self, root):
        super().__init__(root)

        self.pic = tk.Label(self, text='pic')
        self.name = tk.Label(
            self,
            text='Name',
            font=('Ariel', 20),
        )
        self.follower = tk.Label(
            self,
            text='Follower: ',
            font=('Ariel', 20),

        )
        self.genre = tk.Label(
            self,
            text='Genre: ',
            font=('Ariel', 15),

        )
        self.album = ttk.Treeview(
            self,
            columns=('album', 'album_id'),
            show='headings',
            height=7
        )
        self.single = ttk.Treeview(
            self,
            columns=('single', 'album_id'),
            show='headings',
            height=7

        )

        self.init_component()

    def init_component(self):

        self['background'] = 'green'

        bg_color = 'red'

        self.pic.grid(row=0, column=0, sticky='news')
        self.pic['background'] = 'white'

        self.name.grid(row=1, column=0, sticky='news')
        self.name['background'] = 'light grey'

        self.follower.grid(row=2, column=0, sticky='news')
        self.follower['background'] = 'white'

        self.genre.grid(row=3, column=0, sticky='news')
        self.genre['background'] = 'light grey'

        self.album.grid(row=4, column=0, sticky='news')
        self.album['displaycolumns'] = ['album']
        self.album.heading('album', text='Albums')

        self.columnconfigure(0, weight=1)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=2)
        self.rowconfigure(2, weight=2)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=4)

    def clear_disco(self):
        self.album.delete(*self.album.get_children())


class DataStoryTelling(tk.Frame):
    """Class contain component relate to data storytelling"""
    def __init__(self, root):
        super().__init__(root)
        self.canvas = None
        self.canvas_widget = None
        self.ax1 = None
        self.ax2 = None
        self.ax3 = None
        self.ax4 = None
        self.no_album = tk.Label(self, text='Number of single & album: ', anchor=tk.W)
        self.pop_track = tk.Label(self, text='Most popular track: ', anchor=tk.W)
        self.mean = tk.Label(self, text='Mean: ', anchor=tk.W)
        self.sd = tk.Label(self, text='Standard Deviation: ', anchor=tk.W)
        self.median = tk.Label(self, text='Median: ', anchor=tk.W)
        self.corr = tk.Label(self, text='Correlation with duration: ', anchor=tk.W)

        self.init_component()

    def init_component(self):

        self.configure(background='red')

        tk.Label(
            self,
            text="Artist's \npopularity \nanalytic: ",
            font=('Ariel', 15)
        ).grid(row=0, column=0, sticky='news')

        self.no_album.grid(row=0, column=3, sticky='news')
        self.pop_track.grid(row=0, column=1, columnspan=2, sticky='news')

        self.rowconfigure(0, weight=5)

        self.mean.grid(row=1, column=0, sticky="news")
        self.median.grid(row=1, column=1, sticky="news")
        self.sd.grid(row=1, column=2, sticky="news")
        self.corr.grid(row=1, column=3, sticky="news")

        self.rowconfigure(1, weight=5)

        fig = Figure()
        self.ax1 = fig.add_subplot(221)
        self.ax2 = fig.add_subplot(222)
        self.ax3 = fig.add_subplot(223)
        self.ax4 = fig.add_subplot(224)

        fig.tight_layout(pad=4.0)

        self.canvas = FigureCanvasTkAgg(fig, master=self)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(column=0, row=2, columnspan=4, sticky="news")

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)

        self.rowconfigure(2, weight=20)

    def add_pop_track(self, track):
        self.pop_track['text'] = f'Most popular track: {track}'

    def add_no_album(self, no):
        self.no_album['text'] = f'Number of single & album: {no}'

    def add_mean(self, mean):
        self.mean['text'] = f'Mean: {mean:.2f}'

    def add_sd(self, sd):
        self.sd['text'] = f'Standard Deviation: {sd:.2f}'

    def add_median(self, med):
        self.median['text'] = f'Median: {med}'

    def add_corr(self, corr):
        self.corr['text'] = f'Correlation with duration: {corr:.2f}'
