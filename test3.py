import matplotlib as m
import file_utils as fu

a = round(9.49)

dir_loc = '/home/hakob/Downloads'

files = fu.get_all_files_in_folder(dir_loc)

print(f'files are: {files}')