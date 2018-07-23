import re

from pathlib import Path

__all__ = [
    'RE_AUDIO_CHAPTER',
    'get_paths',
    'validate_disc_tracks',

]


# Expected file naming convention for audio chapter files
RE_AUDIO_CHAPTER = re.compile(
    '^(?P<isbn>\d{13,16})_'
    '(?P<abridged>(AB|DA))_'
    '(?P<disc>\d{2})_'
    '(?P<track>\d{3})_r1'
    '\.(?P<ext>(wav|flac))$',
    re.IGNORECASE
)

DISC_DICT = {
    'num': '',
    'tracks': []
}
AUDIO_META = {
    'isbn': '',
    'is_abridged': False,
    'file_paths': [],
    'discs': []
}


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


def merge_audio_files(source_directory, output_directory='.'):
    """
    Merge assumed disc/track directory of audio files into one file, using
    the same format. Uses the first file as a guide and does some light
    validation to ensure that discs and tracks are contiguous.
    :param source_directory:
    :param output_directory:
    :return:
    """
    source_path, output_path = get_paths(
        source_directory, output_directory)
    source_files = list(source_path.iterdir())
    audio_meta = AUDIO_META.copy()

    try:
        init_file = source_files[0]
    except IndexError:
        raise IndexError('Source directory appears to be empty')
    else:
        init_dict = RE_AUDIO_CHAPTER.match(init_file.name)

    # Expecting to use the first file as our start / guide
    if not init_dict:
        raise ValueError(
            'First file in directory: {} does not appear to have the expected '
            'name / format'
        )
    else:
        audio_meta['isbn'] = init_dict['isbn']
        audio_meta['is_abridged'] = init_dict['abridged'].lower() == 'ab'

    current_disc = {}
    for file_path in source_files:
        re_dict = RE_AUDIO_CHAPTER.match(file_path.name)

        # there might be other files, but still valid so continue
        if not re_dict:
            continue

        # Continue gathering tracks for a disc or start a new one
        if current_disc is None or re_dict['disc'] != current_disc.get('num'):
            disc_dict = DISC_DICT.copy()
            disc_dict['num'] = re_dict['disc']
            disc_dict['tracks'].append(re_dict['track'])