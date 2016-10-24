import nltk

from sklearn.base import BaseEstimator, TransformerMixin


class PosSelectorTransformer(BaseEstimator, TransformerMixin):
    """
    Chooses only given parts of speech (POS) from list of words
    """

    def __init__(self, enabled_pos=None):
        if enabled_pos is None:
            self.enabled_pos = set()
        else:
            self.enabled_pos = set(enabled_pos)

    def get_params(self, deep=True):
        return {
            'enabled_pos': self.enabled_pos
        }

    def set_params(self, **kwargs):
        for param_name, param_val in kwargs.items():
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
        return ' '.join(result)

    def transform(self, X):
        return [self._filter_list_of_words(words) for words in X]


class LemmaTokenizer(object):

    def __init__(self):
        self.lemmatizer = nltk.stem.WordNetLemmatizer()

    def __call__(self, doc):
        return [self.lemmatizer.lemmatize(word) for word in nltk.word_tokenize(doc)]
