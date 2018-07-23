import re

from pathlib import Path

__all__ = [
    'RE_AUDIO_CHAPTER',
    'get_paths',
    'validate_disc_tracks',
    'get_audio_file_dict',
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

AUDIO_META = {
    'isbn': None,
    'is_abridged': False,
    'file_paths': [],
    'discs': [],
    'file_type': None
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


def get_audio_file_dict(source_path):
    """
    Build dict for use in merging audio book files
    :param source_path: path containing the source files
    :return:
    """
    source_files = sorted(list(Path(source_path).iterdir()))
    audio_meta = AUDIO_META.copy()

    if len(source_files) == 0:
        raise IndexError('Source directory appears to be empty')

    current_disc = None
    for file_path in source_files:
        re_dict = RE_AUDIO_CHAPTER.match(file_path.name)

        # there might be other files, but still valid so continue
        if not re_dict:
            continue
        else:
            audio_meta['file_paths'].append(file_path.as_uri())

        if audio_meta['isbn'] is None:
            audio_meta.update({
                'isbn': re_dict['isbn'],
                'is_abridged': re_dict['abridged'].lower() == 'ab',
                'file_type': re_dict['ext']
            })

        # Continue gathering tracks for a disc or start a new one
        if current_disc is None or re_dict['disc'] != current_disc['num']:
            current_disc = {
                'num': re_dict['disc'],
                'tracks': []
            }
            current_disc['tracks'].append(re_dict['track'])
            audio_meta['discs'].append(current_disc)
        else:
            current_disc['tracks'].append(re_dict['track'])

    return audio_meta
