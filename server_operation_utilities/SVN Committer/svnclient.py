#! /usr/bin/env python

import pysvn, sys

class SVNClient:
    def __init__(self, svn_id, svn_passwd):
        self.svn_id = svn_id
        self.svn_passwd = svn_passwd
        self.svnclient = pysvn.Client()
        self.svnclient.callback_get_login = self.svn_login
        self.svnclient.callback_get_log_message = self.get_log_message
        print "SVN Login Successful!!"

    def get_log_message(self):
        return True, "Log message"

    def svn_login(self, realm, username, may_save):
        isIdSave = True
        isUsePassword = True
        return isUsePassword, self.svn_id, self.svn_passwd, isIdSave

    def verify_existence(self, file_path):
        try:
            info = self.svnclient.info2(file_path)
        except pysvn._pysvn_2_7.ClientError, ex:
            return False
        
        return True
        
    def delete_file_in_tag(self, delete_file_url):
        retcode = self.verify_existence(delete_file_url)
        if retcode is True:
            self.svnclient.remove(delete_file_url)
            print delete_file_url + " was deleted at tag"
        else:
            print delete_file_url + " is new file going to tag"

    def copy_trunk_file_to_tag(self, src_urls, dest_url):
        self.svnclient.copy2(src_urls, dest_url, make_parents=True)
        print "Copy to " + dest_url
        