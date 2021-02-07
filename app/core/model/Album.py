
class Album:

    __setitem__ = object.__setattr__
    __getitem__ = object.__getattribute__

    """
       model Meta data
    """

    genres: ''
    tags: ''
    collections: ''
    rating: 0.0
    original_title: ''
    title: ''
    summary: ''
    studio: ''
    originally_available_at: ''
    producers: ''
    countries: ''
    # base64 encoded
    poster: ''

    def __init__(self):
        self.genres = ''
        self.tags = ''
        self.collections = ''
        self.rating = 0.0
        self.original_title = ''
        self.title = ''
        self.summary = ''
        self.studio = ''
        self.originally_available_at = ''
        self.producers = ''
        self.countries = ''
        # base64 encoded
        self.poster = ''

    def get_dic(self):
        return self.__dict__

