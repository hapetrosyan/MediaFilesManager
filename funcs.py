

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
    


    return lst