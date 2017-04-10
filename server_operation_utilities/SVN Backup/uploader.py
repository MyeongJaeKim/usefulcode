#! /usr/bin/env python

import os, sys, boto
from boto.s3.key import Key

if len(sys.argv) != 3:
    print "Usage : python uploader.py <bucket name> <file absolute path>"
    print "Usage : Enter 2 arguments in command line!!"
    exit()

# sangyoon.shin
AWS_ACCESS_KEY = "1111"
AWS_SECRET = "1111"

s3Connection = boto.connect_s3(AWS_ACCESS_KEY, AWS_SECRET)

try:
    bucket = s3Connection.get_bucket(sys.argv[1])
    uploader = Key(bucket)
except:
    print "ERROR >> Connecting to bucket was failed !!!"
    exit()

uploadFile = sys.argv[2]

try:
    os.path.exists(uploadFile)
except:
    print "ERROR >> File is not existed in " + uploadFile
    exit()

uploader.key = os.path.split(uploadFile)[1]
uploader.set_contents_from_filename(uploadFile)

print "Done. Uploaded : " + uploadFile
