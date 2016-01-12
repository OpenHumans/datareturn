# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datareturn', '0008_siteconfig_invite_email_postscript'),
    ]

    operations = [
        migrations.AddField(
            model_name='siteconfig',
            name='home_page_summary',
            field=models.TextField(default=b'', blank=True),
        ),
    ]
