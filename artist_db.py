"""
Model part of MVC design pattern
Module for artist discography database and spotipy library
"""
import numpy as np
import spotipy
import pandas as pd


class ArtistDb:
    """
    Class for working with artist discography data csv file
    by utilizing pandas dataframe and spotipy library
    """

    def __init__(
            self,
            sp: 'spotipy.Spotify',
            artist_csv_filename: str,
            album_csv_file_name: str,
            track_csv_file_name: str
    ):
        """
        Create instance of artist database
        :param sp: Spotify object from spotipy library for gather data from Spotify web API.
        :param artist_csv_filename: Name of csv file that contain data about each artist.
        :param album_csv_file_name: Name of csv file that contain data about each album.
        :param track_csv_file_name: Name of csv file that contain data about each track.
        """

        self._sp = sp
        self._artist = pd.read_csv(artist_csv_filename)
        self._album = pd.read_csv(album_csv_file_name)
        self._track = pd.read_csv(track_csv_file_name)

        self.__set_up_data(artist_csv_filename, album_csv_file_name, track_csv_file_name)

    def __set_up_data(self, artist_file_name, album_file_name, track_file_name):
        """
        Check dataframe column and set datatype for each column
        """

        artist_correct_column = np.array(
            [
                'artist_name',
                'artist_id',
                'genres',
                'followers',
                'popularity',
                'img_url',
                'external_url',
            ]
        )

        # Validate artist csv table
        if len(self._artist.columns) != len(artist_correct_column):
            raise ValueError(f"{artist_file_name} doesn't have correct number of column")

        if any(self._artist.columns != artist_correct_column):
            raise ValueError(f"{artist_file_name} columns doesn't have correct columns name")

        # Set datatype for each column
        self._artist = self._artist.astype(
            {
                'followers': 'int64',
                'popularity': 'int8',
            },
            copy=True
        )

        album_correct_column = np.array(
            [
                'artist_id',
                'external_url',
                'img_url',
                'album_name',
                'album_id',
                'release_date',
                'release_date_precision',
                'total_tracks',
                'type',
                'popularity'
            ]
        )

        # Validate album csv table
        if len(self._album.columns) != len(album_correct_column):
            raise ValueError(f"{album_file_name} doesn't have correct number of column")

        if any(self._album.columns != album_correct_column):
            raise ValueError(f"{album_file_name} columns doesn't have correct columns name")

        # Set datatypes for each column
        self._album = self._album.astype(
            {
                'total_tracks': 'int16',
                'popularity': 'int8'
            },
            copy=True
        )

        self._album['release_date'].astype('datetime64[ns]')

        track_correct_column = np.array(
            [
                'artist_id',
                'album_id',
                'track_id',
                'track_name',
                'popularity',
                'duration_ms'
            ]
        )

        # Validate track csv table
        if len(self._track.columns) != len(track_correct_column):
            raise ValueError(f"{track_file_name} doesn't have correct number of column")

        if any(self._track.columns != track_correct_column):
            raise ValueError(f"{artist_file_name} columns doesn't have correct columns name")

        # set datatype for each column
        self._track = self._track.astype(
            {
                'popularity': 'int8',
                'duration_ms': 'int32'
            },
            copy=True
        )

    def search(self, query):
        """
        Search artist name by use query as a keyword
        :param query: Search keyword
        :return: List of tuple of artist name, genre, id
        """

        result = self._sp.search(
            query,
            limit=20,
            type='artist',
            market='TH'
        )['artists']['items']

        return [(artist['name'], artist['genres'], artist['id']) for artist in result]

    def add_artist(self, artist_id):
        """
        Add artist to dataframe
        :param artist_id: Spotify artist ID
        """

        if artist_id in self._artist['artist_id'].values:
            return

        artist_detail = self._sp.artist(artist_id)

        try:
            img_url = artist_detail['images'][0]['url']
        except IndexError:
            img_url = None

        self._artist.loc[len(self._artist)] = {
            'artist_name': artist_detail['name'],
            'artist_id': artist_detail['id'],
            'genres': artist_detail['genres'],
            'followers': artist_detail['followers']['total'],
            'popularity': artist_detail['popularity'],
            'img_url': img_url,
            'external_url': artist_detail['external_urls']['spotify'],
        }
        artist_album = self._sp.artist_albums(
            artist_id,
            album_type='album',
            country='TH'
        )['items']
        album_list = [album['id'] for album in artist_album]

        artist_single = self._sp.artist_albums(
            artist_id,
            album_type='single',
            country='TH'
        )['items']
        album_list += [album['id'] for album in artist_single]

        self.__add_album(album_list, artist_id)

    def __add_album(self, album_list, artist_id):
        """
        Add album to dataframe
        :param album_list: List of spotify album id
        :param artist_id: Spotify artist id
        """

        def add_album(album_id_list):

            if not album_id_list:
                return

            all_album = self._sp.albums(album_id_list, market='TH')['albums']

            track_list = []

            for album_detail in all_album:

                try:
                    img_url = album_detail['images'][0]['url']
                except IndexError:
                    img_url = None

                release_date = np.datetime64(album_detail['release_date'], "D")

                self._album.loc[len(self._album)] = {
                    'artist_id': artist_id,
                    'external_url': album_detail['external_urls']['spotify'],
                    'img_url': img_url,
                    'album_name': album_detail['name'],
                    'album_id': album_detail['id'],
                    'release_date': release_date,
                    'release_date_precision': 'day',
                    'total_tracks': album_detail['total_tracks'],
                    'type': album_detail['type'],
                    'popularity': album_detail['popularity']
                }

                track_list += [track['id'] for track in album_detail['tracks']['items']]

            self.__add_track(track_list, artist_id)

        album_id = album_list

        limit = 20

        while len(album_id) > limit:
            add_album(album_id[0:limit])
            album_id = album_id[limit:]

        add_album(album_id)

    def __add_track(self, track_list, artist_id):
        """
        Add track to dataframe
        :param track_list: List of spotify track id
        :param artist_id: Spotify artist id
        """

        def add_track(track_id_list):

            all_track = self._sp.tracks(track_id_list, market='TH')['tracks']

            for track_detail in all_track:

                self._track.loc[len(self._track)] = {
                    'artist_id': artist_id,
                    'album_id': track_detail['album']['id'],
                    'track_id': track_detail['id'],
                    'track_name': track_detail['name'],
                    'popularity': track_detail['popularity'],
                    'duration_ms': track_detail['duration_ms']
                }

        track_id = track_list

        limit = 50

        while len(track_id) > limit:

            add_track(track_id[0:limit])
            track_id = track_id[limit:]

        add_track(track_id)

    def update_csv(self):
        """
        Update csv file
        """
        self._artist.to_csv('csv/artist.csv', index=False)
        self._album.to_csv('csv/album.csv', index=False)
        self._track.to_csv('csv/track.csv', index=False)

    def get_selected_artist(self, artist_id):
        """
        Return Selected artist object
        :param artist_id: Spotify artist_id
        :return: Selected artist object with selected artist information
        """

        if artist_id not in self._artist['artist_id'].values:
            self.add_artist(artist_id)

        artist_df = self._artist.loc[self._artist.artist_id == artist_id]
        album_df = self._album.loc[self._album.artist_id == artist_id]
        track_df = self._track.loc[self._track.artist_id == artist_id]

        return SelectedArtist(artist_df, album_df, track_df)

    def get_top_tracks(self, artist_id):
        """
        Return list of artist top 10 track
        :param artist_id: Spotify artist ID
        :return: list of artist top 10 track
        """
        try:
            return self._sp.artist_top_tracks(artist_id, country='TH')['tracks']
        except spotipy.SpotifyException:
            return None

    def get_related_artist(self, artist_id):
        """
        Return list of artist's relate artist
        :param artist_id: Spotify artist ID
        :return: list of artist's relate artist
        """
        relate = self._sp.artist_related_artists(artist_id)['artists']
        return [(artist['name'], artist['genres'], artist['id']) for artist in relate]


class SelectedArtist:
    """
    Class contain necessary method and attribute for displaying selected artist detail
    """

    def __init__(
            self,
            artist: pd.DataFrame,
            album: pd.DataFrame,
            track: pd.DataFrame
    ):
        """
        :param artist: Dataframe contain selected artist detail
        :param album: Dataframe contain all selected artist album
        :param track: Dataframe contain all track made by selected artist
        """

        self.artist_name = artist.iloc[0, 0]
        self.id = artist.iloc[0, 1]
        self.genres = str(artist.iloc[0, 2])
        self.no_follow = artist.iloc[0, 3]
        self.popularity = artist.iloc[0, 4]
        self.img_url = artist.iloc[0, 5]

        self.album = album
        self.track = track

        print(artist.values)
