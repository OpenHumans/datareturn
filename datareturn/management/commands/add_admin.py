from django.core.management.base import BaseCommand, CommandError

from _utils import email_valid, new_user


class Command(BaseCommand):
    help = 'Create an admin user for an email address.'

    def add_arguments(self, parser):
        parser.add_argument('email', type=str)
        parser.add_argument('password', type=str)

    def handle(self, *args, **options):
        # Check email.
        if not email_valid(options['email']):
            raise ValueError(
                '"{}" doesn\'t appear to be a valid email.'.format(
                    options['email']))

        # Create user.
        email = options['email']
        user = new_user(email=email)
        user.set_password(options['password'])
        user.is_staff = True
        user.save()
