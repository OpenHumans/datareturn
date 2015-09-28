import argparse
import csv
import os
import sys

from boto.s3.connection import S3Connection


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
        if fileinfo[1] == 'local':
            assert os.path.exists(os.path.join(local_filedir, fileinfo[2]))


def load_local(file_list, local_filedir, bucket):
    check_local(file_list, args.localpath)
    for fileinfo in file_list:
        if not fileinfo[1] == 'local':
            continue
        filepath = os.path.join(local_filedir, fileinfo[2])
        s3_path = os.path.join('datareturn', fileinfo[0], fileinfo[3])
        key = bucket.new_key(s3_path)
        key.set_contents_from_filename(filepath)


def load_data(args):
    file_list = csvfile2list(args.filelist)
    s3 = s3_connection()
    bucket = s3.get_bucket(os.getenv('AWS_S3_STORAGE_BUCKET_NAME'))
    has_local = [x for x in file_list if x[1] == 'local']
    if has_local and not args.localpath:
        raise ValueError('File list indicates local files but no filepath '
                         'provided for local files.')
    load_local(file_list, args.localpath, bucket)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('filelist', help='CSV format, describes files to load')
    parser.add_argument('--localpath', help='path to local files')
    args = parser.parse_args()
    load_data(args)
