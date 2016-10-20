import os

import click
import ujson

import langdetect
from bs4 import NavigableString, BeautifulSoup, Comment
from langdetect.lang_detect_exception import LangDetectException


class HTMLTransformer(object):

    _SKIPPED_TAGS = {
        'area', 'audio', 'br', 'button', 'canvas',
        'code', 'fieldset', 'form', 'img', 'input',
        'keygen', 'map', 'meter', 'noscript',
        'object', 'output', 'param', 'progress',
        'script', 'source', 'style', 'textarea',
        'time', 'track', 'video', 'wbr'
    }

    def __init__(self, html_as_str):
        parsed_html = BeautifulSoup(html_as_str, 'html.parser')
        self.html = self._get_html_root(parsed_html)
        self._html_lang = None

    @property
    def html_lang(self):
        if self._html_lang is None:
            self._html_lang = self._get_html_lang()
        return self._html_lang

    def _get_html_root(self, html_tree):
        all_html = list(html_tree.find_all('html'))
        if not all_html:
            return None
        #assert len(all_html) == 1
        return all_html[0]

    def _get_html_lang(self):
        if self.html is None:
            return None
        if self.html.has_attr('lang'):
            return self.html.get('lang')
        if self.html.has_attr('LANG'):
            return self.html.get('LANG')
        return None

    def _extract_description_from_meta(self, html_node, set_of_strings):
        name = html_node.get('name')
        if name is None or ('description' not in name.lower() and 'keywords' not in name.lower()):
            return
        content = html_node.get('content')
        if content is not None:
            set_of_strings.add(content)

    def _extract_strings_from_node(self, html_node, set_of_strings):
        # NavigableString is a subclass of unicode
        if isinstance(html_node, Comment):
            return
        if isinstance(html_node, NavigableString):
            # skip empty string and BOM
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

    def get_strings_from_html(self):
        if self.html is None:
            return []
        html_strings = set()
        self._extract_strings_from_node(self.html, html_strings)
        # TODO: detect unavailable sites
        return list(html_strings)


def detect_language(description, html_text):
    try:
        return langdetect.detect(description)
    except LangDetectException:
        pass
    try:
        return langdetect.detect(html_text)
    except LangDetectException:
        pass
    return 'en'


# TODO: extract all words + detect language
@click.command()
@click.argument('input-file-path', type=click.Path(exists=True, dir_okay=False))
@click.argument('output-file-path', type=click.Path(exists=False, dir_okay=False))
def extract_text_from_html(input_file_path, output_file_path):
    with open(input_file_path, 'r') as input_file, open(output_file_path, 'w') as output_file:
        progress = 0
        for row in input_file:
            json = ujson.loads(row)
            html_transformer = HTMLTransformer(json['html'])
            html_strings = html_transformer.get_strings_from_html()
            description = json['description']
            language = html_transformer.html_lang
            if language is None:
                language = detect_language(description, ' '.join(html_strings))
            result_json = {
                'html': html_strings,
                'description': description,
                'language': language,
                'industry': json['industry']
            }
            line = ujson.dumps(result_json) + os.linesep
            output_file.write(line)
            progress += 1
            if progress % 100 == 0:
                print 'Progress: {}'.format(progress)


if __name__ == '__main__':
    extract_text_from_html()
