from django.conf import settings
from django.db import models
from django.utils.deconstruct import deconstructible

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

    def __unicode__(self):
        return self.datafile.name
