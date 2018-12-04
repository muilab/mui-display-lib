# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='mui_ui',
    version='0.0.1',
    description='UI Library for mui',
    long_description=readme,
    author='Takuya Kubota',
    author_email='kubota@muilab.com',
    install_requires=['crc8','pyserial','Pillow','numpy','evdev'],
    url='https://github.com/muilab/mui-display-lib',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

