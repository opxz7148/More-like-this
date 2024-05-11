import dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from gui import GUI
from controller import Controller
from artist_db import ArtistDb

if __name__ == "__main__":
    dotenv.load_dotenv()

    auth_manager = SpotifyClientCredentials()

    sp = ArtistDb(
        spotipy.Spotify(auth_manager=auth_manager),
        'csv/artist.csv',
        'csv/album.csv',
        'csv/track.csv'
    )
    ui = GUI()

    controller = Controller(ui, sp)

    ui.set_controller(controller)

    ui.run()

    sp.update_csv()

