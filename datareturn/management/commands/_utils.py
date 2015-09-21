import re

from allauth.account.models import EmailAddress
from allauth.utils import generate_unique_username
from django.contrib.auth import get_user_model


def new_user(email, first_name='', last_name=''):
    usernamebase = [x for x in [email, first_name, last_name] if x]
    username = generate_unique_username(usernamebase)
    usermodel = get_user_model()
    if usermodel.objects.filter(email=email):
        raise ValueError('Email "{}" not unique.'.format(email))
    user = usermodel(username=username, email=email)
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name
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
