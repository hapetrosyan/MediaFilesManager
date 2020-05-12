import file_utils as fu
import hash_utils as hu
import pandas as pd
from datetime import datetime
import os
import re
import funcs
import os
import sys
import shutil
from datetime import datetime
import argparse

start_time = datetime.now()
print('process started .......')

print(f'assigning arguments, variables and paths ... time passed: {datetime.now() - start_time}')

parser = argparse.ArgumentParser()
parser.add_argument('--base_folder', required=True, help='base folder help')
parser.add_argument('--delete_from_repo', required=False, help='reindex clean repo help')
args = parser.parse_args()
base_folder = args.base_folder
delete_from_repo = args.delete_from_repo

if delete_from_repo:
    print(f'delete_from_repo: {delete_from_repo}')

# base_folder =  input('enter base folder: ')
# base_folder = '/home/hakob/Pictures/Emma'
managed_files_folder = base_folder + '/MANAGED_FILES_FOLDER'
guest_files = managed_files_folder + '/GUEST_FILES'
clean_repo = managed_files_folder + '/CLEAN_REPO'
service_files = managed_files_folder + '/service_files' # make hidden
tmp_csv = service_files + '/tmp_csv.csv'
tmp_files_descr_list = service_files + '/tmp_files_descr_list.csv'
clean_repo_file_list = service_files + '/clean_repo_file_list.csv'
files_to_delete_from_repo = managed_files_folder + '/FILES_TO_DELETE'
deleted_files_log = service_files + '/deleted_files_log.csv'

if not os.path.exists(managed_files_folder):
    os.mkdir(managed_files_folder)
if not os.path.exists(guest_files):
    os.mkdir(guest_files)
if not os.path.exists(clean_repo):
    os.mkdir(clean_repo)
if not os.path.exists(service_files):
    os.mkdir(service_files)
if not os.path.exists(clean_repo_file_list):
    shutil.copyfile('clean_repo_file_list.csv', clean_repo_file_list) 
if not os.path.exists(files_to_delete_from_repo):
    os.mkdir(files_to_delete_from_repo)

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

if os.path.exists(tmp_csv):
    os.remove(tmp_csv)

if os.path.exists(tmp_files_descr_list):
    os.remove(tmp_files_descr_list)

print(f'walking through the guest files ... time passed: {datetime.now() - start_time}')

for dirpath, dirnames, filenames in os.walk(guest_files):
    df = pd.DataFrame()
    print(f'processing folder {dirpath} ... time passed: {datetime.now() - start_time}')
    for filename in filenames:
        full_file_path = os.path.join(dirpath, filename)
        df = df.append ( [[full_file_path, os.path.splitext(filename)[-1].lower(), hu.get_file_hash(full_file_path)]] )
    df.to_csv(tmp_csv, mode='a', header=False, index=False)
    print(f'folder {dirpath} processed ... time passed: {datetime.now() - start_time}')


# analyze csv
print(f'analyzing csv ... time passed: {datetime.now() - start_time}')

df = pd.read_csv(tmp_csv, names=['full_file_path', 'file_extension', 'file_hash'])
# df['full_file_path'] = df['full_file_path'].apply(lambda x: x.replace('/media/hakob/Seagate Expansion Drive/', '')).str.lower() + '!'
df['full_file_path_tosplit'] = df['full_file_path'].apply(lambda x: x.replace(guest_files, '')).str.lower() + '!'
df['file_extension'] = df['file_extension'].str.lower()
# df_hash_paths_union = df.groupby('file_hash', as_index=False).agg('sum')
df_hash_paths_union = df.groupby('file_hash', as_index=False).agg({'full_file_path_tosplit': 'sum', 'file_extension': 'min', 'full_file_path': 'min'})

df_hash_paths_union['paths_list'] = df_hash_paths_union['full_file_path_tosplit'].apply(lambda x: re.split('[ . / _ \\\  , !]' , x)).apply(lambda x: list(dict.fromkeys(x)))
df_hash_paths_union['desc_list'] = df_hash_paths_union['paths_list'].apply(funcs.remove_useless_words)
# df_hash_paths_union.to_csv(tmp_files_descr_list, index=False)   # to remove

