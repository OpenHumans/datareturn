# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datareturn', '0002_auto_20151105_2219'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='siteconfig',
            name='source_name',
        ),
    ]
