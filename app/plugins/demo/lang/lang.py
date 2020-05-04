from app.plugins.demo.lang.en import text as en_text

from app.plugins.demo.lang.zh import text as zh_text


class I18n:
    lang = 'en'

    def __init__(self, lang):
        self.lang = lang

    def str(self, key):
        if self.lang == 'en':
            return en_text.get(key)

        if self.lang == 'zh':
            return zh_text.get(key)
