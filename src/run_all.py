import click

from src.classifier.run_classification import run_classification
from src.json_transformer.run_transform_jsons import run_transform_jsons


@click.command()
@click.argument('input-file-path', type=click.Path(exists=True, dir_okay=False))
@click.argument('transformed-jsons-file-path', type=click.Path(exists=False, dir_okay=False))
def main(input_file_path, transformed_jsons_file_path):
    run_transform_jsons(input_file_path, transformed_jsons_file_path)
    run_classification(transformed_jsons_file_path)


if __name__ == '__main__':
    main()
