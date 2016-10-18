import ujson

import numpy as np
from bs4 import BeautifulSoup
import langdetect
from langdetect.lang_detect_exception import LangDetectException
from matplotlib import pyplot as plot


def get_html_from_str(line):
    parsed_line = ujson.loads(line)
    return parsed_line.get('html')


def traverse_tree(tree_node, fun_on_node, *fun_args, **fun_kwargs):
    fun_on_node(tree_node, *fun_args, **fun_kwargs)
    for child in tree_node.children:
        traverse_tree(child, fun_on_node, *fun_args, **fun_kwargs)


def detect_language(instance_as_json):
    assert 'html' in instance_as_json or 'description' in instance_as_json
    if 'html' in instance_as_json:
        html_tree = BeautifulSoup(instance_as_json['html'], 'html.parser')
        for descendant in html_tree.descendants:
            if descendant.name == 'html':
                if descendant.has_attr('lang'):
                    return descendant.get('lang')
                else:
                    break
    try:
        if 'description' in instance_as_json:
            return langdetect.detect(instance_as_json['description'])
    except LangDetectException:
        print instance_as_json['description']
    return 'en'


def plot_distr(tags_distr):
    most_common = tags_distr.most_common(100)
    tags_distr_labels, tags_distr_values = zip(*most_common)
    X = np.arange(len(tags_distr_labels))
    plot.bar(X, tags_distr_values)
    plot.axes().set_xticks(X)
    plot.axes().set_xticklabels(tags_distr_labels, rotation=90)
    ymax = max(tags_distr_values) + 1
    plot.ylim(0, ymax)
    plot.show()