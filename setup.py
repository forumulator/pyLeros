#!/usr/bin/env python

from setuptools import setup
from setuptools import find_packages

setup(

    name='pyleros',
    version='0.1.dev0',
    description='pyLeros tiny microprocessor',
    author='Pranjal Agrawal, Martin Schoeberl',
    author_email='forumulator@gmail.com',
    url='https://github.com/forumulator/pyLeros',
    packages=find_packages(),
    install_requires = ['myhdl >= 1.0.dev'],
    classifiers=[
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3',
        ],
)