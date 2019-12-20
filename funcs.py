import re

ex_list = ['pana',
'segateoriginalfiles',
'dvd',
'jpg',
'jpeg',
'hdd',
'archive',
'img',
'uniquecopiesfolder',
'tmp',
'mov',
'hd',
'copied',
'not',
'to',
'xary',
'hakob',
'pics',
'camera', 
'managedmediafiles', 'cleanrepo', 'samsung',
'uploads','sd', 'card', 'dcim', 'thumbnails', 
'phone'
]

def remove_useless_words(lst):

    lst = [x for x in lst if x not in ex_list]
    ex_list_1 = []

    for e in lst:
        if str(e)[-2:] == 'kb' or str(e)[:3] == 'dsc' or str(e)[:5] == 'image' or str(e)[:7] == 'picture' or str(e)[-5:] == 'nikon' or re.search("^p[0-9]{7}$", str(e)):
            ex_list_1.append(e)

    lst = [x for x in lst if x not in ex_list_1]

    while ("" in lst):
        lst.remove("")

    # IMPLEMENT THE CASE WITH p_______ (p1150273)
    # REMOVE DIGITS THAT ARE NOT DATE

    return lst


def get_descriptions_list(path_str):
    path_str = path_str.replace('/media/hakob/Seagate Expansion Drive/', '').lower() + '!'


# df['full_file_path'] = df['full_file_path'].apply(lambda x: x.replace('/media/hakob/Seagate Expansion Drive/', '')).str.lower() + '!'


    path_str = re.split('[ . / _  , ! \ ]' , path_str)
    path_str = list(dict.fromkeys(path_str))
    path_str = remove_useless_words(path_str)



    return path_str # .apply(lambda x: re.split('[ . / _  , !]' , x)).apply(lambda x: list(dict.fromkeys(x))).apply(remove_useless_words)