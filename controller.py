"""
Controller part of design pattern
"""
from artist_db import Artist_db

class Controller:
    """
    Class responsible for controlling gui
    """

    def __init__(self, ui: 'GUI', model: 'Artist_db'):
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
                values=(result[index][0], ", ".join(result[index][1]))
            )

