import csv
import os
from cStringIO import StringIO

from boto.s3.connection import S3Connection
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

from datareturn.models import DataFile, DataLink
from ._utils import new_user

User = get_user_model()


def s3_connection():
    """
    Get an S3 connection using environment variables.
    """
    key = os.getenv('AWS_ACCESS_KEY_ID')
    secret = os.getenv('AWS_SECRET_ACCESS_KEY')

    if not (key and secret):
        raise Exception('You must specify AWS credentials.')

    return S3Connection(key, secret)


def load_data(user, filedata):
    for item in filedata:
        print item
        if item[1] == 'file':
            data_file = DataFile(user=user)
            data_file.datafile.name = item[3]
            data_file.description = item[4]
            data_file.save()
        elif item[1] == 'link':
            data_link = DataLink(user=user)
            data_link.url = item[2]
            data_link.name = item[3]
            data_link.description = item[4]
            data_link.save()


def load_datareturn_info(bucket):
    key = bucket.get_key('datareturn_info.csv')
    contents = key.get_contents_as_string()
    filestring = StringIO(contents)
    data = csv.reader(filestring)
    contents = []
    for row in data:
        contents.append(row)
    return contents


class Command(BaseCommand):
    help = 'Create DataRecipientUsers for files loaded on S3.'

    def handle(self, *args, **options):
        s3 = s3_connection()
        bucket = s3.get_bucket(os.getenv('AWS_S3_STORAGE_BUCKET_NAME'))
        userdata = {}
        datareturn_info = load_datareturn_info(bucket)
        for item in datareturn_info:
            try:
                userdata[item[0]].append(item)
            except KeyError:
                userdata[item[0]] = [item]
        users = []
        for email in userdata:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                user = new_user(email=email)
                user.save()
            if user not in users:
                users.append(user)
        for user in users:
            load_data(user, userdata[user.email])
