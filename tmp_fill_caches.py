import file_utils as fu
import hash_utils as hu
import pandas as pd
from datetime import datetime
import os
import re
import funcs
import os

# load csv file

loc = '/media/hakob/Seagate Expansion Drive/ManagedMediaFiles/CleanRepo'
# os.remove('my_csv.csv')
startime = datetime.now()

for dirpath, dirnames, filenames in os.walk(loc):
    df = pd.DataFrame()
    for filename in filenames:
        full_file_path = os.path.join(dirpath, filename)
        df = df.append ( [[full_file_path, os.path.splitext(filename)[-1].lower(), hu.get_file_hash(full_file_path)]] )
    df.to_csv('CleanRepoFiles.csv', mode='a', header=False, index=False)
    print(f'processing folder {dirpath}')

endtime = datetime.now()
diff = endtime - startime
print(diff)