# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='SimpleCrawler',
    version='1.0.0',
    description='Simple web-crawler',
    long_description=readme,
    author='Aurélien Bertail',
    author_email='aurelienbrtail@gmail.com',
    url='',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

