from setuptools import setup, find_packages
from io import open
from os import path
import pathlib

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# automatically captured required modules for install_requires in requirements.txt and as well as configure dependency links
with open(path.join(HERE, 'requirements.txt'), encoding='utf-8') as f:
    all_reqs = f.read().split('\n')

install_requires = [x.strip() for x in all_reqs if ('git+' not in x) and (not x.startswith('#')) and (not x.startswith('-'))]
dependency_links = [x.strip().replace('git+', '') for x in all_reqs if 'git+' not in x]

setup(
    name="clipbit",
    description="Generate concise meaningful summaries YouTube videos",
    version="1.0.0",
    packages=find_packages(),
    install_requires = install_requires,
    entry_points='''
        [console_scripts]
        clipbit=clipbit.__main__:main
    ''',
    author="Sarthak Khattar <sarthakoct@gmail.com>, Miguel Guardia <guardia@ualberta.ca>, Kimaru Thagana <thagana44@gmail.com>",
    keywords="nlp, youtube, cli, captions",
    long_description=README,
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/MLH-Fellowship/ClipBit",
    download_url="https://github.com/MLH-Fellowship/ClipBit/archive/v1.0.tar.gz",
    dependency_links=dependency_links,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        "License :: OSI Approved :: MIT License",
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ]
)
