#! /usr/bin/env python

# ---------------------------------------------------------
#
# WAS Log Rotation
#
# ---------------------------------------------------------

import os, glob, datetime, signal, time, gzip, boto

# ---------------------------------------------------------
# Constants
# ---------------------------------------------------------

WAS_LOG_BASE_PATH = '/111/1111'

PRD_ENV = True

# ---------------------------------------------------------
# Functions
# ---------------------------------------------------------

def find_all_sub_directory(path):
    directories = [os.path.join(path, f) for f in os.listdir(path)
                       if os.path.isdir(os.path.join(path, f))]
    return directories

def path_name_split(path):
    return os.path.split(path)[1]

def name_ext_split(path):
    return os.path.splitext(path)[1]

def compress(target_file):
    # Size 0 must be skipped
    if int(os.stat(target_file).st_size) > 0:
        # Gzipped to new file
        f_in = open(target_file, 'rb')
        f_out = gzip.open(target_file + '.gz', 'wb')
        f_out.writelines(f_in)
        f_out.close()
        f_in.close()

# ---------------------------------------------------------
# Global Variables
# ---------------------------------------------------------

# Working directories
jennifer_directories = []
application_directories = []
log4j_directories = []

# Today?
today = datetime.date.today()
today_str = today.strftime("%y-%m-%d")

# Result gathering
TOTAL_DELETE_FILES = []
TOTAL_GZIP_FILES = []
TOTAL_S3_MOVE_FILES = []

# ---------------------------------------------------------
# Step 1. Check Log Directory
# ---------------------------------------------------------

if os.path.exists(WAS_LOG_BASE_PATH) == False:
    print 'Log directory (' + WAS_LOG_BASE_PATH + ') is not valid!'
    exit()

# ---------------------------------------------------------
# Step 2. List up All Working directory
# ---------------------------------------------------------

application_directories = find_all_sub_directory(WAS_LOG_BASE_PATH)

for app_dir in application_directories:
    jennifer_directories.append(app_dir + '/log')

for log_dir in jennifer_directories:
    log4j_directories += find_all_sub_directory(log_dir)

# ---------------------------------------------------------
# Step 3. Gather old jennifer logs
# ---------------------------------------------------------

for jennifer_dir in jennifer_directories:
    TOTAL_DELETE_FILES += glob.glob(jennifer_dir + '/*.log.*')

# ---------------------------------------------------------
# Step 4. Gather old gzip files
# ---------------------------------------------------------

now = time.time()

gzipped_log_files = []

for log4j_dir in log4j_directories:
    gzipped_log_files += glob.glob(log4j_dir + '/*.log.*.gz')

for file_entry in gzipped_log_files:
    if os.stat(file_entry).st_mtime < now - 15 * 86400:
        if PRD_ENV:
            TOTAL_S3_MOVE_FILES.append(file_entry)
        else:
            TOTAL_DELETE_FILES.append(file_entry)

# ---------------------------------------------------------
# Step 5. Gather old log4j log files
# ---------------------------------------------------------

for log4j_dir in log4j_directories:
    TOTAL_GZIP_FILES += glob.glob(log4j_dir + '/*.log.*')

# ---------------------------------------------------------
# Step 6. Gzipping rolled log files and Remove them
# ---------------------------------------------------------

for file_entry in TOTAL_GZIP_FILES:
    if name_ext_split(file_entry) == '.gz':
        continue
    compress(file_entry)
    os.remove(file_entry)

# ---------------------------------------------------------
# Step 7. Delete Files
# ---------------------------------------------------------

for file_entry in TOTAL_DELETE_FILES:
    os.remove(file_entry)

# ---------------------------------------------------------
# Step 8. S3 Upload
# ---------------------------------------------------------

'''
AWS_ACCESS_KEY_ID='1111'
AWS_SECRET_ACCESS_KEY='1111'

bucket_name = 'cns-wasserver-old-log-spcs'

s3_connection = boto.connect_s3(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
bucket = s3_connection.get_bucket(bucket_name)
from boto.s3.key import Key
file_key = Key(bucket)
'''
for file_entry in TOTAL_S3_MOVE_FILES:
    if PRD_ENV:
        file_name = path_name_split(file_entry)
        # Upload S3
        file_key.key = file_name
        file_key.set_contents_from_filename(file_entry)
    os.remove(file_entry)
