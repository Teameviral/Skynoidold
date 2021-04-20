import pip
from typing import List

with open('requirements.txt') as f:
    packages = f.read().splitlines()
    f.close()


def install(
    package: List,
):
    for pack in package:
        if hasattr(pip, 'main'):
            pip.main(['install', pack])
        else:
            pip._internal.main(['install', pack])


if __name__ == '__main__':
    install(packages)
