"""
Controller part of design pattern
"""
import tkinter as tk
from textwrap import wrap
import urllib.request
import io
import pandas as pd
from PIL import ImageTk, Image
from artist_db import ArtistDb


class Controller:
    """
    Class responsible for controlling gui
    """

    def __init__(self, ui, model: 'ArtistDb'):
        self.ui = ui
        self.model = model
        self.selected_artist = None
        self.blank_img = ImageTk.PhotoImage(
            Image.open('pic/blank-profile-picture-973460_960_720.webp').resize((300, 300))
        )
        self.showing_image = self.blank_img

        self.ui.info.pic['image'] = self.showing_image

    def search(self, query: str):
        """
        Send search request to database
        :param query: Search keyword
        """

        # Check does query is not a blank string
        if not query:
            return

        result = self.model.search(query)

        # Clear recent result
        self.ui.search.clear_result()

        # Load search result into result treeview
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

        self.selected_artist = self.model.get_selected_artist(artist_id)

        self.show_info()
        self.show_data_analyze()

    def show_info(self):
        """
        Show artist information
        :return:
        """

        # Get artist image from URL
        try:
            self.showing_image = self.get_img(self.selected_artist.img_url)
        except ValueError:
            self.showing_image = self.blank_img

        # Display image and information on GUI
        self.ui.info.pic['image'] = self.showing_image
        self.ui.info.name['text'] = self.selected_artist.artist_name
        self.ui.info.follower['text'] = f"Followers: {self.selected_artist.no_follow:,}"

        self.ui.info.genre['text'] = self.selected_artist\
            .genres\
            .replace('[', '')\
            .replace(']', '')\
            .replace("'", '')

        self.ui.info.genre.configure(
            wraplength=250
        )

        # Show discography and relate artist detail
        self.show_disco()
        self.show_relate_artist()

    def show_disco(self):
        """
        Show selected artist discography
        """

        # Get all album from selected artist
        all_album = self.selected_artist.album.loc[self.selected_artist.album['type'] == 'album']

        # Clear discography treeview
        self.ui.info.clear_disco()

        self.ui.info.album.tag_configure('track', background='light grey')

        # Load every album into treeview
        for i in range(len(all_album)):
            album_iid = self.ui.info.album.insert(
                "",
                tk.END,
                values=[
                    all_album.iloc[i]['album_name'],
                    all_album.iloc[i]['album_id']
                ]
            )

            # Get every track in album
            track_in_album = self.selected_artist.track.loc[
                self.selected_artist.track['album_id'] == all_album.iloc[i]['album_id']
                ]

            # Load all track in to treeview
            for j in range(len(track_in_album)):
                self.ui.info.album.insert(
                    album_iid,
                    tk.END,
                    values=[
                        "   " + track_in_album.iloc[j]['track_name'],
                        track_in_album.iloc[j]['track_id'],
                    ],
                    tags=('track',)
                )

    def show_relate_artist(self):
        """
        Show selected artist's related artist
        """

        # Get all related artist
        related = self.model.get_related_artist(self.selected_artist.id)

        # Clear related artist treeview
        self.ui.search.clear_relate()

        # Load all related artist
        for index in range(len(related)):
            self.ui.search.relate.insert(
                '',
                index,
                values=(related[index][0], ", ".join(related[index][1]), related[index][2])
            )

    def get_img(self, url):

        """
        Generate ImageTk object from url.
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
        """
        Show statistics about artist track
        """

        if not self.selected_artist:
            return

        # Clear all graph
        self.clear_graph()

        # Show popularity statistics
        self.add_statistics()

        # Show every graph
        self.histogram()
        self.scatter()
        self.bar_graph()
        self.pie_chart()

        self.ui.data.canvas.draw()

    def add_statistics(self):
        """
        Show artist track statistics
        """

        # Get most popular track
        if len(self.selected_artist.album) > 0:
            self.ui.data.add_pop_track(
                self.selected_artist.track.sort_values(
                    'popularity', ascending=False
                ).iloc[0, 3]
            )

        # Add each statistics value
        self.ui.data.add_no_album(len(self.selected_artist.album))
        self.ui.data.add_mean(self.selected_artist.track['popularity'].mean())
        self.ui.data.add_sd(self.selected_artist.track['popularity'].std())
        self.ui.data.add_median(self.selected_artist.track['popularity'].median())

        self.ui.data.add_corr(
            self.selected_artist.track.loc[:, ['popularity', 'duration_ms']].corr().loc['popularity', 'duration_ms']
        )

    def histogram(self):
        """
        Show histogram of track popularity distribution
        """

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
        """
        Show scatter chart of correlation between track popularity and track duration
        """

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
        """
        Show bar chart of each album popularity
        """

        release_date_sorted = self.selected_artist.album.sort_values('release_date')

        ax = self.ui.data.ax3
        ax.bar(
            x=release_date_sorted['album_name'],
            height=release_date_sorted['popularity']
        )
        ax.tick_params(axis='x', labelrotation=90)

        ax.set_title('Discography populartiy \nsort by release date')

    def pie_chart(self):
        """
        Show pie chart of ratio of top track from each album
        """

        album_list = self.selected_artist.album.copy().set_index('album_id')['album_name']

        top_tracks = self.model.get_top_tracks(self.selected_artist.id)

        try:
            top_tracks_album_count = \
                pd.DataFrame([track['album'] for track in top_tracks])\
                .groupby('id').count()\

        except KeyError:
            return

        # Oliver messiaen <-- test case

        top_tracks_album_count['album_name'] = [
            album_list.loc[album_id]
            if album_id in album_list
            else None
            for album_id
            in top_tracks_album_count.index

        ]

        top_tracks_album_count.rename(columns={'album_type': 'count'}, inplace=True)

        ax = self.ui.data.ax4

        ax.pie(
            top_tracks_album_count['count'],
            autopct=lambda pct: int(pct/10),
            # labels=top_tracks_album_count['album_name']
        )

        labels = [
            "\n".join(
                wrap(album, 20)
            )
            if album
            else None
            for album in top_tracks_album_count['album_name']
        ]
        # "\n".join(wrap(album,20))
        ax.legend(
            title='Albums',
            labels=labels,
            loc='lower center',
            bbox_to_anchor=(0, -0.4),
            fontsize='xx-small'
        )

        ax.set_title('Number of track in artist\ntop 10 from each album')

    def clear_graph(self):
        """
        Clear all graph axes
        """
        self.ui.data.ax1.cla()
        self.ui.data.ax2.cla()
        self.ui.data.ax3.cla()
        self.ui.data.ax4.cla()
