# ---------------------------------------------------------------------------------------------
# Exception Logs Grabber
#
# Work horse script
#
# Author : MJ Kim
# ---------------------------------------------------------------------------------------------

import AWSSESSender, sys, os, datetime, tarfile

# ---------------------------------------------------------------------------------------------
# Check Commnadline Arguments
# ---------------------------------------------------------------------------------------------

if len(sys.argv) != 3:
    print "Usage : python grabber.py <OUTPUT FILE PATH> <CENTER NAME>"
    print "Usage : Enter 2 arguments in command line!!"
    exit()

output_path = sys.argv[1]
center_name = sys.argv[2]

# ---------------------------------------------------------------------------------------------
# Grabbing all results files
# ---------------------------------------------------------------------------------------------

files = os.listdir(output_path)

# ---------------------------------------------------------------------------------------------
# Making Tar file
# ---------------------------------------------------------------------------------------------

today = datetime.date.today()
today = today.strftime("%y-%m-%d")

tarfile_name = output_path + "/WAS_Exception_" + center_name + "_" + today + ".tar.gz"

out = tarfile.open(tarfile_name, mode='w:gz')

try:
    for file in files:
        # Ignore directory hierarchy
        out.add(output_path + "/" + file, arcname=file)
except:
    print "Error while making tar archive"
    exit()
finally:
    out.close()

for file in files:
    os.remove(file)

# ---------------------------------------------------------------------------------------------
# Sending an Email with tar file
# ---------------------------------------------------------------------------------------------

mail_service = AWSSESSender.AWSSESSender("1111", "1111")

recipient_list = ["abc@abc.com", "abc@abc.com"]

mail_service.send_raw_email("abc@abc.com",
                            "Online Exception Report - " + today + " - " + center_name,
                            "Online Exception Report",
                             recipient_list,
                             tarfile_name)
