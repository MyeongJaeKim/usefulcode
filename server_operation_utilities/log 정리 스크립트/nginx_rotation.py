#! /usr/bin/env python

# ---------------------------------------------------------
#
# Nginx Log Rotation
#
# ---------------------------------------------------------

import os, glob, datetime, signal, time, gzip, boto

# ---------------------------------------------------------
# Constants
# ---------------------------------------------------------

NGINX_LOG_PATH = '/1111/1111/nginx/logs'

# ---------------------------------------------------------
# Step 1. Check Log Directory
# ---------------------------------------------------------

try:
    os.stat(NGINX_LOG_PATH)
except ex:
    print 'Log directory (' + NGINX_LOG_PATH + ') is not valid!'
    exit()

# ---------------------------------------------------------
# Step 2. Preparation
# ---------------------------------------------------------

# Today?
today = datetime.date.today()
today_str = today.strftime("%y-%m-%d")

# Get nginx Process ID
pid_file = open('/1111/1111/nginx/nginx.pid', 'r')
nginx_pid = pid_file.readline()
pid_file.close()

# ---------------------------------------------------------
# Step 3. Log file moving
# ---------------------------------------------------------

# Get current log files
log_file_list = glob.glob(NGINX_LOG_PATH + '/*.log')

# Rename *.log to *.log.yyyy-MM-dd
for file_entry in log_file_list:
    os.rename(file_entry, file_entry + '.' + today_str)

# ---------------------------------------------------------
# Step 4. Send Killing signal
# ---------------------------------------------------------

# Tell Nginx to create new log files
os.kill(int(nginx_pid), signal.SIGUSR1)

# Sleep 1 sec. to wait Nginx
time.sleep(1)

# ---------------------------------------------------------
# Step 5. Gzipping rotated log file
# ---------------------------------------------------------

# Get all renamed log files
log_file_list = glob.glob(NGINX_LOG_PATH + '/*.' + today_str)

# Gzipping
for file_entry in log_file_list:
    # Size 0 must be skipped
    if int(os.stat(file_entry).st_size) == 0:
        continue
    # Gzipped to new file
    f_in = open(file_entry, 'rb')
    f_out = gzip.open(file_entry + '.gz', 'wb')
    f_out.writelines(f_in)
    f_out.close()
    f_in.close()

# ---------------------------------------------------------
# Step 6. Delete original logs
# ---------------------------------------------------------

# Delete renamed log files
for file_entry in log_file_list:
    os.remove(file_entry)

# ---------------------------------------------------------
# Step 7. Find old log files older than 15 days
# ---------------------------------------------------------

# Find gzipped old log files
old_log_file_list = glob.glob(NGINX_LOG_PATH + '/*.gz')

# Find old log files older that 15 days
now = time.time()

too_old_log_file_list = []

for file_entry in old_log_file_list:
    if os.stat(file_entry).st_mtime < now - 15 * 86400:
        if os.path.isfile(file_entry):
            too_old_log_file_list.append(file_entry)

# ---------------------------------------------------------
# Step 8-1. Discard old log files
# ---------------------------------------------------------

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
