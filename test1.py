import file_utils as fu
import os
# import filecmp
import hashlib
import hash_utils as hu
import sys


loc = "C:\\Users\\011868\\Pictures"
# loc = "/Users/hakob/Documents/ViberDownloads"
# loc = "C:\\Q_C_Hakob"
# text_file = open("C:\\Users\\011868\\Pictures\\Reports\\log.txt", "w")

df = hu.get_location_files_hashes_dict(loc)

print(sys.version, sys.executable)



# print(df.groupby(['file_hash']).count())

# print(fu.get_all_files_in_folder(loc))
# print(sys.version)
