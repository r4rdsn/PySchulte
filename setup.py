from setuptools import setup, find_packages

from PySchulte import __version__
from os.path import abspath, dirname, join

with open(join(abspath(dirname(__file__)), 'README.md')) as file:
    long_description = file.read()

setup(
    name='PySchulte',
    version=__version__,
    description='Schulte table implementation on Python using Kivy framework.',
    long_description=long_description,
    url='https://github.com/r4rdsn/PySchulte',
    author='alfred richardsn',
    author_email='rchrdsn@protonmail.ch',
    license='GPLv3',
    classifiers=[
        'Intended Audience :: Healthcare Industry',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ],
    keywords='schulte table reading attention vision training health',
    packages=find_packages(),
    install_requires=['Kivy', 'KivyCalendar', 'tinydb'],
    entry_points={
        'console_scripts': [
            'pyschulte=PySchulte.schulte:main',
        ],
    }
)
