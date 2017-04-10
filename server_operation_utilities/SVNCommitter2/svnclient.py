#! /usr/bin/env python

import pysvn, sys, os

class SVNClient:
    def __init__(self, svn_id, svn_passwd, trunk_path, branch_path):
        self.svn_id = svn_id
        self.svn_passwd = svn_passwd
        self.svnclient = pysvn.Client()
        self.svnclient.callback_get_login = self.svn_login
        self.svnclient.callback_get_log_message = self.get_log_message

        self.trunk_path = trunk_path
        self.branch_path = branch_path

        if verify_path() == False:
            print "Error >> SVN Path is incorrect!!"
            print "Error >> trunk : " + self.trunk_path
            print "Error >> branch : " + self.branch_path
            exit()
        print "SVN Login Successful!!"

    def svn_login(self, realm, username, may_save):
        isIdSave = True
        isUsePassword = True
        return isUsePassword, self.svn_id, self.svn_passwd, isIdSave

    def update_trunk_working_copy(self):
        print "Updating Trunk Working Copy...."
        self.svnclient.update(trunk_path)
        print "Updating Branch Working Copy...."
        self.svnclient.update(branch_path)

    def verify_path(self):
        if os.path.exists(self.trunk_path) == False:
            return False
        if os.path.exists(self.branch_path) == False:
            return False
        return True

    def get_log_message(self):
        return True, "Log message"

    def verify_existence(self, file_path):
        try:
            info = self.svnclient.info2(file_path)
        except pysvn._pysvn_2_7.ClientError, ex:
            return False
        return True

    def add_newfile_to_branch(self, src_url, dest_url):
        self.svnclient.copy2(src_url, dest_url, make_parents=True)
        self.svnclient.add(dest_url)
        print "Add to " + dest_url

    def copy_to_branch(self, src_url, dest_url):
        self.svnclient.copy2(src_url, dest_url, make_parents=True)
        print "Copy to " + dest_url

    def delete_file_in_branch(self, delete_file_url):
        retcode = self.verify_existence(delete_file_url)
        self.svnclient.remove(delete_file_url)
        print delete_file_url + " was deleted."

    def add_or_delete(self, trunk_url, branch_url):
        trunk_existence = verify_existence(trunk_url)
        branch_existence = verify_existence(branch_url)

        if trunk_existence == True and branch_existence == False:
            return "Add"
        if trunk_existence == False and branch_existence == True:
            return "Delete"