# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datareturn', '0005_siteconfig_source_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='siteconfig',
            old_name='data_page_explanation',
            new_name='data_page_intro',
        ),
        migrations.AlterField(
            model_name='siteconfig',
            name='invite_email_content',
            field=models.TextField(default=b'', blank=True),
        ),
        migrations.AlterField(
            model_name='siteconfig',
            name='invite_email_subject',
            field=models.TextField(default=b'', blank=True),
        ),
        migrations.AlterField(
            model_name='siteconfig',
            name='data_page_intro',
            field=models.TextField(default=b'', blank=True),
        ),
        migrations.AddField(
            model_name='siteconfig',
            name='data_page_data_section',
            field=models.TextField(default=b'', blank=True),
        ),
        migrations.AddField(
            model_name='siteconfig',
            name='data_page_open_humans',
            field=models.TextField(default=b'', blank=True),
        ),
    ]
