from app.plugins.adultscraperx.lang.lang import I18n


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
    return [
        {
            'type': 'text',
            'label': 'text',
            'model': 'text_model',
            'place_holder': 'place_holder',
        },
        {
            'type': 'select',
            'label': 'select',
            'model': 'select_model',
            'option': [
                {
                    'label': 'label-1',
                    'value': 'value-1'
                },
                {
                    'label': 'label-2',
                    'value': 'value-2'
                },
            ]
        },
        {
            'type': 'switch',
            'label': 'switch',
            'model': 'switch_model',
        },
        {
            'type': 'radio',
            'label': 'radio',
            'model': 'radio_model',
            'place_holder': 'place_holder',
            'option': [
                {
                    'label': 'label-1'
                },
                {
                    'label': 'label-2'
                },
            ]
        },
    ]
