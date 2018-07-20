import os
import pytest

from audio_bundler.path_utils import RE_AUDIO_CHAPTER


PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_DIR = os.path.join(PROJECT_DIR, 'test_files')


@pytest.mark.datafiles(os.path.join(TEST_DIR, 'clean'))
def test_re_audio_chapter(datafiles):
    """ Should match against file naming convention"""
    for img in datafiles.listdir():
        match = RE_AUDIO_CHAPTER.match(img.basename)
        assert match is not None

