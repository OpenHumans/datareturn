import re

from django import template

register = template.Library()


def reset_to_login_url(url):
    """Replaces password reset url with token login url"""
    print url
    url_parts = re.match(r'(https?://[^/]+/).*?/key/(.*)$', url).groups()
    return url_parts[0] + 'token_login/' + url_parts[1]


register.filter('reset_to_login_url', reset_to_login_url)
