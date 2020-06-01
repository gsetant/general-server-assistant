
class MetaData:
    """
       model Meta data
    """

    tittle: ''
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

    def get_dic(self):
        return self.__dict__

