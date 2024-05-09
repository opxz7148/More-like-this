"""
Controller part of design pattern
"""
import pandas as pd

from artist_db import ArtistDb
from PIL import ImageTk, Image
import urllib.request
import io
import numpy as np


class Controller:
    """
    Class responsible for controlling gui
    """

    def __init__(self, ui: 'GUI', model: 'ArtistDb'):
        self.ui = ui
        self.model = model
        self.selected_artist = None
        self.blank_img = ImageTk.PhotoImage(
            Image.open('pic/blank-profile-picture-973460_960_720.webp').resize((300, 300))
        )
        self.showing_image = self.blank_img

        self.ui.info.pic['image'] = self.showing_image

    def search(self, query):

        if not query:
            return

        result = self.model.search(query)

        self.ui.search.clear_result()

        for index in range(len(result)):
            self.ui.search.result.insert(
                '',
                index,
                values=(result[index][0], ", ".join(result[index][1]), result[index][2])
            )

    def select_artist(self, artist_id):
        """
        Handle selected artist
        :param artist_id: spotify artist id
        """

        self.ui.search.disable_detail_button()

        self.selected_artist = self.model.get_selected_artist(artist_id)

        self.show_info()

        self.ui.search.enable_detail_button()

    def show_info(self):
        """
        Show artist information
        :return:
        """

        try:
            self.showing_image = self.get_img(self.selected_artist.img_url)
        except ValueError:
            self.showing_image = self.blank_img

        self.ui.info.pic['image'] = self.showing_image
        self.ui.info.name['text'] = self.selected_artist.artist_name
        self.ui.info.follower['text'] = f"Followers: {self.selected_artist.no_follow}"

        print(type(self.selected_artist.genres))

    def get_img(self, url):

        """
        Get image from url
        :param url: Image url
        :return ImakeTk from url:
        """

        if not url:
            raise ValueError

        with urllib.request.urlopen(url) as u:
            raw_data = u.read()

        image = Image.open(io.BytesIO(raw_data))
        image = image.resize((300, 300))
        photo = ImageTk.PhotoImage(image)

        return photo

    def show_data_analyze(self):

        print('show data')

        if not self.selected_artist:
            return

        self.clear_graph()

        self.histogram()
        self.scatter()
        self.bar_graph()
        self.pie_chart()
        self.ui.data.canvas.draw()

    def histogram(self):

        track_pop = self.selected_artist.track['popularity']

        ax = self.ui.data.ax1
        ax.hist(
            track_pop,
            range=(0, 100),
        )

        ax.set_title("tracks popularity distribution")
        ax.set_ylabel('Frequency')
        ax.set_xlabel('Popularity(1 - 100)')

    def scatter(self):

        track_pop = self.selected_artist.track['popularity']
        track_duration = self.selected_artist.track['duration_ms']

        ax = self.ui.data.ax2
        ax.scatter(
            x=track_pop,
            y=track_duration/1000
        )

        ax.set_title("tracks popularity and\nduration correlation")
        ax.set_ylabel('Track duration (second)')
        ax.set_xlabel('Popularity(1 - 100)')

    def bar_graph(self):
        release_date_sorted = self.selected_artist.album.sort_values('release_date')

        ax = self.ui.data.ax3
        ax.bar(
            x=release_date_sorted['album_name'],
            height=release_date_sorted['popularity']
        )
        ax.tick_params(axis='x', labelrotation=90)

    def pie_chart(self):

        album_list = self.selected_artist.album.copy().set_index('album_id')['album_name']
        print(album_list)

        top_tracks = self.model.get_top_tracks(self.selected_artist.id)
        print(top_tracks)
        top_tracks_album_count = \
            pd.DataFrame([track['album'] for track in top_tracks])\
            .groupby('id').count()\

        print(album_list)

        top_tracks_album_count['album_name'] = [album_list.loc[album_id] for album_id in top_tracks_album_count.index]
        top_tracks_album_count.rename(columns={'album_type': 'count'}, inplace=True)

        ax = self.ui.data.ax4

        ax.pie(
            top_tracks_album_count['count'],
            autopct=lambda pct: int(pct/10),
            # labels=top_tracks_album_count['album_name']
        )

        ax.legend(
            title='Albums',
            labels=top_tracks_album_count['album_name'],
            loc='lower center',
            bbox_to_anchor=(0, -0.25),
            fontsize='xx-small'
        )

        ax.set_title('Number of track in artist\ntop 10 from each album')

    def clear_graph(self):
        self.ui.data.ax1.cla()
        self.ui.data.ax2.cla()
        self.ui.data.ax3.cla()
        self.ui.data.ax4.cla()




