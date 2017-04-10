# ----------------------------------------------------------------------------------------
#
# AWS SES - boto's email sender API Wrapper
#
# Author : MJ Kim
# ----------------------------------------------------------------------------------------

from boto.ses import SESConnection

# For RAW type email seding
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart

import os

class AWSSESSender:

    def __init__ (self, aws_access_key, aws_secret_key):
        try:
            self.ses_conn = SESConnection(aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)
        except:
            print "SES Connection was failed !!"
            exit()

    def send_email(self, sender, subject, body, recipient_list):
        if self.ses_conn != None:
            self.ses_conn.send_email(sender, subject, body, recipient_list)
        else:
            print "Connection object is null!!"

    def send_raw_email(self, sender, subject, body, recipient_list, attachment_path):
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = sender

        to_list = ""

        for idx, data in enumerate(recipient_list):
            if idx < len(recipient_list) -1:
                to_list += data + ","
            else:
                to_list += data

        msg['To'] = to_list
        msg.premable = 'Multipart Message.\n'

        # Assembling Mail body
        part = MIMEText(body)
        msg.attach(part)

        # Assembling Attachment
        part = MIMEApplication(open(attachment_path, 'rb').read())
        part.add_header('Content-Disposition', 'attachment', filename=os.path.basename(attachment_path))
        msg.attach(part)

        # Send RAW email
        if self.ses_conn != None:
            self.ses_conn.send_raw_email(msg.as_string(), source=msg['From'], destinations=recipient_list)
        else:
            print "Connection object is null!!"
        



