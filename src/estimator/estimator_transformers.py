import nltk

# TODO estimator pipeline:
# - read as (list of tokens, label)
# - POS tagging transformer
# - list of tokens -> lowercase string
# - countVectorizer with lemmatization / stemming
# - tf-idf
# - SVC


# FIXME
class LematizationTransformer(object):

    def __init__(self):
        self.lemmatizer = nltk.stem.WordNetLemmatizer()

    def _lemmatize_word(self, word):
        return self.lemmatizer.lemmatize(word)

    def _lemmatize_words(self, words):
        return map(self._lemmatize_word, words)

    def transform(self, json):
        return {
            'html': self._lemmatize_words(json['html']),
            'description': self._lemmatize_words(json['description']),
            'industry': json['industry']
        }
