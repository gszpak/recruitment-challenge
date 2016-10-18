import ujson
from collections import Counter

import click
from bs4 import BeautifulSoup, NavigableString

KEYS = {'html', 'description', 'industry'}


def tag_has_text(html_node, tags_without_text):
    has_text = False
    if isinstance(html_node, NavigableString):
        return True
    if html_node.name == 'p':
        print list(html_node.children)
    for child in html_node.children:
        if tag_has_text(child, tags_without_text):
            has_text = True
    if html_node.name == 'p':
        print has_text
    if not has_text:
        tags_without_text[html_node.name] += 1
    return has_text


@click.command()
@click.argument('input-file-path', type=click.Path(exists=True, dir_okay=False))
def get_tags_without_text(input_file_path):
    tags_without_text = Counter()
    with open(input_file_path, 'r') as input_file:
        progress = 0
        for line in input_file:
            line_as_json = ujson.loads(line)
            html = line_as_json['html']
            parsed_html = BeautifulSoup(html, 'html.parser')
            tag_has_text(parsed_html, tags_without_text)
            progress += 1
            if progress % 100 == 0:
                print "Progress: {}".format(progress)
    print tags_without_text


if __name__ == '__main__':
    get_tags_without_text()
