import re

import langdetect
import nltk
from bs4 import BeautifulSoup, Comment, NavigableString
from langdetect.lang_detect_exception import LangDetectException

from src.translator_rest.translator_rest_service import TranslatorRestService


class JsonTransformer(object):

    def transform(self, json):
        """
        Args:
            | json - input json
        Returns:
            | transformed json
        """
        raise NotImplementedError


class HtmlJsonTransformer(JsonTransformer):
    """
    Extracts text from HTML and detects language
    """

    _SKIPPED_TAGS = {
        'area', 'audio', 'br', 'button', 'canvas',
        'code', 'fieldset', 'form', 'img', 'input',
        'keygen', 'map', 'meter', 'noscript',
        'object', 'output', 'param', 'progress',
        'script', 'source', 'style', 'textarea',
        'time', 'track', 'video', 'wbr'
    }

    def _get_html_roots(self, parsed_html):
        return list(parsed_html.find_all('html'))

    def _get_html_lang(self, html_roots):
        for html_root in html_roots:
            if html_root.has_attr('lang'):
                return html_root.get('lang')
            if html_root.has_attr('LANG'):
                return html_root.get('LANG')
        return None

    def _extract_description_from_meta(self, html_node, set_of_strings):
        name = html_node.get('name')
        if name is None or ('description' not in name.lower() and 'keywords' not in name.lower()):
            return
        content = html_node.get('content')
        if content is not None:
            set_of_strings.add(content)

    def _extract_strings_from_node(self, html_node, set_of_strings):
        if isinstance(html_node, Comment):
            return
        if isinstance(html_node, NavigableString):
            str_to_add = html_node.strip()
            if not str_to_add.isspace():
                set_of_strings.add(str_to_add)
            return
        assert html_node.name is not None
        tag = html_node.name.lower()
        if tag in self._SKIPPED_TAGS:
            return
        if tag == 'meta':
            self._extract_description_from_meta(html_node, set_of_strings)
        for child in html_node.children:
            self._extract_strings_from_node(child, set_of_strings)

    def _get_string_from_html(self, html_roots):
        html_strings = set()
        for html_root in html_roots:
            self._extract_strings_from_node(html_root, html_strings)
        # TODO: detect unavailable sites
        return ' '.join(list(html_strings))

    def _detect_language(self, text):
        try:
            return langdetect.detect(text)
        except LangDetectException:
            return 'en'

    def _detect_html_language(self, html_roots, html_text):
        lang_from_html = self._get_html_lang(html_roots)
        if lang_from_html is not None:
            return lang_from_html
        return self._detect_language(html_text)

    def transform(self, json):
        parsed_html = BeautifulSoup(json['html'], 'html.parser')
        html_roots = self._get_html_roots(parsed_html)
        string_from_html = self._get_string_from_html(html_roots)
        description = json['description']
        html_language = self._detect_html_language(html_roots, string_from_html)
        description_language = self._detect_language(description)
        return {
            'html': string_from_html,
            'description': description,
            'html_language': html_language,
            'description_language': description_language,
            'industry': json['industry']
        }


class TranslatorTransformer(JsonTransformer):

    def __init__(self):
        self._translator_rest_service = TranslatorRestService()

    def _translate(self, text, from_lang):
        # en-US is the default value of en
        if from_lang == 'en' or from_lang == 'en-US' or from_lang == 'en-GB':
            return text
        return self._translator_rest_service.translate(
            text,
            from_lang=from_lang
        )

    def transform(self, json):
        html_translated = self._translate(json['html'], json['html_language'])
        description_translated = self._translate(json['description'], json['description_language'])
        return {
            'html': html_translated,
            'description': description_translated,
            'industry': json['industry']
        }


class TokenizerTransformer(JsonTransformer):

    @staticmethod
    def _convert_to_words(string):
        result = []
        sentences = nltk.sent_tokenize(string)
        for sentence in sentences:
            result.extend(nltk.word_tokenize(sentence))
        return result

    def transform(self, json):
        return {
            'html': self._convert_to_words(json['html']),
            'description': self._convert_to_words(json['description']),
            'industry': json['industry']
        }


class NonWordsEliminatorTransformer(JsonTransformer):

    _WORD_REGEX = re.compile(r'^[a-zA-Z0-9\-\']+$')

    @staticmethod
    def _is_word(word):
        return bool(NonWordsEliminatorTransformer._WORD_REGEX.match(word))

    @staticmethod
    def _filter_non_words(list_of_words):
        return filter(NonWordsEliminatorTransformer._is_word, list_of_words)

    def transform(self, json):
        return {
            'html': self._filter_non_words(json['html']),
            'description': self._filter_non_words(json['description']),
            'industry': json['industry']
        }


class LematizationTransformer(JsonTransformer):

    def __init__(self):
        self.lemmatizer = nltk.stem.WordNetLemmatizer()

    def _lemmatize_word(self, word):
        return self.lemmatizer.lemmatize(word)

    def _lemmatize_words(self, words):
        return map(self._lemmatize_word, words)

    def transform(self, json):
        return {
            'html': self._lemmatize_words(json['html']),
            'description': self._lemmatize_words(json['description']),
            'industry': json['industry']
        }
