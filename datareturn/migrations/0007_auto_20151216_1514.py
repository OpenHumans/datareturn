# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datareturn.models


class Migration(migrations.Migration):

    dependencies = [
        ('datareturn', '0006_auto_20151210_1526'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datafile',
            name='datafile',
            field=models.FileField(storage=datareturn.models.MyS3BotoStorage(querystring_expire=239200, querystring_auth=True, acl=b'private'), upload_to=b''),
        ),
    ]
