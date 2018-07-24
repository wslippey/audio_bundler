from setuptools import setup


with open('requirements.txt') as req:
    requirements = req.read().splitlines()


setup(
    version='0.1',
    name='audio_bundler',
    py_modules=['cmd'],
    install_requires=requirements,
    entry_points='''
        [console_scripts]
        audio_bundler=cmd:cli
    ''',
    description='Bundle audiobook chapter files into one file',
    packages=['audio_bundler']
)
