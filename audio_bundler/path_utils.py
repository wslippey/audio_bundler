import re

from pathlib import Path


# Expected file naming convention for audio chapter files
RE_AUDIO_CHAPTER = re.compile(
    '^(?P<isbn>\d{13,16})_'
    '(?P<abridged>(AB|DA))_'
    '(?P<disc>\d{2})_'
    '(?P<track>\d{3})_r'
    '\.(?P<ext>\d+)$'
)


def check_in_out_paths(input_path, output_path='.'):
    """
    Verify input and optional output_paths are valid
    :param input_path: Path to directory containing audio chapter files
    :param output_path:
    :return:
    """
    pass
