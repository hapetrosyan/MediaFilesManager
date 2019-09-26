import file_utils as fu
import os
import pandas as pd
loc = "/Users/hakob/Documents/ViberDownloads"


df = fu.get_all_files_in_folder(loc)


print(type(df))