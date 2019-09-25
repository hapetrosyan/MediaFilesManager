import file_utils as fu
import os
# import filecmp
import hashlib
import hash_utils as hu

loc = "C:\\Users\\011868\\Pictures"
# loc = "C:\\Q_C_Hakob"
text_file = open("C:\\Users\\011868\\Pictures\\Reports\\log.txt", "w")

df = hu.get_location_files_hashes_dict(loc)

# print(df)

print(df.groupby(['file_hash']).count())

print(fu.get_all_files_in_folder(loc))
print(3334)