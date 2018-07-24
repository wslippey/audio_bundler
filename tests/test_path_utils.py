import os
import pytest

from pathlib import Path

from audio_bundler.path_utils import *


PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_DIR = os.path.join(PROJECT_DIR, 'test_files')


@pytest.mark.datafiles(os.path.join(TEST_DIR, 'clean'))
def test_re_audio_chapter_clean(datafiles):
    """ Should match against file naming convention"""
    for img in datafiles.listdir():
        match = RE_AUDIO_CHAPTER.match(img.basename)
        assert match is not None


def test_check_paths_valid():
    source_directory = os.path.join(TEST_DIR, 'clean')
    output_directory = TEST_DIR
    source, output = get_paths(source_directory, output_directory)
    assert source == Path(source_directory)
    assert output == Path(output_directory)


def test_check_paths_invalid():
    source_directory = '/opt/invalid'
    output_directory = TEST_DIR
    with pytest.raises(ValueError):
        get_paths(source_directory, output_directory)


def test_clean_audio_file_dict():
    d = get_audio_file_dict(os.path.join(TEST_DIR, 'clean'))
    assert d['isbn'] == '9780739366608'
    assert d['is_abridged'] is True
    assert len(d['file_paths'])
    assert validate_audio_tracks(d) is True


def test_invalid_audio_file_dict():
    """
    Should still gather anything that appears valid according to RE as long
    as it matches the isbn and file extension
    """
    d = get_audio_file_dict(os.path.join(TEST_DIR, 'invalid_types'))
    assert d['isbn'] == '9780739366608'
    assert d['is_abridged'] is True
    assert len(d['file_paths'])
    for path in d['file_paths']:
        for ext in ('.flac', '.txt'):
            assert ext not in path
    with pytest.raises(ValueError):
        validate_audio_tracks(d)

