from app.plugins.douban.lang.lang import I18n


def get_info(lang):
    """

    :param lang: i18n support
    :return: plugin info
        {
            'name': 'has to be same as package name',
            'tittle': 'is the tittle shows by website',
            'version': '1.0',
            'github': 'githubUrl',
            'icon': 'should be a accessible url',
        }
    """
    i18n = I18n(lang)
    return {
        'name': i18n.str('name'),
        'tittle': i18n.str('tittle'),
        'version': '1.0',
        'github': 'https://github.com/AdultScraperX/AdultScraperX.bundle',
        'icon': 'someUrl',

    }


def get_settings(lang):
    i18n = I18n(lang)
    return {
        'name': i18n.str('name'),
        'tittle': i18n.str('tittle')
    }
