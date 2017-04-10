# ----------------------------------------------------------------------------------------
#
# Multiple words cropper from a given file
#
# Author : MJ Kim
# ----------------------------------------------------------------------------------------

import os, glob, time

class Cropper:

    # base_dir : target directory to parse a file
    # target_files_pattern : file name pattern to search
    # crop_start_pattern, crop_end_pattern : each start and end word to crop
    # skip_ext_patterns : extension of skipping file
    # output_filename : file name of output to write
    def __init__(self, base_dir, target_files_pattern, crop_start_pattern, crop_end_pattern, skip_ext_patterns, output_filename):

        if os.path.exists(base_dir) == False:
            print "Directory is invalid"
            exit()
        self.base_dir = base_dir
        self.output_filename = output_filename
        self.target_files_pattern = target_files_pattern


        # Regular Expression
        self.crop_start_pattern = crop_start_pattern
        self.crop_end_pattern = crop_end_pattern

        self.skip_ext_patterns = skip_ext_patterns
        self.output_data = []

        self.target_files = []

    # File extension splitter
    def name_ext_split(self, path):
        return os.path.splitext(path)[1]

    # File target file in a given directory
    def find_target_files(self):
        files = glob.glob(self.base_dir + '/' + self.target_files_pattern)

        for f in files:
            extension = self.name_ext_split(f)

            skippable = False

            # Check skip extension pattern
            for skip in self.skip_ext_patterns:
                if skip in extension:
                    skippable = True
            
            now = time.time()

            if os.stat(f).st_ctime < now - 86400:
                skippable = True

            if skippable:
                continue

            print "Appending .....  ", f
            self.target_files.append(f)

    # Crop text from file between start_pattern and end_pattern
    def crop_exception(self):

        for f in self.target_files:
            seeker = 0

            while True:

                # Open target file
                try:
                    fo = open(f, 'r', 1)
                    data = fo.read()
                except:
                    print "File open/read Error : " + f
                    break
                finally:
                    fo.close()

                # Find first index
                start_idx = data.find(self.crop_start_pattern, seeker)
                if start_idx == -1:
                    break

                # Find end index
                end_idx = data.find(self.crop_end_pattern, start_idx)
                if end_idx == -1:
                    break

                # Cropping and restoring result
                self.output_data.append(data[start_idx:end_idx])

                seeker = end_idx

    def get_result(self):
        return self.output_data

    def write_result_tofile(self):
        if len(self.output_data) > 0:

            # Concatenating
            data = ""
            for result in self.output_data:
                data = data + result

            # Write to file
            try:
                fw = open(self.output_filename, 'w', 1)
                fw.write(data)
            except:
                print "Writing result error"
                exit()
            finally:
                fw.close()

