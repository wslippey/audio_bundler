from . import path_utils


DISC_DICT = {
    'num': '',
    'tracks': []
}


AUDIO_META = {
    'isbn': '',
    'is_abridged': None,
    'file_paths': [],
    'discs': []
}


def merge_audio_files(source_directory, output_directory='.'):
    """
    Merge assumed disc/track directory of audio files into one file, using
    the same format. Uses the first file as a guide and does some light
    validation to ensure that discs and tracks are contiguous.
    :param source_directory:
    :param output_directory:
    :return:
    """
    source_path, output_path = path_utils.get_paths(
        source_directory, output_directory)
    source_files = list(source_path.iterdir())
    audio_meta = AUDIO_META.copy()

    try:
        init_file = source_files[0]
    except IndexError:
        raise IndexError('Source directory appears to be empty')
    else:
        init_dict = path_utils.RE_AUDIO_CHAPTER.match(init_file.basename)

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
        re_dict = path_utils.RE_AUDIO_CHAPTER.match(file_path.basename)

        # there might be other files, but still valid so continue
        if not re_dict:
            continue

        # Continue gathering tracks for a disc or start a new one
        if current_disc is None or re_dict['disc'] != current_disc.get('num'):
            disc_dict = DISC_DICT.copy()
            disc_dict['num'] = re_dict['disc']
            disc_dict['tracks'].append(re_dict['track'])
