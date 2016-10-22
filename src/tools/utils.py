import ujson

import numpy as np
from matplotlib import pyplot as plot


def get_html_from_str(line):
    parsed_line = ujson.loads(line)
    return parsed_line.get('html')


def traverse_tree(tree_node, fun_on_node, *fun_args, **fun_kwargs):
    fun_on_node(tree_node, *fun_args, **fun_kwargs)
    for child in tree_node.children:
        traverse_tree(child, fun_on_node, *fun_args, **fun_kwargs)


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
