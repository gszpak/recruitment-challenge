import click


SKIPPED_TAGS = ['img', 'form', 'input', 'br', 'button']


@click.command()
@click.argument('input-file-path', type=click.Path(exists=True, dir_okay=False))
def extract_text_from_html(input_file_path):
    pass