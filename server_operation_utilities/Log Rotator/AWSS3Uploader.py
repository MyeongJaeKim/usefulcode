#! /usr/bin/env python

import boto
from boto.s3.key import Key

class AWSS3Uploader:

    def __init__(self, awsId, awsKey, awsBucketName):
        try:
            self.s3Connection = boto.connect_s3(awsId, awsKey)
            self.bucket = self.s3Connection.get_bucket(awsBucketName)
            self.uploader = Key(self.bucket)
        except:
            print "AWS Initialization was failed!"
            exit()

    def uploadFile(self, fileName, fileFullPath):
        try:
            self.uploader.key = fileName
            self.uploader.set_contents_from_filename(fileFullPath)
        except:
            print "Uploading %s file was failed", fileFullPath

