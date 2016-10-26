import ujson

import click
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline

from src.classifier.classifier_transformers import PosSelectorTransformer, LemmaTokenizer

# POS tags from NLTK library
ADJECTIVES = ['JJ', 'JJR', 'JJS']
NOUNS = ['NN', 'NNP', 'NNS', 'NNPS']
ADVERBS = ['RB', 'RBR', 'RBS']
VERBS = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']


def _read_x_y(input_file_path):
    X, y = [], []
    with open(input_file_path, 'r') as input_file:
        for row in input_file:
            json = ujson.loads(row)
            X.append(json['html'] + json['description'])
            y.append(json['industry'])
    return X, y


def run_classification(input_file_path):
    pipeline = Pipeline([
        ('pos_selection', PosSelectorTransformer()),
        # Words were lowercased in PosSelectorTransformer
        ('vectorization', CountVectorizer(tokenizer=LemmaTokenizer(), lowercase=False)),
        ('tfidf', TfidfTransformer()),
        ('svm', SGDClassifier(loss='hinge', penalty='l2'))
    ])
    # This would be a parameter grid to search, but it takes a lot of time to build a model
    param_grid = [
        {
            'pos_selection__enabled_pos': [(NOUNS + VERBS), (NOUNS + VERBS + ADJECTIVES + ADVERBS)],
            'tfidf__use_idf': [True, False],
            'svm__alpha': [0.1, 0.01, 0.001, 0.0001, 0.00001, 0.000001],
            'svm__n_iter': [5, 10, 15],
        },
        {
            'pos_selection__enabled_pos': [(NOUNS + VERBS), (NOUNS + VERBS + ADJECTIVES + ADVERBS)],
            'tfidf__use_idf': [True, False],
            'svm__alpha': [0.1, 0.01, 0.001, 0.0001, 0.00001, 0.000001],
            'svm__n_iter': [5, 10, 15],
            'svm__learning_rate': ['constant', 'invscaling'],
            'svm__eta0': [0.5, 0.1, 0.05, 0.01],
            'svm__power_t': [0.5, 0.1, 0.05, 0.01]
        },
    ]
    grid_search = GridSearchCV(
        pipeline,
        param_grid={
            'pos_selection__enabled_pos': [(NOUNS + VERBS)],
            'tfidf__use_idf': [True],
            'svm__alpha': [0.0001]
        },
        cv=3,
        verbose=10,
        n_jobs=-1
    )
    X, y = _read_x_y(input_file_path)
    grid_search.fit(X, y)
    print('CV accuracy: {}'.format(grid_search.best_score_))


@click.command()
@click.argument('input-file-path', type=click.Path(exists=True, dir_okay=False))
def main(input_file_path):
    run_classification(input_file_path)


if __name__ == '__main__':
    main()

