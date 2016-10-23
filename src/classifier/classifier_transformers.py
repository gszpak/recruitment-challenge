import nltk

# TODO classifier pipeline:
# - read as (list of tokens, label)
# - POS tagging transformer
# - list of tokens -> lowercase string
# - countVectorizer with lemmatization / stemming
# - tf-idf
# - SVC
from sklearn.base import BaseEstimator, TransformerMixin


class PosSelectorTransformer(BaseEstimator, TransformerMixin):
    """
    Chooses only given parts of speech (POS) from list of words
    """

    def __init__(self, enabled_pos):
        self.enabled_pos = set(enabled_pos)

    def get_params(self, deep=True):
        return {
            'enabled_pos': self.enabled_pos
        }

    def set_params(self, **kwargs):
        for param_name, param_val in kwargs:
            setattr(self, param_name, param_val)
        return self

    def fit(self, X, y=None):
        return self

    def _filter_list_of_words(self, words):
        words = list(map(lambda s: s.lower(), words))
        pos_tagged_words = nltk.pos_tag(words)
        result = []
        for word, tag in pos_tagged_words:
            if tag in self.enabled_pos:
                result.append(word)
        return result

    def transform(self, X):
        print('{} start'.format(self.__class__.__name__))
        result = []
        for i, words in enumerate(X):
            result.append(self._filter_list_of_words(words))
            if i % 100 == 0:
                print('Progress: {}'.format(i))
        return result
