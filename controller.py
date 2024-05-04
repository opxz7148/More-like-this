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
        :param arist_id: spotify artist id
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
        pass



