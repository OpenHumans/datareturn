# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import datareturn.models


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DataFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datafile', models.FileField(storage=datareturn.models.MyS3BotoStorage(querystring_expire=600, querystring_auth=True, acl=b'private'), upload_to=b'')),
                ('description', models.TextField(default=b'')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DataLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.TextField(default=b'')),
                ('name', models.TextField(default=b'')),
                ('description', models.TextField(default=b'')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OpenHumansConfig',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('client_id', models.CharField(max_length=255)),
                ('client_secret', models.CharField(max_length=255)),
                ('source_name', models.CharField(max_length=255)),
                ('site', models.OneToOneField(to='sites.Site')),
            ],
        ),
        migrations.CreateModel(
            name='OpenHumansUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('openhumans_userid', models.PositiveIntegerField(null=True)),
                ('access_token', models.CharField(max_length=60, blank=True)),
                ('refresh_token', models.CharField(max_length=60, blank=True)),
                ('token_expiration', models.DateTimeField(null=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SiteConfig',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('source_name', models.CharField(max_length=40)),
                ('data_page_explanation', models.TextField(default=b'')),
                ('site', models.OneToOneField(to='sites.Site')),
            ],
        ),
    ]
