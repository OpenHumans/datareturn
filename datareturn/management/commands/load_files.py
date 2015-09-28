import os

from boto.s3.connection import S3Connection
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

from datareturn.models import DataFile
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


def os_split_all(path):
    split = os.path.split(path)
    if split[0] and split[1]:
        return os_split_all(split[0]) + [split[1]]
    elif split[0]:
        return [split[0]]
    return [split[1]]


def load_files(user, filedata):
    for email in filedata:
        assert email == user.email
        data_file = DataFile(user=user)
        data_file.datafile.name = filedata[email]
        data_file.save()


class Command(BaseCommand):
    help = 'Create DataRecipientUsers for files loaded on S3.'

    def handle(self, *args, **options):
        s3 = s3_connection()
        bucket = s3.get_bucket(os.getenv('AWS_S3_STORAGE_BUCKET_NAME'))
        userdata = {}
        for key in bucket.list():
            key_path = os_split_all(key.key)
            if key_path[0] != 'datareturn':
                continue
            userdata[key_path[1]] = key.key
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
            load_files(user, {k: userdata[k] for k in userdata if
                              k == user.email})
