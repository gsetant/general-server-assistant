
class Artist:

    __setitem__ = object.__setattr__
    __getitem__ = object.__getattribute__

    """
       model Meta data
    """

    genres: ''
    tags: ''
    collections: ''
    rating: 0.0
    title: ''
    summary: ''
    # base64 encoded
    poster: ''
    art: ''
    themes: ''

    def __init__(self):
        self.genres = ''
        self.tags = ''
        self.collections = ''
        self.rating = 0.0
        self.title = ''
        self.summary = ''
        # base64 encoded
        self.poster = ''
        self.art = ''
        self.themes = ''

    def get_dic(self):
        return self.__dict__

