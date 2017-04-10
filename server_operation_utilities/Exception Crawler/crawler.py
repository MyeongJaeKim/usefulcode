# ---------------------------------------------------------------------------------------------
# Exception Logs Crawler
#
# Work horse script
#
# Author : MJ Kim
# ---------------------------------------------------------------------------------------------

import cropper, sys

# ---------------------------------------------------------------------------------------------
# Check Commnadline Arguments
# ---------------------------------------------------------------------------------------------

if len(sys.argv) != 5:
    print "Usage : main.py <WAS LOG PATH> <WAS LOG FILENAME> <OUTPUT FILE PATH> <OUTPUT FILE NAME>"
    print "Usage : Enter 5 arguments in command line!!"
    exit()

log_path = sys.argv[1]
log_filename = sys.argv[2]

output_path = sys.argv[3]
output_filename = sys.argv[4]

# ---------------------------------------------------------------------------------------------
# Cropping Exception messages
# ---------------------------------------------------------------------------------------------

cut = cropper.Cropper(log_path, log_filename, '$# Exception information', '$# End logging',['.tar', '.gz'], output_path + '/' + output_filename)
cut.find_target_files()
cut.crop_exception()
cut.write_result_tofile()
