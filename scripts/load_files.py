import argparse
from cStringIO import StringIO
import csv
import hashlib
import os
import sys

from boto.s3.connection import S3Connection


def hashfile(filepath):
    sha1 = hashlib.sha1()
    f = open(filepath, 'rb')
    try:
        sha1.update(f.read())
    finally:
        f.close()
    return sha1.hexdigest()


def s3_connection():
    """
    Get an S3 connection using environment variables.
    """
    key = os.getenv('AWS_ACCESS_KEY_ID')
    secret = os.getenv('AWS_SECRET_ACCESS_KEY')

    if not (key and secret):
        raise Exception('You must specify AWS credentials.')

    return S3Connection(key, secret)


def csvfile2list(filepath):
    returned_list = []
    with open(filepath) as f:
        input_csv = csv.reader(f)
        for row in input_csv:
            returned_list.append(row)
    return returned_list


def check_local(file_list, local_filedir):
    for fileinfo in file_list:
        if fileinfo[1] == 'file':
            assert os.path.exists(os.path.join(local_filedir, fileinfo[2]))


def load_local(file_list, local_filedir, bucket):
    check_local(file_list, args.localpath)
    list_update = StringIO()
    list_update_csv = csv.writer(list_update)
    for fileinfo in file_list:
        if not fileinfo[1] == 'file':
            list_update_csv.writerow(fileinfo)
            continue
        filepath = os.path.join(local_filedir, fileinfo[2])
        s3_path = os.path.join('datareturn', hashfile(filepath), fileinfo[3])
        key = bucket.new_key(s3_path)
        key.set_contents_from_filename(filepath)
        fileinfo[2] = s3_path
        list_update_csv.writerow(fileinfo)
    return list_update.getvalue()


def load_data(args):
    """
    Load local files onto S3, as well as the "item list" CSV document itself.

    The "item list" CSV document describes loaded files and/or links. See
    description below for how this should be formatted. There should be no
    header row.

    A slightly modified copy of the item list will be loaded to S3 (see
    column 4 description regarding modification).

    Every 'file' item on the list (which must correspond to a local file) will
    also be loaded onto S3.

    Column 1: Recipient.
              The recipient's email address.

    Column 2: Type.
              There are two different return methods: 'local' or 'link'.
              'file': local file that will be loaded onto S3.
              'link': URL to return.

    Column 3: Path to file.
              For 'file' this is the path relative to args.localpath.
              For 'link' this is the URL for the item.

    Column 4: Name.
              For 'file' this is the basename to use for the file on S3.
                On S3, this is replaced with the key name, which combines this
                basename with a sha1 of the file.
              For 'link' this is a name to use when displaying the link.

    Column 5: Description.
              Description of this item.
    """
    file_list = csvfile2list(args.filelist)
    s3 = s3_connection()
    bucket = s3.get_bucket(os.getenv('AWS_S3_STORAGE_BUCKET_NAME'))
    has_local = [x for x in file_list if x[1] == 'file']
    if has_local and not args.localpath:
        raise ValueError('File list indicates local files but no filepath '
                         'provided for local files.')

    file_list_updated = load_local(file_list, args.localpath, bucket)

    # Keys are "SHA1/BASENAME", combining
    # Updated file list replaces the 'file' name field with this
    key = bucket.new_key('datareturn_info.csv')
    key.set_contents_from_string(file_list_updated)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('filelist', help='CSV format, describes files to load')
    parser.add_argument('--localpath', help='path to local files')
    args = parser.parse_args()
    load_data(args)
