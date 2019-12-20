import file_utils as fu
import hash_utils as hu
import pandas as pd
from datetime import datetime
import os
import re
import funcs
import os
import sys





base_folder = input('enter base folder: ')

managed_files_folder = base_folder + '/ManagedFilesFolder'
guest_files = managed_files_folder + '/guest_files'
clean_repo = managed_files_folder + '/clean_folder'
service_files = managed_files_folder + '/service_files' # make hidden
clean_repo_files_list = service_files + '/clean_repo_files_list.csv'

if not os.path.exists(managed_files_folder):
    os.mkdir(managed_files_folder)
if not os.path.exists(guest_files):
    os.mkdir(guest_files)
if not os.path.exists(clean_repo):
    os.mkdir(clean_repo)
if not os.path.exists(service_files):
    os.mkdir(service_files)

'''
print ('Please enter operation type:')
print ('1 - accept new files')
print ('2 - shrink existing repo')
operation_type_code =  input('enter the option : ')
'''


# args = sys.argv
# age = 0
# name = ''
# city = ''

# for i in range( len(args) ):
#     if args[i] == '-managed files folder':
#         age = args[i+1]
#     elif args[i] == '-operation':
#         name = args[i+1]
#     elif args[i] == '-city':
#         city = args[i+1]

# print(age, name, city, aa)

# load csv file

tmp_csv = service_files + '/tmp_csv.csv'
'''
if os.path.exists(tmp_csv):
    os.remove(tmp_csv)

for dirpath, dirnames, filenames in os.walk(guest_files):
    df = pd.DataFrame()
    for filename in filenames:
        full_file_path = os.path.join(dirpath, filename)
        df = df.append ( [[full_file_path, os.path.splitext(filename)[-1].lower(), hu.get_file_hash(full_file_path)]] )
    df.to_csv(tmp_csv, mode='a', header=False, index=False)
    print(f'processing folder {dirpath}')
'''


# analyze csv

df = pd.read_csv(tmp_csv, names=['full_file_path', 'file_extension', 'file_hash'])
df['full_file_path'] = df['full_file_path'].apply(lambda x: x.replace('/media/hakob/Seagate Expansion Drive/', '')).str.lower() + '!'
df['file_extension'] = df['file_extension'].str.lower()
df_hash_paths_union = df.groupby('file_hash').agg('sum')
df_hash_paths_union['paths_list'] = df_hash_paths_union['full_file_path'].apply(lambda x: re.split('[ . / _  , !]' , x)).apply(lambda x: list(dict.fromkeys(x)))
df_hash_paths_union['desc_list'] = df_hash_paths_union['paths_list'].apply(funcs.remove_useless_words)
df_hash_paths_union.to_csv(clean_repo_files_list)


# deleting files
'''
df = pd.read_csv('my_csv.csv', names=['full_file_path', 'file_extension', 'file_hash'])
df = df.sort_values('file_hash')
df['is_copy'] = df['file_hash'].shift(1) == df['file_hash']
files_to_del = df[df['is_copy'] == True]['full_file_path']
for f in files_to_del:
    if os.path.exists(f):
        os.remove(f)
    else:
        print(f'The file {f} does not exist')
'''







# finding all unique words to remove useless ones
"""
s = {'jpg'}
for r in df_hash_paths_union['paths_list']:
    for elem in r:
        s.add(elem)

df_s = pd.DataFrame(s)
df_s.to_csv('df_set.csv', index=False)
"""