df_guest_list = pd.read_csv(tmp_csv, names=['full_file_path', 'file_extension', 'file_hash'])
df_guest_list = df_guest_list.sort_values('file_hash')
df_guest_list['is_copy_in_guest'] = df_guest_list['file_hash'].shift(1) == df_guest_list['file_hash']
# df_guest_list.to_csv(service_files + '/guest_csv.csv', index=False) # to remove
os.remove(tmp_csv)

df_clean_repo_list = pd.read_csv(clean_repo_file_list)[['file_hash']]
df_clean_repo_list['is_copy_in_repo'] = True
# df_clean_replo_hashes = df_clean_repo_list['file_hash']



# delete files that have copy in clean or guest repo

mrg1 = pd.merge(df_guest_list, df_clean_repo_list, how='left', on='file_hash')
# print(mrg1[(mrg1['is_copy_in_repo'] == True) | (mrg1['is_copy_in_guest'] == True)])
files_to_del = mrg1[(mrg1['is_copy_in_repo'] == True) | (mrg1['is_copy_in_guest'] == True)]['full_file_path']
print(f'removing duplicate files ... time passed: {datetime.now() - start_time}')
for f in files_to_del:
    if os.path.exists(f):
        os.remove(f)
    else:
        print(f'The file {f} does not exist')

files_to_del.to_csv(deleted_files_log, index=False)

files_to_move = mrg1[(mrg1['is_copy_in_repo'] != True) & (mrg1['is_copy_in_guest'] == False)]['file_hash']
files_to_move = pd.DataFrame(files_to_move)
# print(files_to_move)

repo_add = pd.merge(files_to_move, df_hash_paths_union, how='inner', on='file_hash')[['file_hash', 'file_extension', 'desc_list', 'full_file_path']]

if repo_add.shape[0] > 0:
    date_time = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    repo_add['clean_repo_file_path'] = clean_repo + '/' + repo_add['full_file_path'].apply(lambda x: x.replace(guest_files, date_time))
    repo_add['date_copied'] =  date_time
    # os.mkdir(clean_repo + '/' + date_time)
    shutil.move(guest_files, clean_repo)
    os.rename(clean_repo + '/GUEST_FILES', clean_repo + '/' + date_time)
    funcs.removeEmptyfolders(clean_repo + '/' + date_time)
    clean_repo_insert = repo_add[['file_hash', 'file_extension', 'desc_list' ,'clean_repo_file_path', 'date_copied']]


    clean_repo_insert.to_csv(clean_repo_file_list, mode='a', header=False, index=False)

funcs.removeEmptyfolders(guest_files)

if not os.path.exists(guest_files):
    os.mkdir(guest_files)



# processing FILES_TO_DELETE

df_files_to_delete = pd.DataFrame()
for dirpath, dirnames, filenames in os.walk(files_to_delete_from_repo):
    for filename in filenames:
        full_file_path = os.path.join(dirpath, filename)
        df_files_to_delete = df_files_to_delete.append ( [{'del_file_hash': hu.get_file_hash(full_file_path)}] )
        
if df_files_to_delete.shape[0] > 0:
    print('deleting files in FILES_TO_DELETE folder ...........................................')

    df_clean_repo_list_after_fill = pd.read_csv(clean_repo_file_list)
    df_clean_repo_list_after_fill = df_clean_repo_list_after_fill[~df_clean_repo_list_after_fill['file_hash'].isin(df_files_to_delete['del_file_hash'])]
    # print(df_clean_repo_list_after_fill[~df_clean_repo_list_after_fill['file_hash'].isin(df_files_to_delete['del_file_hash'])])
    # print(df_clean_repo_list_after_fill)
    df_clean_repo_list_after_fill.to_csv(clean_repo_file_list, index=False)
    shutil.rmtree(files_to_delete_from_repo)
    print(f'{df_files_to_delete.shape[0]} files deleted form repository')
    if not os.path.exists(files_to_delete_from_repo):
        os.mkdir(files_to_delete_from_repo)
    
print(f'process finished, time passed: {datetime.now() - start_time}')


# to do list
# clean empty folder in clear repo
# add logging

# finding all unique words to remove useless ones
"""
s = {'jpg'}
for r in df_hash_paths_union['paths_list']:
    for elem in r:
        s.add(elem)

df_s = pd.DataFrame(s)
df_s.to_csv('df_set.csv', index=False)
"""