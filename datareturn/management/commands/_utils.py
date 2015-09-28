import re

from allauth.account.models import EmailAddress
from django.contrib.auth import get_user_model


def is_username_unique(username):
    User = get_user_model()
    try:
        User.objects.get(username__iexact=username)
        return False
    except User.DoesNotExist:
        return True
    return False


def make_unique_username(basename):
    username = basename
    i = 1
    while not is_username_unique(username):
        i += 1
        username = basename + str(i)
    return username


def new_user(email, username=''):
    User = get_user_model()
    if username:
        assert is_username_unique(username)
    else:
        basename = email.split('@')[0]
        username = make_unique_username(basename)
    if User.objects.filter(email=email):
        raise ValueError('Email "{}" not unique.'.format(email))
    user = User(username=username, email=email)
    user.save()

    # Set up email for allauth.
    ea = EmailAddress(user=user, email=email, primary=True, verified=False)
    ea.user = user
    ea.save()

    return user


def email_valid(email):
    if not '@' in email:
        return False
    user_part, domain_part = email.rsplit('@', 1)
    if not re.match(
            r"^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*\Z",
            user_part, re.IGNORECASE):
        return False
    if not re.match(
            r'((?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+)(?:[A-Z0-9-]{2,63}(?<!-))\Z',
            domain_part,
            re.IGNORECASE):
        return False
    return True
