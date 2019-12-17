import file_utils as fu
import hash_utils as hu
import pandas as pd
from datetime import datetime
import os
import re

# load csv file

loc = '/media/hakob/Seagate Expansion Drive'
os.remove('my_csv.csv')
startime = datetime.now()

for dirpath, dirnames, filenames in os.walk(loc):
    # print(dirpath)
    df = pd.DataFrame()
    for filename in filenames:
        # print(filename)
        full_file_path = os.path.join(dirpath, filename)
        df = df.append ( [[full_file_path, os.path.splitext(filename)[-1].lower(), hu.get_file_hash(full_file_path)]] )
    df.to_csv('my_csv.csv', mode='a', header=False, index=False)
    print(f'processing folder {dirpath}')

endtime = datetime.now()
diff = endtime - startime
print(diff)

# analyze csv

df = pd.read_csv('my_csv.csv', names=['full_file_path', 'file_extension', 'file_hash'])
df['full_file_path'] = df['full_file_path'].apply(lambda x: x.replace('/media/hakob/Seagate Expansion Drive/', ''))
df['full_file_path'] = df['full_file_path'].str.lower()
df['file_extension'] = df['file_extension'].str.lower()
# df['path_words'] = df['full_file_path'].apply(lambda x: x.split('/')).apply(lambda x: x[1:])
# df['path_words'] = df['full_file_path'].apply(lambda x: re.split('[ . / _  ,]' , x))

df['full_file_path'] = df['full_file_path'] + '!'
df_hash_paths_union = df.groupby('file_hash').agg('sum')
df_hash_paths_union['paths_list'] = df_hash_paths_union['full_file_path'].apply(lambda x: re.split('[ . / _  , !]' , x)).apply(lambda x: list(dict.fromkeys(x)))
# df_hash_paths_union.to_csv('path_words.csv')