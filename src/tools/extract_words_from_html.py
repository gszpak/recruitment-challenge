import os

import click
import ujson
from bs4 import NavigableString, BeautifulSoup

SKIPPED_TAGS = {
    'area', 'audio', 'br', 'button', 'canvas',
    'code', 'fieldset', 'form', 'img', 'input',
    'keygen', 'map', 'meter', 'noscript',
    'object', 'output', 'param', 'progress',
    'script', 'source', 'style', 'textarea',
    'time', 'track', 'video', 'wbr'
}


def _extract_description_from_meta(html_node, bag_of_strings):
    if html_node.name != 'meta':
        return
    name = html_node.get('name')
    if name is None or 'description' not in name.lower():
        return
    content = html_node.get('content')
    if content is not None:
        bag_of_strings.append(content)


def extract_strings_from_node(html_node, list_of_strings):
    # NavigableString is a subclass of unicode
    if html_node.name in SKIPPED_TAGS:
        return
    if isinstance(html_node, NavigableString):
        list_of_strings.append(html_node)
        return
    for child in html_node.children:
        extract_strings_from_node(child, list_of_strings)


@click.command()
@click.argument('input-file-path', type=click.Path(exists=True, dir_okay=False))
@click.argument('output-file-path', type=click.Path(exists=False, dir_okay=False))
def extract_text_from_html(input_file_path, output_file_path):
    with open(input_file_path, 'r') as input_file, open(output_file_path, 'w') as output_file:
        for row in input_file:
            json = ujson.loads(row)
            strings = []
            html_tree = BeautifulSoup(json['html'], 'html.parser')
            extract_strings_from_node(html_tree, strings)
            result_json = {
                'html': strings,
                'description': json['description'],
                'industry': json['industry']
            }
            line = ujson.dumps(result_json) + os.linesep
            output_file.write(line)
