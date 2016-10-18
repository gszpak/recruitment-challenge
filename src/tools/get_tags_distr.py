from collections import Counter

import click
from bs4 import BeautifulSoup

from utils import plot_distr
from utils import get_html_from_str


def _update_tags_distr(html, tags_distr):
    parsed_html = BeautifulSoup(html, 'html.parser')
    for descendant in parsed_html.descendants:
        if descendant.name is not None:
            tags_distr[descendant.name] += 1


@click.command()
@click.argument('input-file-path', type=click.Path(exists=True, dir_okay=False))
def get_tags_distr(input_file_path):
    tags_distr = Counter()
    with open(input_file_path) as f:
        progress = 0
        for line in f:
            html = get_html_from_str(line)
            if html is None:
                continue
            _update_tags_distr(html, tags_distr)
            progress += 1
            if progress % 10 == 0:
                print 'Progress: {}'.format(progress)
    plot_distr(tags_distr)


if __name__ == '__main__':
    get_tags_distr()
