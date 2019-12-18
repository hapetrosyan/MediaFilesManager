

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
'hakob'
]

def remove_useless_words(lst):

    lst = [x for x in lst if x not in ex_list]
    ex_list_1 = []

    for e in lst:
        if str(e)[-2:] == 'kb' or str(e)[:3] == 'dsc' or str(e)[:5] == 'image' or str(e)[:7] == 'picture' or str(e)[-5:] == 'nikon':
            ex_list_1.append(e)

    lst = [x for x in lst if x not in ex_list_1]

    while ("" in lst):
        lst.remove("")

    # IMPLEMENT THE CASE WITH p_______ (p1150273)
    # REMOVE DIGITS THAT ARE NOT DATE

    return lst