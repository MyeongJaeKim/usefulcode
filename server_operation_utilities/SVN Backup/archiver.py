#! /usr/bin/env python

import os, gzip, sys, tarfile

if len(sys.argv) != 3:
    print "Usage : python archiver.py <zipping directory> <zip file>"
    print "Usage : Enter 2 arguments in command line!!"
    exit()

ZIPPING_DIRECTORY = sys.argv[1]
ZIP_FILE = sys.argv[2]

if os.path.exists(ZIPPING_DIRECTORY) == False:
    print "Directory is invalid"
    exit()

if os.path.exists(ZIP_FILE) == True:
    os.remove(ZIP_FILE)

tf = tarfile.open(ZIP_FILE, "w:gz")
tf.add(ZIPPING_DIRECTORY, arcname = os.path.basename(ZIPPING_DIRECTORY))
tf.close()
