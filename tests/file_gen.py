import os

from pathlib import Path


TEST_DIR = os.path.dirname(os.path.abspath(__file__))


def generate_test_audio_files(
        test_file_dir,
        isbn,
        is_abridged=True,
        ext='wav',
        disc_limit=10,
        missing_discs=False,
        track_limit=(),
        missing_tracks=False
):
    """
    Create test audio files for cd audio books
    :param test_file_dir: target directory under ./test_files
    :param isbn: string
    :param is_abridged: switch between codes AB|DA
    :param ext: file extension
    :param disc_limit: maximum discs to produce
    :param missing_discs: set to True to create missing discs
    :param track_limit: maximum track per disc
    :param missing_tracks: set to True to create missing tracks in a disc
    :return:
    """
    target_directory = Path(TEST_DIR, 'test_files', test_file_dir)
    if not target_directory.is_dir():
        raise Exception('Test files directory: {} does not exist'.format(
            target_directory))

    base_file_name = '{isbn}_{is_abridged}_{{}}_{{}}_r1.{ext}'.format(
        isbn=isbn,
        is_abridged='AB' if is_abridged else 'DA',
        ext=ext,
    )
    return base_file_name


if __name__ == '__main__':
    results = generate_test_audio_files(
        'clean',
        '9780739366608'
    )
    print(results)
