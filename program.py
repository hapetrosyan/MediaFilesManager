import file_utils as fu

# pairs = fu.get_pairs("C:\\temp\\pp")

# print(fu.get_pairs_of_files_in_folder("C:\\temp\\pp"))
loc = "C:\\Subversion"
print("------------------------------------------------------")
result = fu.get_same_files_in_folder(loc)

for row in result:
    print(row)

# print(fu.get_same_files_in_folder("C:\\SVN\\branches"))