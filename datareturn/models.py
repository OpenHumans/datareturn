import datetime

from django.conf import settings
from django.contrib.sites.models import Site
from django.db import models
from django.utils import timezone
from django.utils.deconstruct import deconstructible

import requests

from storages.backends.s3boto import S3BotoStorage

User = settings.AUTH_USER_MODEL


@deconstructible
class MyS3BotoStorage(S3BotoStorage):
    pass


class DataFile(models.Model):
    user = models.ForeignKey(User)
    datafile = models.FileField(
        storage=MyS3BotoStorage(acl='private',
                                querystring_auth=True,
                                querystring_expire=600))
    description = models.TextField(default='')

    def __unicode__(self):
        return ':'.join([self.user.email, self.datafile.name])


class DataLink(models.Model):
    user = models.ForeignKey(User)
    url = models.TextField(default='')
    name = models.TextField(default='')
    description = models.TextField(default='')

    def __unicode__(self):
        return ':'.join([self.user.email, self.name])


class SiteConfig(models.Model):
    """
    Site configuration, customize with additional information and descriptions.
    """
    site = models.OneToOneField(Site)
    source_name = models.CharField(max_length=40)
    data_page_explanation = models.TextField(default='')


class OpenHumansConfig(models.Model):
    """
    Site configuration for data export to Open Humans. Only one should exist.
    """
    site = models.OneToOneField(Site)
    client_id = models.CharField(max_length=255)
    client_secret = models.CharField(max_length=255)
    source_name = models.CharField(max_length=255)

    token_url = settings.OPEN_HUMANS_SERVER + '/oauth/token/'

    @property
    def redirect_uri(self):
        return self.site.domain + '/open_humans_complete'

    @property
    def auth_url(self):
        return (settings.OPEN_HUMANS_SERVER +
                '/oauth2/authorize?client_id={}&response_type=code'.format(
                    self.client_id))

    @property
    def return_url(self):
        return_url = '{}/study/{}/return/'.format(
            settings.OPEN_HUMANS_SERVER, self.source_name
        )
        return return_url


class OpenHumansUser(models.Model):
    """
    Handle data for a user's Open Humans account connection.
    """
    user = models.OneToOneField(User)
    openhumans_userid = models.PositiveIntegerField(null=True)
    access_token = models.CharField(max_length=60, blank=True)
    refresh_token = models.CharField(max_length=60, blank=True)
    token_expiration = models.DateTimeField(null=True)

    def _refresh_tokens(self):
        site = Site.objects.get_current()
        response_refresh = requests.post(
            site.openhumansconfig.token_url,
            data={
                'grant_type': 'refresh_token',
                'refresh_token': self.refresh_token},
            auth=requests.auth.HTTPBasicAuth(
                site.openhumansconfig.client_id,
                site.openhumansconfig.client_secret
            )
        )
        token_data = response_refresh.json()
        self.access_token = token_data['access_token']
        self.refresh_token = token_data['refresh_token']
        self.token_expiration = (timezone.now() +
                                 datetime.timedelta(
                                     seconds=token_data['expires_in']))
        self.save()

    def _token_expired(self, offset=0):
        """
        True if token expired (or expires in offset seconds), otherwise False.
        """
        offset_expiration = (
            self.token_expiration - timezone.timedelta(seconds=offset))
        if timezone.now() >= offset_expiration:
            return True
        return False

    def get_access_token(self, offset=30):
        """
        Return access token fresh for at least offset seconds (default 30).
        """
        if self._token_expired(offset=30):
            self._refresh_tokens()
        return self.access_token

    def __unicode__(self):
        return '{} OpenHumans:{}'.format(self.user.email, self.openhumans_userid)
