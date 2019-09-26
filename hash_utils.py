import os
import hashlib
import pandas as pd

# loc = "C:\\Users\\011868\\Pictures"
# loc = "C:\\Q_C_Hakob"
# text_file = open("C:\\Users\\011868\\Pictures\\Reports\\log.txt", "w")


def get_file_hash(filename):
    with open(filename, "rb") as f:
        bytes = f.read()  # read entire file as bytes
        readable_hash = hashlib.sha256(bytes).hexdigest()
        return (readable_hash)


def get_location_files_hashes_dict(location):
    df = pd.DataFrame(columns=['file_hash', 'file_extension'], index=['full_file_path'])
    for dirpath, dirnames, filenames in os.walk(location):
        for filename in filenames:
            full_file_path = os.path.join(dirpath, filename)
            df.loc[full_file_path] = [get_file_hash(full_file_path), os.path.splitext(filename)[-1].lower()]
    return df

