"""
Model part of MVC design pattern
Module for artist discography database and spotipy library
"""
import numpy as np
import spotipy
import dotenv
import pandas as pd
from datetime import date


class  Artist_db():
    """
    Class for working with artist discography data csv file by utilizing pandas dataframe and spotipy library
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
        pass

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
                'num_album',
                'num_single',
                'average_toptrack_pop',
                'average_toptrack_duration'
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
                'followers': 'int16',
                'popularity': 'int8',
                'num_album': 'int16',
                'num_single': 'int16',
                'average_toptrack_pop': 'float32',
                'average_toptrack_duration': 'float32'
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
                'album_duration_ms',
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
                'release_date': 'datetime64[ns]',
                'total_tracks': 'int16',
                'album_duration_ms': 'int64',
                'popularity': 'int8'
            },
            copy=True
        )

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





