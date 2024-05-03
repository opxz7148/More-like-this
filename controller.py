"""
Controller part of design pattern
"""
from artist_db import ArtistDb
from PIL import ImageTk, Image
import urllib.request
import io

class Controller:
    """
    Class responsible for controlling gui
    """

    def __init__(self, ui: 'GUI', model: 'ArtistDb'):
        self.ui = ui
        self.model = model
        self.selected_artist = None
        self.showing_image = None

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
        :param arist_id: spotify artist id
        """

        self.selected_artist = self.model.get_selected_artist(artist_id)

        self.show_info()

    def show_info(self):
        """
        Show artist information
        :return:
        """

        self.showing_image = self.get_img(self.selected_artist.img_url)

        self.ui.info.pic['image'] = self.showing_image

    def get_img(self, url):

        with urllib.request.urlopen(url) as u:
            raw_data = u.read()

        image = Image.open(io.BytesIO(raw_data))
        image = image.resize((300, 300))
        photo = ImageTk.PhotoImage(image)

        return photo

