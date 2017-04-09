#! /usr/bin/env python

import AWSS3Uploader

# 특정 폴더를 S3 의 특정 Bucket 으로 copy 하는 스크립트
# DB Data Directory 를 Backup 하는데 사용했었음

if len(sys.argv) != 4:
    print "Usage : main.py <FILE NAME> <FILE FULL PATH> <HOSTNAME>"
    print "Usage : Enter 2 arguments in command line!!"
    exit()

fileName = sys.argv[1]
filePath = sys.argv[2]
dbHostName = sys.argv[3]

uploader = AWSS3Uploader('key here', 'secret here', 'bucket name here')

s3ObjectName = dbHostName + '/' + fileName

uploader.uploadFile(s3ObjectName, filePath)
