import os
import ujson

import click

from src.json_transformer.pipeline import JsonTransformerPipeline
from src.json_transformer.json_transformers import HtmlJsonTransformer, TranslatorTransformer, TokenizerTransformer, \
    NonWordsEliminatorTransformer, UnidecodeTransformer, StripNonAlphanumericTransformer


def run_transform_jsons(input_file_path, output_file_path):
    pipeline = JsonTransformerPipeline(
        HtmlJsonTransformer(),
        # TranslatorTransformer(),
        UnidecodeTransformer(),
        TokenizerTransformer(),
        StripNonAlphanumericTransformer(),
        NonWordsEliminatorTransformer(),
    )
    with open(input_file_path, 'r') as input_file, open(output_file_path, 'w') as output_file:
        progress = 0
        for row in input_file:
            json = ujson.loads(row)
            result_json = pipeline.transform(json)
            line = ujson.dumps(result_json) + os.linesep
            output_file.write(line)
            progress += 1
            print('Progress: {}'.format(progress))

@click.command()
@click.argument('input-file-path', type=click.Path(exists=True, dir_okay=False))
@click.argument('output-file-path', type=click.Path(exists=False, dir_okay=False))
def main(input_file_path, output_file_path):
    run_transform_jsons(input_file_path, output_file_path)


if __name__ == '__main__':
    main()
