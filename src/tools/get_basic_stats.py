import ujson
from collections import Counter

import click

from utils import detect_language, plot_distr


KEYS = {'html', 'description', 'industry'}


@click.command()
@click.argument('input-file-path', type=click.Path(exists=True, dir_okay=False))
def get_tags_distr(input_file_path):
    label_distr = Counter()
    instances_without_html = 0
    instances_without_descr = 0
    instances_not_in_eng = 0
    with open(input_file_path, 'r') as input_file:
        progress = 0
        for line in input_file:
            line_as_json = ujson.loads(line)
            assert set(line_as_json.keys()) <= KEYS
            if 'html' not in line_as_json:
                instances_without_html += 1
            if 'description' not in line_as_json:
                instances_without_descr += 1
            label_distr[line_as_json['industry']] += 1
            lang_code = detect_language(line_as_json)
            if lang_code not in ['en', 'en-US', 'en-GB']:
                instances_not_in_eng += 1
            progress += 1
            if progress % 100 == 0:
                print 'Progress: {}'.format(progress)
    print instances_without_html
    print instances_without_descr
    print instances_not_in_eng
    print label_distr
    print len(label_distr)
    plot_distr(label_distr)


if __name__ == '__main__':
    get_tags_distr()
