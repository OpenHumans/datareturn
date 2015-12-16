# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datareturn', '0007_auto_20151216_1514'),
    ]

    operations = [
        migrations.AddField(
            model_name='siteconfig',
            name='invite_email_postscript',
            field=models.TextField(default=b'', blank=True),
        ),
    ]
