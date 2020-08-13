
class MetaData:
    """
       model Meta data
    """

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
    """
        #base64 encoded
        actor : { 'actor name': 'picture' }
    """
    actor: {}

    def __init__(self):
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

    def get_dic(self):
        return self.__dict__

