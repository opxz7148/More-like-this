import dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from gui import GUI
from controller import Controller
from artist_db import Artist_db

dotenv.load_dotenv()

auth_manager = SpotifyClientCredentials()

sp = Artist_db(
    spotipy.Spotify(auth_manager=auth_manager),
    'csv/artist.csv',
    'csv/album.csv',
    'csv/track.csv'
)
ui = GUI()

controller = Controller(ui, sp)

ui.set_controller(controller)

ui.run()
