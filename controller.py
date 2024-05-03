"""
Controller part of design pattern
"""
from artist_db import ArtistDb

class Controller:
    """
    Class responsible for controlling gui
    """

    def __init__(self, ui: 'GUI', model: 'ArtistDb'):
        self.ui = ui
        self.model = model
        self.selected_artist = None

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
