from configparser import ConfigParser
from os import environ

config = ConfigParser()
config.read('config.ini')


def get_var(name, default=None):
    ENV = bool(environ.get('ENV', False))
    if ENV:
        return environ.get(name, default)

    try:
        return config.get('skynoid', name)
    except AttributeError:
        return None
