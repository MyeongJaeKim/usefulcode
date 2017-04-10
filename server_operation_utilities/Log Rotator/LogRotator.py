#! /usr/bin/env python

import os, glob, gzip, time, socket
from AWSS3Uploader import AWSS3Uploader

class LogRotator:

    def __init__(self, startPath, rolledFilePattern, zippedFilePattern, logDecadePolicy, awsId, awsKey, awsBucket):
        if awsId != 'null':
            self.s3Uploader = AWSS3Uploader(awsId, awsKey, awsBucket)
        else:
            self.useS3 = False

        self.startPath = startPath
        self.rolledFilePattern = rolledFilePattern
        self.zippedFilePattern = zippedFilePattern
        self.logDecadePolicy = logDecadePolicy

    def grabUnzippedLogFile(self):
        logFileList = glob.glob(self.startPath + '/' + self.rolledFilePattern)

        return logFileList

    def grabOldZippedLogFile(self):
        zippedLogFile = glob.glob(self.startPath + '/' + self.zippedFilePattern)

        now = time.time()

        # Find the zipped files younger than ${logDecadePolicy} days, and except it
        oldZippedLogFile = []
        for fileEntry in zippedLogFile:
            if os.stat(fileEntry).st_mtime < now - self.logDecadePolicy * 86400:
                oldZippedLogFile.append(fileEntry)

        return oldZippedLogFile

    def compressGzip(self, fileFullPath):
        #print 'File is zipping :: ' + fileFullPath
        f_in = open(fileFullPath, 'rb')
        f_out = gzip.open(fileFullPath + '.gz', 'wb')
        f_out.writelines(f_in)
        f_out.close()
        f_in.close()

    def deleteFile(self, fileFullPath):
        os.remove(fileFullPath)

    def compressOldLog(self):
        oldLogFile = self.grabUnzippedLogFile()

        now = time.time()
        dayAgo = now - 86400

        for fileEntry in oldLogFile:
            if int(os.stat(fileEntry).st_size) > 0 and os.path.splitext(fileEntry)[1] != '.gz' and int(os.stat(fileEntry).st_mtime) < dayAgo:
                self.compressGzip(fileEntry)
                self.deleteFile(fileEntry)

    def uploadS3andRemove(self):
        oldZippedFile = self.grabOldZippedLogFile()

        hostname = socket.gethostname()

        for fileEntry in oldZippedFile:
            fileName = hostname + "/" + os.path.split(fileEntry)[1]
            try:
                self.s3Uploader.uploadFile(fileName, fileEntry)
            except:
                print "Upload was failed! %s" % (fileName, fileEntry)
                continue
            os.remove(fileEntry)
