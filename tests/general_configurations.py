import glob
from os import remove
from os.path import join


def remove_raw_files(raw_folder):
    file_list = glob.glob(join(raw_folder, "raw*"), recursive=False)
    for file in file_list:
        remove(file)
