import sys
import os
import hashlib

# text_file = open("C:\\temp\\pp\\Output.txt", "w")


def chunk_reader(fobj, chunk_size=1024):
    """Generator that reads a file in chunks of bytes"""
    while True:
        chunk = fobj.read(chunk_size)
        if not chunk:
            return
        yield chunk

def check_for_duplicates(paths, hash=hashlib.sha1):
    text_file = open("C:\\Users\\011868\\Pictures\\Reports\\log.txt", "w")
    hashes = {}
    for path in paths:
        for dir_path, dir_names, file_names in os.walk(path):
            for filename in file_names:
                full_path = os.path.join(dir_path, filename)
                hash_object = hash()
                for chunk in chunk_reader(open(full_path, 'rb')):
                    hash_object.update(chunk)
                file_id = (hash_object.digest(), os.path.getsize(full_path))
                duplicate = hashes.get(file_id, None)
                if duplicate:
                    # print ("Duplicate found: %s and %s" % (full_path, duplicate))
                    text_file.write("Duplicate found: %s and %s\n" % (full_path, duplicate))
                else:
                    hashes[file_id] = full_path
    text_file.close()

if sys.argv[1:]:
    check_for_duplicates(sys.argv[1:])
else:
    print ("Please pass the paths to check as parameters to the script")
