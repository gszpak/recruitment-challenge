import click


SKIPPED_TAGS = [
    'area', 'audio', 'br', 'button', 'canvas',
    'code', 'fieldset', 'form', 'img', 'input',
    'keygen', 'map', 'meter', 'noscript',
    'object', 'output', 'param', 'progress',
    'script', 'source', 'style', 'textarea',
    'time', 'track', 'video', 'wbr'
]


@click.command()
@click.argument('input-file-path', type=click.Path(exists=True, dir_okay=False))
def extract_text_from_html(input_file_path):
    pass