from datetime import datetime

import boto
import re
import os

from django.conf import settings
from boto.s3.connection import OrdinaryCallingFormat
from boto.s3.key import Key


class AWSUtils(object):
    access_key = None
    secret_key = None
    bucket = None
    region = None
    expires = getattr(settings, 'AWS_DOWNLOAD_EXPIRE', 5000)

    def __init__(self, access_key, secret_key, bucket, region, *args, **kwargs):
        self.bucket = bucket
        self.access_key = access_key
        self.secret_key = secret_key
        self.region = region
        super(AWSUtils, self).__init__(*args, **kwargs)

    def s3connect(self):
        conn = boto.s3.connect_to_region(
            self.region,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            is_secure=True,
            calling_format=OrdinaryCallingFormat()
        )
        return conn

    def get_bucket(self):
        # todo connect only one time
        conn = self.s3connect()
        bucket_name = self.bucket
        bucket = conn.get_bucket(bucket_name)
        return bucket

    def get_key(self, path):
        bucket = self.get_bucket()
        key = bucket.get_key(path)
        return key

    def get_filename(self, path, new_filename=None):
        current_filename = os.path.basename(path)
        if new_filename is not None:
            filename, file_extension = os.path.splitext(current_filename)
            escaped_new_filename_base = re.sub(r'[^A-Za-z0-9\#]+', '-', new_filename)
            escaped_filename = escaped_new_filename_base + file_extension
            return escaped_filename
        return current_filename

    def generate_url(self, path, download=True, new_filename=None):
        file_url = None
        aws_obj_key = self.get_key(path)
        if aws_obj_key:
            headers = None
            if download:
                filename = self.get_filename(path, new_filename=new_filename)
                headers = {
                    'response-content-type': 'application/force-download',
                    'response-content-disposition': 'attachment;filename="%s"' % filename
                }
            file_url = aws_obj_key.generate_url(
                response_headers=headers,
                expires_in=self.expires,
                method='GET')
        return file_url

    def upload_to_s3(self, file_path, destination=None):
        """
        Uploads the given file to the AWS S3

        :param file_path: File path where file is stored
        :param destination: destination where file is going to be store
        :return: boolean indicating success/failure of upload.
        """

        size = os.stat(file_path).st_size
        bucket = self.get_bucket()
        k = Key(bucket)
        new_file_name = os.path.basename(file_path)
        k.key = new_file_name
        if destination:
            k.key = destination

        sent = k.set_contents_from_filename(file_path)
        if sent == size:
            return True
        return False

    def move_deleted_file(self, file_path):
        """
        Rename file to the AWS S3

        :param file_path: File path where file is stored
        :return: boolean indicating success/failure of upload.
        """
        bucket = self.get_bucket()
        cuurent_time = datetime.now()
        src_file_path = file_path
        dest_file_path = "deleted/"+file_path+"_"+str(cuurent_time)
        bucket.copy_key(dest_file_path, bucket.name, src_file_path)
        k = Key(bucket,file_path)
        k.delete()
        return True
