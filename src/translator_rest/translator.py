import requests


class TranslatorRestService(object):

    TRANSLTR_API_URL = 'http://www.transltr.org/api/translate'
    NUM_OF_RETRIES = 10

    def translate(self, text, from_lang='en-US', to_lang='en-US'):
        json = {
            'text': text,
            'from': from_lang,
            'to': to_lang
        }
        for _ in xrange(self.NUM_OF_RETRIES):
            response = requests.post(self.TRANSLTR_API_URL, json=json)
            if response.status_code == 200:
                return response.json()['translationText']
