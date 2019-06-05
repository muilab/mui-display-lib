# -*- coding: utf-8 -*-

from distutils.core import setup
from setuptools import find_packages
from Cython.Distutils import build_ext
from Cython.Build import cythonize

with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='mui_ui',
    version='0.1.1',
    description='UI Library for mui',
    long_description=readme,
    author='Takuya Kubota',
    author_email='kubota@muilab.com',
    install_requires=['crc8','pyserial','Pillow','numpy','evdev', 'RPi.GPIO'],
    url='https://github.com/muilab/mui-display-lib',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    package_dir={'mui_ui':'mui_ui'},
    package_data={'mui_ui':['assets/*']},
    ext_modules=cythonize("./mui_ui/matrix.pyx")
)