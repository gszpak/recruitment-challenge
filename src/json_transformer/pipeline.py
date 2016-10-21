
class JsonTransformerPipeline(object):

    def __init__(self, *transformers):
        self.transfomers = transformers

    def transform(self, json):
        current_json = json
        for transformer in self.transfomers:
            current_json = transformer.transform(current_json)
        return current_json
