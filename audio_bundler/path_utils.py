import re

from pathlib import Path


# Expected file naming convention for audio chapter files
RE_AUDIO_CHAPTER = re.compile(
    '^(?P<isbn>\d{13,16})_'
    '(?P<abridged>(AB|DA))_'
    '(?P<disc>\d{2})_'
    '(?P<track>\d{3})_r1'
    '\.(?P<ext>(wav|flac))$',
    re.IGNORECASE
)


def get_paths(source_directory, output_directory):
    """
    Verify input and optional output_paths are valid
    :param source_directory: Path to directory containing audio chapter files
    :param output_directory: Export path
    :return:
    """
    source_path = Path(source_directory)
    output_path = Path(output_directory)
    if not all([source_path.is_dir(), output_path.is_dir()]):
        raise ValueError('Issue with source and/or output directory')
    return source_path, output_path


def validate_disc_tracks(disc_dict):
    """
    Light validation of expected dictionary track completed structure.
    The track numbers are part of the filename, so the last track should be
    the same as the total list length.
    :param disc_dict:
    :return:
    """
    tracks = disc_dict['tracks']
    actual_count = len(tracks)
    expected_count = int(tracks[-1])
    if expected_count != actual_count:
        raise ValueError(
            'Disc #{}, appears to be missing tracks. '
            'Expected {}, but gathered {}.'.format(
                disc_dict['num'],
                expected_count,
                actual_count
            )
        )
    return True
