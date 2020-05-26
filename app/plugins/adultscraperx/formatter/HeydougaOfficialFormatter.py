import re

from app.plugins.adultscraperx.formatter.basicFormatter import BasicFormater


class HeydougaOfficialFormatter(BasicFormater):

    def format(code):
        code = 'heydouga-%s' % code
        return code
