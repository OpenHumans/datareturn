import os

from django import template

register = template.Library()


def basename(path):
    """Returns basename in path"""
    return os.path.basename(path)


register.filter('basename', basename)
