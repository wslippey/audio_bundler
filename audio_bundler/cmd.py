import click
import ffmpeg

from .path_utils import *


@click.command()
@click.argument('source_directory')
@click.option('--output-path', default='.', help='Path for output file')
def cli(source_directory, output_path):
    """
    Concatenate a single audio file from a directory of audio book disc tracks.
    If successful, outputs the combined file with a similar name convention as
    the ones found in the source directory.

    e.g. 9780739366608_AB_02_011_r1.wav -> 9780739366608_AB_r1_full.wav
    """
    try:
        source, output = get_paths(source_directory, output_path)
    except ValueError as e:
        click.echo('Exception: {}'.format(e))
        raise click.Abort()

    try:
        audio_dict = get_audio_file_dict(source)
        validate_audio_tracks(audio_dict)
    except (IndexError, ValueError) as e:
        click.echo('Exception: {}'.format(e))
        raise click.Abort()

    output_filename = '{isbn}_{abridged_code}_r1_full.{file_type}'.format(
        **audio_dict)
    output_path = output.joinpath(output_filename)

    # Kick off ffmpeg work stream
    out, err = (
        ffmpeg
        .concat(*(ffmpeg.input(f) for f in audio_dict['file_paths']), v=0, a=1)
        .output(output_path.as_posix())
        .overwrite_output()
        .run()
    )

    if err:
        click.echo(err)
        raise click.Abort()

    click.echo('File written to: {}'.format(output_path.as_posix()))
