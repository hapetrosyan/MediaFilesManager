

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
'to'
]

def remove_useless_words(lst):

    lst = [x for x in lst if x not in ex_list]

    for e in lst:
        if str(e)[-2:] == 'kb' or str(e)[:3] == 'dsc' or str(e)[:5] == 'image' or str(e)[:7] == 'picture' or str(e)[-5:] == 'nikon':
            lst.remove(e)
    


    return lst