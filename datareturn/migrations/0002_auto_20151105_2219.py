# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datareturn', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='openhumansconfig',
            name='client_id',
        ),
        migrations.RemoveField(
            model_name='openhumansconfig',
            name='client_secret',
        ),
    ]
