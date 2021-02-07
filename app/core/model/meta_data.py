from app.core.model.Album import Album
from app.core.model.Artist import Artist


class MetaData:

    __setitem__ = object.__setattr__
    __getitem__ = object.__getattribute__

    """
       model Meta data
    """
    code: ''
    title: ''
    original_title: ''
    summary: ''
    studio: ''
    collections: ''
    originally_available_at: ''
    year: ''
    directors: ''
    category: ''
    # base64 encoded
    poster: ''
    # base64 encoded
    thumbnail: ''
    cache_id: ''
    """
            #base64 encoded
            actor : { 'actor name': 'picture' }
        """
    actor: None

    """
        music
    """
    artist: []
    album: {}

    def __init__(self):
        self.code = ''
        self.title = ''
        self.original_title = ''
        self.summary = ''
        self.studio = ''
        self.collections = ''
        self.originally_available_at = ''
        self.year = ''
        self.directors = ''
        self.category = ''
        self.poster = ''
        self.thumbnail = ''
        self.actor = {}
        self.cache_id = ''
        self.artist = []
        self.album = Album()

    def get_dic(self):
        self.album = self.album.get_dic()
        artist_dict = []
        for artist_obj in self.artist:
            artist_dict.append(artist_obj.get_dic())
        self.artist = artist_dict
        return self.__dict__

