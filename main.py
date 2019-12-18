import file_utils as fu
import hash_utils as hu
import pandas as pd
from datetime import datetime
import os
import re
import funcs

# load csv file
"""
loc = '/media/hakob/Seagate Expansion Drive'
# os.remove('my_csv.csv')
startime = datetime.now()

for dirpath, dirnames, filenames in os.walk(loc):
    df = pd.DataFrame()
    for filename in filenames:
        full_file_path = os.path.join(dirpath, filename)
        df = df.append ( [[full_file_path, os.path.splitext(filename)[-1].lower(), hu.get_file_hash(full_file_path)]] )
    df.to_csv('my_csv.csv', mode='a', header=False, index=False)
    print(f'processing folder {dirpath}')

endtime = datetime.now()
diff = endtime - startime
print(diff)
"""

# analyze csv

df = pd.read_csv('my_csv.csv', names=['full_file_path', 'file_extension', 'file_hash'])
df['full_file_path'] = df['full_file_path'].apply(lambda x: x.replace('/media/hakob/Seagate Expansion Drive/', '')).str.lower() + '!'
df['file_extension'] = df['file_extension'].str.lower()
df_hash_paths_union = df.groupby('file_hash').agg('sum')
df_hash_paths_union['paths_list'] = df_hash_paths_union['full_file_path'].apply(lambda x: re.split('[ . / _  , !]' , x)).apply(lambda x: list(dict.fromkeys(x)))
df_hash_paths_union['desc_list'] = df_hash_paths_union['paths_list'].apply(funcs.remove_useless_words)
df_hash_paths_union.to_csv('path_words.csv')


# finding all unique words to remove useless ones
"""
s = {'jpg'}
for r in df_hash_paths_union['paths_list']:
    for elem in r:
        s.add(elem)

df_s = pd.DataFrame(s)
df_s.to_csv('df_set.csv', index=False)
"""