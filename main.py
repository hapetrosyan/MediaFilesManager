import file_utils as fu
import hash_utils as hu
import pandas as pd
from datetime import datetime
import os

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

# read csv to df

df = pd.read_csv('my_csv.csv', names=['full_file_path', 'file_extension', 'file_hash'])

# replace loc path

df['full_file_path'] = df['full_file_path'].apply(lambda x: x.replace('/media/hakob/Seagate Expansion Drive/', ''))

# create path words

df['path_words'] = df['full_file_path'].apply(lambda x: x.split('/')) 
