#! /usr/bin/env python

import boto, os, tarfile, sys

# Verifying
if len(sys.argv) != 3:
    print "Usage : python backupFromJira.py <JIRA db exporting absolute path> <JIRA Attachment absolute path>"
    print "Usage : Enter 2 arguments in command line!!"
    exit()

jira_db_path = sys.argv[1]
jira_attachment_path = sys.argv[2]

try:
    os.stat(jira_db_path)
    os.stat(jira_attachment_path)
except:
    print "ERROR >> Arguments are not correct"
    exit()

access_key = '1111'
secret_key = '1111'
bucket_name = 'bucket'

# Connect to bucket
conn = boto.connect_s3(access_key, secret_key)
bucket = conn.get_bucket(bucket_name)

# Backup exported DB
most_recent_backupfile = find_most_recent(jira_db_path)

print "Most recent file is " + most_recent_backupfile

key = bucket.new_key("jira_exported_db.zip")
key.set_contents_from_filename(most_recent_backupfile)

if os.path.exists("attachment_jira.tar.gz") == True:
    os.remove("attachment_jira.tar.gz")

# Backup Attachment
tf = tarfile.open("attachment_jira.tar.gz", "w:gz")
tf.add(jira_attachment_path, arcname = os.path.basename(jira_attachment_path))
tf.close()

key = bucket.new_key("attachment_jira.tar.gz")
key.set_contents_from_filename("attachment_jira.tar.gz")

def find_most_recent(directory):
    files = os.listdir(directory)
    name_n_timestamp = dict([(x, os.stat(directory+x).st_mtime) for x in files])
    return max(name_n_timestamp, key=lambda k: name_n_timestamp.get(k))
