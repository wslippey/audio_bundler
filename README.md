# Audio-Book file bundler

Read book audio files in a target directory and combine into one using ffmpeg.

Files are checked for order and appropriate format.

**Assumes that FFMPEG is installed and available*

Assumes filenames in the format of 
    
    9780739366608_AB_02_011_r1.wav
    <isbn>_<abridged>_<disc>_<track>_t1.wav 


## Installation

* Download package
* cd to directory
* `pip install .`

## Usage

`audio_bundler --help`

    Usage: audio_bundler [OPTIONS] SOURCE_DIRECTORY

    Concatenate a single audio file from a directory of audio book disc tracks

    Options:
      --output-path TEXT  Path for output file
      --help              Show this message and exit.


