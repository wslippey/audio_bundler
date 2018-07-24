import click
import ffmpeg

from .path_utils import *


@click.command()
@click.argument('source_directory')
@click.option('--output-path', default='.', help='Path for output file')
def cli(source_directory, output_path):
    """
    Concatenate a single audio file from a directory of audio book disc tracks
    """
    try:
        source, output = get_paths(source_directory, output_path)
    except ValueError as e:
        click.echo('Exception: {}'.format(e))
        raise click.Abort()

    audio_dict = get_audio_file_dict(source)
    output_filename = '{isbn}_{abridged_code}_r1_full.{file_type}'.format(
        **audio_dict)
    output_path = output.joinpath(output_filename)
    out, err = (
        ffmpeg
        .concat(*(ffmpeg.input(f) for f in audio_dict['file_paths']))
        .output(str(output_path))
        .run()
    )

    if err:
        click.echo(err)
        raise click.Abort()

    click.echo(out)
