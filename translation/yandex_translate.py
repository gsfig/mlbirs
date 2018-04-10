import requests
import translation.yandex_secret as yandex_secret


def yandex_translation(to_translate, lang_from, lang_to):
    """

    :param to_translate:
    :param lang_from:
    :param lang_to:
    :return:
    """

    # For POST requests, the maximum size of the text being passed is 10,000 characters.
    # In GET requests, the restriction applies not to the text itself, but to the size of the entire request string,
    # which can contain other parameters besides the text.
    # The maximum size of the string is from 2 to 10 KB (depending on the browser version).

    url = 'https://translate.yandex.net/api/v1.5/tr.json/translate?key='
    api_key = yandex_secret.get_key()
    text = '&text=' + to_translate
    # text = '&text=' + 'papel' # TODO: remove, for development purpose.
    lang = '&lang=' + lang_from + '-' + lang_to

    full_url = url + api_key + text + lang

    reply = requests.post(full_url)
    reply = reply.json()
    reply_text = ''

    reply_code = reply['code']
    if reply_code == 200:  # Operation completed successfully
        reply_text = reply['text']
    elif reply_code == 401:
        print('yandex translation error: Invalid API key')
    elif reply_code == 402:
        print('yandex translation error: Blocked API key')
    elif reply_code == 404:
        print('yandex translation error: Exceeded the daily limit on the amount of translated text')
    elif reply_code == 413:
        print('yandex translation error: Exceeded the maximum text size')
    elif reply_code == 422:
        print('yandex translation error: The text cannot be translated')
    elif reply_code == 501:
        print('yandex translation error: The specified translation direction is not supported')

    return reply_text[0]
