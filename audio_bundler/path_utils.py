import re

from pathlib import Path

__all__ = [
    'RE_AUDIO_CHAPTER',
    'get_paths',
    'validate_disc_tracks',
    'validate_audio_tracks',
    'get_audio_file_dict',
]


# Expected file naming convention for audio chapter files
RE_AUDIO_CHAPTER = re.compile(
    '^(?P<isbn>\d{13,16})_'
    '(?P<abridged>(AB|DA))_'
    '(?P<disc>\d{2})_'
    '(?P<track>\d{3})_r1'
    '\.(?P<file_type>(wav|flac))$',
    re.IGNORECASE
)

AUDIO_META = {
    'isbn': None,
    'abridged_code': '',
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
        raise ValueError('Source and/or output directory is invalid')
    return source_path, output_path


def validate_disc_tracks(disc_dict):
    """
    Validate that a disc's track numbers are contiguous
    :param disc_dict:
    :return:
    """
    tracks = disc_dict['tracks']
    track_num = 1

    for track in tracks:
        if track_num != int(track):
            raise ValueError(
                'Disc #{} is missing track #{:0>3d}'.format(
                    disc_dict['num'],
                    track_num
                )
            )
        track_num += 1
    return True


def validate_audio_tracks(audio_dict):
    """
    Test that disc numbers are contiguous and their tracks
    :param audio_dict:
    :return:
    """
    disc_num = 1
    for disc_dict in audio_dict['discs']:
        if disc_num != int(disc_dict['num']):
            raise ValueError(
                'Disc #{:0>2d} appears to be missing'.format(disc_num))
        validate_disc_tracks(disc_dict)
        disc_num += 1
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

        if not re_dict:
            continue

        # Initial values
        if audio_meta['isbn'] is None:
            audio_meta.update({
                'isbn': re_dict['isbn'],
                'abridged_code': re_dict['abridged'],
                'is_abridged': re_dict['abridged'].lower() == 'ab',
                'file_type': re_dict['file_type']
            })
        elif not all([audio_meta[k] == re_dict[k] for k in ('isbn', 'file_type')]):
            # Constrain to the same file type for now
            continue
        else:
            audio_meta['file_paths'].append(str(file_path))

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

    if audio_meta['isbn'] is None:
        raise ValueError('No files matched name / extension criteria')

    return audio_meta
