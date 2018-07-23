import os
import pytest

from pathlib import Path

from audio_bundler.path_utils import RE_AUDIO_CHAPTER, check_paths


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
    source, output = check_paths(source_directory, output_directory)
    assert source == Path(source_directory)
    assert output == Path(output_directory)


def test_check_paths_invalid():
    source_directory = '/opt/invalid'
    output_directory = TEST_DIR
    with pytest.raises(ValueError):
        check_paths(source_directory, output_directory)
