import os
import random
import pprint

from pathlib import Path


TEST_DIR = os.path.dirname(os.path.abspath(__file__))


def generate_test_audio_files(
        test_file_dir,
        isbn,
        is_abridged=True,
        ext='wav',
        disc_limit=10,
        missing_discs=False,
        track_limit=5,
        missing_tracks=False,
        random_tracks=True,
        dry_run=False
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
    :param random_tracks: randomize number of tracks per disc
    :param dry_run: only print file names, don't generate
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

    track_names = []
    for d in range(1, disc_limit + 1):
        disc_num = '{:0>2d}'.format(d)
        track_range = range(1, track_limit + 1)
        if random_tracks:
            track_range = range(1, random.choice(track_range) + 1)

        for t in track_range:
            track_num = '{:0>3d}'.format(t)
            file_name = base_file_name.format(disc_num, track_num)
            track_names.append(file_name)

            if not dry_run:
                Path(target_directory, file_name).touch()
            else:
                print('{}/{}'.format(target_directory.name, file_name))

    return track_names


if __name__ == '__main__':

    results = generate_test_audio_files(
        'clean',
        '9780739366608',
        dry_run=True
    )

