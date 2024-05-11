"""
View part of MVC design pattern
Take responsibility about rendering GUI
"""
import tkinter as tk
from tkinter import ttk
from threading import Thread
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from controller import Controller

matplotlib.use("TkAgg")


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
        """
        Set GUI controller
        :param controller: Controller class object
        """
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
        """Start progress bar"""
        self.progress.grid(row=2, column=0, columnspan=2, sticky='news')
        self.rowconfigure(2, weight=1)
        self.progress.start(10)

    def finish_progress(self):
        """
        Stop progress bar
        """
        self.progress.grid_forget()
        self.progress.stop()

    def search_handler(self, *args):
        """
        Event handler when search button got press
        :param args:
        :return:
        """
        self.controller.search(self.search.query.get())

    def artist_selected(self, event, *args):
        """
        Event handler when show both show detail button got press
        """

        def thread_check(running_thread: Thread):

            """
            Checking that is thread is still running if not stop the progress bar
            """

            if running_thread.is_alive():
                self.after(10, lambda: thread_check(thread))
            else:
                self.finish_progress()

        # Disabled both button
        self.search.disable_detail_button()
        self.search.disable_relate_detail_button()

        # Get a event widget
        caller = event.widget

        # Determine which treeview to extract data from
        if caller['text'] == 'Show detail':
            result_tree = self.search.result
        else:
            result_tree = self.search.relate

        try:
            selected_artist = result_tree.item(result_tree.selection()[0])['values']
        except IndexError:
            self.search.enable_relate_detail_button()
            return

        print(selected_artist)

        self.show_progress()

        thread = Thread(target=lambda: self.controller.select_artist(selected_artist[2]))
        thread.start()

        thread_check(thread)
        self.search.enable_detail_button()

    def run(self):
        """
        Run GUI mainloop
        """
        self.mainloop()


class Searching(tk.Frame):
    """Class contain component relate to searching"""

    def __init__(self, root):
        """
        Searching part constructor
        :param root: Master component
        """

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

        tk.Label(
            self,
            text="Related Artist",
            font=('Ariel', 15)
        ).grid(row=2, column=0, sticky='news')

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
        """
        Disable relate artist detail button
        """
        self.detail_button2['state'] = tk.DISABLED

    def _(self, *args):
        """
        Enable relate artist detail button
        """
        self.detail_button2['state'] = tk.NORMAL

    def disable_detail_button(self, *args):
        """
        Disable detail button
        """
        self.detail_button['state'] = tk.DISABLED

    def enable_detail_button(self, *args):
        """
        Enable detail button
        """
        self.detail_button['state'] = tk.NORMAL

    def clear_result(self):
        """
        Clear result treeview
        """
        self.disable_detail_button()
        self.result.delete(*self.result.get_children())

    def clear_relate(self):
        """
        Clear relate artist treeview
        :return:
        """
        self.disable_detail_button()
        self.relate.delete(*self.relate.get_children())


class ArtistInfo(tk.Frame):
    """Class contain component relate to artist information"""

    def __init__(self, root):
        """
        Artist info section constructor
        :param root: Master component
        """
        super().__init__(root)

        # Create necessary component in artist info section
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

        self.init_component()

    def init_component(self):
        """
        Arrange component in info section
        """

        self['background'] = 'green'

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
        """
        Clear discography treeview
        """

        self.album.delete(*self.album.get_children())


class DataStoryTelling(tk.Frame):
    """Class contain component relate to data storytelling"""

    def __init__(self, root):
        """
        Data storytelling section constructor
        :param root: Master component
        """

        # Create necessary component
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
        """Arrange component in datastory telling section"""

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

        # Laying out graph

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

    def add_pop_track(self, track: str):
        """
        Change popular track label
        :param track: String of track name
        """
        self.pop_track['text'] = f'Most popular track: {track}'

    def add_no_album(self, no: int):
        """
        Change number of album and single label
        :param no: Integer number of single & album
        """
        self.no_album['text'] = f'Number of single & album: {no}'

    def add_mean(self, mean: float):
        """
        Change mean value in mean label
        :param mean: Float value of mean
        """
        self.mean['text'] = f'Mean: {mean:.2f}'

    def add_sd(self, sd: float):
        """
        Change SD in sd label
        :param sd: Float value of sd
        :return:
        """
        self.sd['text'] = f'Standard Deviation: {sd:.2f}'

    def add_median(self, med: float):
        """
        Change median in median label
        :param med: Float value of median
        """
        self.median['text'] = f'Median: {med}'

    def add_corr(self, corr: float):
        """
        Change correlation in corr label
        :param corr: Float value of correlation
        """
        self.corr['text'] = f'Correlation with duration: {corr:.2f}'
