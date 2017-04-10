import os

def path_name_split(path):
    return os.path.split(path)[1]

def name_ext_split(path):
    return os.path.splitext(path)[1]

print path_name_split('/1111/1111/1111/log/11/1111.cache.log')

print name_ext_split('/1111/1111/1111/log/11/1111.cache.log')
