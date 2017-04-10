#! /usr/bin/env python

# ---------------------------------------------------------
#
# Apache Log Rotation
#
# ---------------------------------------------------------

import os, glob, datetime, signal, time, gzip, boto

# ---------------------------------------------------------
# Constants
# ---------------------------------------------------------

APACHE_LOG_PATH = '/1111/apache2/logs'

# ---------------------------------------------------------
# Step 1. Check Log Directory
# ---------------------------------------------------------

try:
    os.stat(APACHE_LOG_PATH)
except ex:
    print 'Log directory (' + APACHE_LOG_PATH + ') is not valid!'
    exit()

# ---------------------------------------------------------
# Step 2. Check Argument to indentify this env is PRD
# ---------------------------------------------------------

FLAG_PRD=true

if len(sys.argv) == 1:
    FLAG_PRD=false

# ---------------------------------------------------------
# Step 3. Get Today in YYYYmmDD format
# ---------------------------------------------------------

# Today?
today = datetime.date.today()
today_str = today.strftime("%Y%m%d")

# ---------------------------------------------------------
# Step 5. Gzipping rotated log file
# ---------------------------------------------------------

# Get all renamed log files
log_file_list = glob.glob(APACHE_LOG_PATH + '/*.log.' + today_str)

# Gzipping
for file_entry in log_file_list:
    # Size 0 must be skipped
    if int(os.stat(file_entry).st_size) == 0:
        continue
    # .gz file must be skipped
    if os.path.split(file_entry)[1] == '.gz':
        continue
    # Gzipped to new file
    f_in = open(file_entry, 'rb')
    f_out = gzip.open(file_entry + '.gz', 'wb')
    f_out.writelines(f_in)
    f_out.close()
    f_in.close()
    # Delete Gzipped original file
    os.remove(file_entry)

# ---------------------------------------------------------
# Step 6. Find old log files older than 15 days
# ---------------------------------------------------------

# Find gzipped old log files
old_log_file_list = glob.glob(APACHE_LOG_PATH + '/*.gz')

# Find old log files older that 15 days
now = time.time()

too_old_log_file_list = []

for file_entry in old_log_file_list:
    if os.stat(file_entry).st_mtime < now - 15 * 86400:
        if os.path.isfile(file_entry):
            too_old_log_file_list.append(file_entry)

# ---------------------------------------------------------
# Step 7. Delete or Upload to AWS S3
# ---------------------------------------------------------

AWS_ACCESS_KEY_ID='1111'
AWS_SECRET_ACCESS_KEY='1111'

bucket_name = 'cns-webserver-old-log-global'

for file_entry in too_old_log_file_list:


# ONLY FOR DEV/STG SERVERS # ONLY FOR DEV/STG SERVERS # ONLY FOR DEV/STG SERVERS
# ONLY FOR DEV/STG SERVERS # ONLY FOR DEV/STG SERVERS # ONLY FOR DEV/STG SERVERS

#for file_entry in too_old_log_file_list:
#    os.remove(file_entry)

# ONLY FOR DEV/STG SERVERS # ONLY FOR DEV/STG SERVERS # ONLY FOR DEV/STG SERVERS
# ONLY FOR DEV/STG SERVERS # ONLY FOR DEV/STG SERVERS # ONLY FOR DEV/STG SERVERS

# ---------------------------------------------------------
# Step 8-2. Upload old logs to Amazon S3
# ---------------------------------------------------------

# ONLY FOR PRD SERVERS # ONLY FOR PRD SERVERS # ONLY FOR PRD SERVERS # ONLY FOR PRD SERVERS
# ONLY FOR PRD SERVERS # ONLY FOR PRD SERVERS # ONLY FOR PRD SERVERS # ONLY FOR PRD SERVERS

AWS_ACCESS_KEY_ID='1111'
AWS_SECRET_ACCESS_KEY='1111'

bucket_name = 'cns-webserver-old-log-global'

# Nothing to do
if len(too_old_log_file_list) > 0:
    # Connect to S3
    s3_connection = boto.connect_s3(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
    bucket = s3_connection.get_bucket(bucket_name)
    from boto.s3.key import Key
    file_key = Key(bucket)

    for file_entry in too_old_log_file_list:
        tokens = file_entry.split('/')
        file_name = tokens[len(tokens) - 1]
        # Upload S3
        file_key.key = file_name
        file_key.set_contents_from_filename(file_entry)

# ONLY FOR PRD SERVERS # ONLY FOR PRD SERVERS # ONLY FOR PRD SERVERS # ONLY FOR PRD SERVERS
# ONLY FOR PRD SERVERS # ONLY FOR PRD SERVERS # ONLY FOR PRD SERVERS # ONLY FOR PRD SERVERS
