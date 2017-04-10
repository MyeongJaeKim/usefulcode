#! /usr/bin/env python

import sys, pysvn
from svnclient import SVNClient

# ---------------------------------------------------------------------------------------------
# Check Commnadline Arguments
# ---------------------------------------------------------------------------------------------

if len(sys.argv) is not 5:
    print "Usage : main.py <deploy-list-file-name> <application-name> <SVN ID> <SVN Password>"
    print "Usage : Enter 4 arguments in command line!!"
    exit()

# ---------------------------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------------------------
_url_prefix = "svn://1.1.1.1/"
_url_application_postfix = "-ear"
_url_trunk = "/trunk/"
_url_tags = "/tags/"
_url_tag_postfix = "-ear-staging"

# "svn://localhost/" + argument + "/trunk/" + argument + "-ear"
_trunk_prefix = _url_prefix + sys.argv[2] + _url_trunk + sys.argv[2] + _url_application_postfix
#_trunk_prefix = _url_prefix + "sample/svn-automerger" + _url_trunk + sys.argv[2] + _url_application_postfix
_tags_prefix = _url_prefix + sys.argv[2] + _url_tags + sys.argv[2] + _url_tag_postfix
#_tags_prefix = _url_prefix + "sample/svn-automerger" + _url_tags + sys.argv[2] + _url_tag_postfix

# ---------------------------------------------------------------------------------------------
# Initialization Steps..
# ---------------------------------------------------------------------------------------------
my_client = SVNClient(sys.argv[3], sys.argv[4])


# Make trunk full file path from requested list
trunk_file_list = []
tag_file_list = []

fileHandler = file(sys.argv[1], 'r')
for line in fileHandler:
    # Trimming
    trimmed = line.strip()
    trimmed = trimmed.rstrip()
    if len(trimmed) > 0:
        trunk_file_list.append(_trunk_prefix + trimmed)
        tag_file_list.append(_tags_prefix + trimmed)
    else:
        print "CR/LF was skipped"

# ---------------------------------------------------------------------------------------------
# Verify file list to detect incorrect request file
# ---------------------------------------------------------------------------------------------
error_file_list = []
for entry in trunk_file_list:
    if my_client.verify_existence(entry) is False:
        error_file_list.append(entry)

if len(error_file_list) > 0:
    print "\nRequest is not valid!!!! Check below files!!"
    print error_file_list
    exit()

print "\nVerification was completed. All request files are in trunk!!"

# ---------------------------------------------------------------------------------------------
# Delete files in tag
# ---------------------------------------------------------------------------------------------
print "\nAll initilization was completed."
print "Start to delete files at tag."

for entry in tag_file_list:
    my_client.delete_file_in_tag(entry)

print str(len(trunk_file_list)) + " files are processed. Is this correct?"

# ---------------------------------------------------------------------------------------------
# Copy files from trunk to tag
# ---------------------------------------------------------------------------------------------
print "\nStart to copy files from trunk to tag"

copy_file_list = []
for entry in trunk_file_list:
    copy_file_list.append( (entry, ) )

#my_client.copy_trunk_file_to_tag(copy_file_list, _tags_prefix)

for idx in range(len(copy_file_list)) :
    print str(copy_file_list[idx]) + " to " + tag_file_list[idx]
    my_client.copy_trunk_file_to_tag([copy_file_list[idx]], tag_file_list[idx])

print "\nAll job has done!!!"
