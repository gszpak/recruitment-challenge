import requests


class TranslatorRestService(object):

    TRANSLTR_API_URL = 'http://www.transltr.org/api/translate'
    _NUM_OF_RETRIES = 10
    _CHUNK_SIZE = 30

    def _generate_chunk(self, text_words):
        for i in xrange(0, len(text_words), self._CHUNK_SIZE):
            yield ' '.join(text_words[i:i + self._CHUNK_SIZE])

    def _translate_chunk(self, text_chunk, from_lang, to_lang):
        json = {
            'text': text_chunk,
            'from': from_lang,
            'to': to_lang
        }
        for _ in xrange(self._NUM_OF_RETRIES):
            try:
                response = requests.post(self.TRANSLTR_API_URL, json=json)
                if response.status_code == 200:
                    return response.json()['translationText']
            except requests.RequestException:
                pass
        print "WARNING: chunk not translated"

    def translate(self, text, from_lang='en-US', to_lang='en-US'):
        text_words = text.split()
        result = []
        for text_chunk in self._generate_chunk(text_words):
            translated_chunk = self._translate_chunk(text_chunk, from_lang, to_lang)
            if translated_chunk:
                result.append(translated_chunk)
        return ' '.join(result)
