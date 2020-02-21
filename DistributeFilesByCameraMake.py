import os
from PIL import Image, ExifTags
import pandas as pd
import shutil

main_dir = input("Pleas eneter main directory:   ")

df = pd.DataFrame(columns= ['FileFullPath', 'FileFullPathNew', 'NewDirFullPath'])

def get_camera_make_model(f_loc):
    try:
        img = Image.open(f_loc)
        exif = { ExifTags.TAGS[k]: v for k, v in img._getexif().items() if k in ExifTags.TAGS }
        make_model = exif['Make'] # + ' ' + exif['Model']
    except:
        make_model = 'NoCamera'
    return make_model


copy_dir = main_dir + '/DistributedByCamera'
os.mkdir(copy_dir)

i = 0
for root, dirs, files in os.walk(main_dir, topdown=False):
    for name in files:
        cameara_model = get_camera_make_model(os.path.join(root, name))
        full_file_path_original = os.path.join(root, name)
        full_file_path_new = full_file_path_original.replace(main_dir, main_dir + '\\DistributedByCamera\\' + cameara_model)
        full_file_dir_new = root.replace(main_dir, main_dir + '\\DistributedByCamera\\' + cameara_model)
        df.loc[i] = full_file_path_original, full_file_path_new, full_file_dir_new
        i += 1

dirs = df['NewDirFullPath'].unique()
for d in dirs:
    # print(d.replace(main_dir, main_dir + '\\DistributedByCamera'))
    try:
        os.makedirs(d)
    except:
        continue

for index, row in df.iterrows():
    # print(row['FileFullPath'], row['FileFullPathNew'])
    shutil.move(row['FileFullPath'], row['NewDirFullPath'])
