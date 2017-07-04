"""
Tackling Cancer app for biopsy image classification on Bluemix
"""

from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='Tackling Cancer',
    description='Tackling Cancer app for biopsy image classification on Bluemix',
    long_description=long_description,
    license='Apache-2.0',
    packages=['tackling_cancer'],
    include_package_data=True,
    install_requires=[
        'flask',
        'watson_developer_cloud',
        'setuptools',
        'opencv_python',
        'numpy',
        'Werkzeug',
        'matplotlib',
        'mpld3',
        'pathlib',
        'Pillow',
        'scikit_learn',
    ], 
)