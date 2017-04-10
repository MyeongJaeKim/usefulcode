# ----------------------------------------------------------------------------------------
# Exception Logs Crawler 
#
# Work horse script
#
# Author : MJ Kim
# ----------------------------------------------------------------------------------------

import cropper

output = []

#cut = cropper.Cropper(".", "testdata", "[\$\#][\s][Exception][\s][information]", "[\$\#][\s][End][\s][logging]",['.tar', '.gz'], output)
cut = cropper.Cropper(".", "testdata", "$#Exception information", "$# End logging",['.tar', '.gz'], output)
cut.find_target_files()
cut.crop_exception()

result = cut.get_result()

for res in result:
    print res
