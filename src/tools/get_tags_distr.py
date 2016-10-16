from collections import Counter
import ujson

from bs4 import BeautifulSoup
import click
import matplotlib.pyplot as plot
import numpy as np


def _get_html_from_line(line):
    parsed_line = ujson.loads(line)
    return parsed_line.get('html')


def _update_tags_distr(html, tags_distr):
    parsed_html = BeautifulSoup(html, 'html.parser')
    for descendant in parsed_html.descendants:
        if descendant.name is not None:
            tags_distr[descendant.name] += 1


def _print_histogram(tags_distr):
    most_common = tags_distr.most_common(100)
    tags_distr_labels, tags_distr_values = zip(*most_common)
    X = np.arange(len(tags_distr_labels))
    plot.bar(X, tags_distr_values)
    plot.axes().set_xticks(X)
    plot.axes().set_xticklabels(tags_distr_labels, rotation=90)
    ymax = max(tags_distr_values) + 1
    plot.ylim(0, ymax)
    plot.show()


@click.command()
@click.argument('input-file-path', type=click.Path(exists=True, dir_okay=False))
def get_tags_distr(input_file_path):
    tags_distr = Counter()
    with open(input_file_path) as f:
        progress = 0
        for line in f:
            html = _get_html_from_line(line)
            if html is None:
                continue
            _update_tags_distr(html, tags_distr)
            progress += 1
            if progress % 10 == 0:
                print 'Progress: {}'.format(progress)
    _print_histogram(tags_distr)


if __name__ == '__main__':
    get_tags_distr()
