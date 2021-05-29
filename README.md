# flake8_loopy
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/) ![GitHub](https://img.shields.io/github/license/bdscharf/flake8_loopy)

basic code quality checks in loops

## checks
| error code      | description |
| ----------- | ----------- |
| LPY100      | unused variable created by ```enumerate()```: you probably do not need ```enumerate()```, or you should use ```range(len())``` instead      |

## todo
1) check for duplicated variable name in inner loop(s)

2) iteration with index where index is only used to get an item (should iterate directly over items)


## notes
this plugin is currently mostly untested and should be considered experimental. please report false positives / errors if found!
