Random python utility libraries.

[![CircleCI](https://circleci.com/gh/daniyalzade/utensils.svg?style=svg)](https://circleci.com/gh/daniyalzade/utensils)

# Requirements

* **Python**: 3.*

# Installation

Install using pip:

```sh
pip install utensils
```

# Testing

Use `tox` for testing.

```sh
tox
```

# Usage

Safe accessors for Python dictionaries

```py
from utensils.dictutils import get_dotted
from utensils.dictutils import set_dotted

foo = {
    'test': [1, 2, 3]
}

set_dotted(foo, 'bar.dar', 5)

print(get_dotted(foo, 'bar.dar') == 5)
print(get_dotted(foo, 'test[2]') == 3)
```

# Contribution

* Make sure that the tests are passing before opening up the PR
* Create a PR for feature enhancements
* Once a PR is merged, update version with the following commands:

```
bumpversion patch
git push origin master --tags
```

# Packaging

`tox` creates a package in `.tox/dist`. Use twine to upload it to pypi:

```sh
twine upload .tox/dist/utensils-*.zip
```
