from allauth.account.utils import user_pk_to_url_str

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.core.management.base import BaseCommand, CommandError
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string

from datareturn.models import SiteConfig

User = get_user_model()


class Command(BaseCommand):
    help = 'Send invites to a list of emails.'

    def add_arguments(self, parser):
        parser.add_argument('-e', '--emails',
                            dest='emails',
                            nargs='*',
                            required=True,
                            help='the email list file')

    def handle(self, *args, **options):
        users = []

        for email in options['emails']:
            user_match = User.objects.filter(email=email)
            if user_match and len(user_match) == 1:
                users.append(user_match[0])
            else:
                continue

        messages = []
        for user in users:
            token = default_token_generator.make_token(user)
            login_path = reverse('token_login',
                                 kwargs={'uidb36': user_pk_to_url_str(user),
                                         'token': token})

            current_site = Site.objects.get_current()
            site_config = SiteConfig.objects.get(site=current_site)
            login_url = 'https://{}{}'.format(current_site.domain, login_path)
            subject = ('Your {} data: Download or share with '
                       'Open Humans!'.format(current_site.name))
            if site_config.invite_email_subject:
                subject = site_config.invite_email_subject
            context = {'login_url': login_url, 'site': current_site }
            content = render_to_string('datareturn/email/invite.txt', context)
            send_mail(subject, content, settings.DEFAULT_FROM_EMAIL, [user.email])
