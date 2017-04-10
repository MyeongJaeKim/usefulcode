#! /usr/bin/env python


import sys
from LogRotator import LogRotator

# ---------------------------------------------------------------------------------------------
# Check Commnadline Arguments
# ---------------------------------------------------------------------------------------------

if len(sys.argv) != 7:
    print "Usage : main.py <START_PATH> <ROLLED_FILE_PATTERN> <ZIPPED_FILE_PATTERN> <AWS ID> <AWS KEY> <AWS BUCKET>"
    print "Usage : Enter 7 arguments in command line!!"
    print "Usage : If this is not production environment, AWS arguments can be 'null'"
    exit()

# ---------------------------------------------------------------------------------------------
# Environment
# ---------------------------------------------------------------------------------------------

START_PATH=sys.argv[1]
ROLLED_FILE_PATTERN=sys.argv[2]
ZIPPED_FILE_PATTERN=sys.argv[3]
LOG_DECADE_POLICY=15

AWS_ID=sys.argv[4]
AWS_KEY=sys.argv[5]
AWS_BUCKET=sys.argv[6]

logWorker = LogRotator(START_PATH, ROLLED_FILE_PATTERN, ZIPPED_FILE_PATTERN, LOG_DECADE_POLICY, AWS_ID, AWS_KEY, AWS_BUCKET)

logWorker.compressOldLog()
logWorker.uploadS3andRemove()

