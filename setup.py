from setuptools import setup, find_packages
import importlib

setup(
    name='contoml',
    packages=find_packages(),
    version=importlib.import_module('contoml._version').VERSION,
    description='Consistent TOML for Python',
    author='Amr Hassan',
    author_email='amr.hassan@gmail.com',
    url='https://github.com/Jumpscale/python-consistent-toml',
    keywords=['toml'],
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5'
    ],
    install_requires=[
        'six',
        'strict_rfc3339',
        'iso8601',
        'pytz',
        'timestamp'
    ]
)
