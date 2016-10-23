import os
import ujson

import click
from sklearn.pipeline import Pipeline

from src.classifier.classifier_transformers import PosSelectorTransformer

# POS tags from NLTK library
ADJECTIVES = ['JJ', 'JJR', 'JJS']
NOUNS = ['NN', 'NNP', 'NNS', 'NNPS']
ADVERBS = ['RB', 'RBR', 'RBS']
VERBS = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']


@click.command()
@click.argument('input-file-path', type=click.Path(exists=True, dir_okay=False))
@click.argument('output-file-path', type=click.Path(exists=False, dir_okay=False))
def run_classification(input_file_path, output_file_path):
    pipeline = Pipeline([
        ('pos_selection', PosSelectorTransformer(NOUNS + VERBS))
    ])
    with open(input_file_path, 'r') as input_file:
        X, y = [], []
        for row in input_file:
            json = ujson.loads(row)
            X.append(json['html'] + json['description'])
            y.append(json['industry'])
    X_transformed = pipeline.transform(X)
    with open(output_file_path, 'w') as output_file:
        for document, industry in zip(X_transformed, y):
            json = ujson.dumps({
                'words': document,
                'label': industry
            })
            output_file.write(json + os.linesep)


if __name__ == '__main__':
    run_classification()
