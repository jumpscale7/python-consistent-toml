# Consistent TOML for Python

[![Build Status](https://travis-ci.org/Jumpscale/python-consistent-toml.svg?branch=master)](https://travis-ci.org/Jumpscale/python-consistent-toml)
[![Python Versions](https://img.shields.io/pypi/pyversions/contoml.svg)](https://pypi.python.org/pypi/contoml)
[![Release](https://img.shields.io/pypi/v/contoml.svg)](https://pypi.python.org/pypi/contoml)
![Wheel](https://img.shields.io/pypi/wheel/contoml.svg)
[![Join the chat at https://gitter.im/Jumpscale/python-consistent-toml](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/Jumpscale/python-consistent-toml?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)


A Python module for updating data within [TOML](https://github.com/toml-lang/toml) files without messing up their nice formating. This is achieved by preserving the parsed/constructed TOML data structures as lexical tokens internally and having the data manipulations performed directly on the tokens.

## Installation ##
```bash
pip install --upgrade contoml
```

## Usage ##

```python
>>> import contoml

>>> toml_file = contoml.load('sample.toml')

# The anonymous table is accessible using the empty string key on the TOML file
>>> toml_file['']['title']
'TOML Example'

# You can modify table values in-place
>>> toml_file['fruit'][1]['variety'][0]['points'][0]['y'] = 42
>>> toml_file['servers']['alpha']['ip'] = '192.168.0.111'
>>> toml_file['environment'] = {'OS': 'Arch Linux', 'Type': 'GNU/Linux'}
```
