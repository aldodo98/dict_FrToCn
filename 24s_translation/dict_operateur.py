import json
import csv
import re
file_path = 'D://dict_FrToCn//24s_translation//items_collection/dict_enfant-f_accesoires.csv'

data = csv.reader(open('D://dict_FrToCn//24s_translation//items_collection//dict_enfant-f_accesoires.csv',encoding = 'utf-8'))
list1=[]
for line in data:
    if len(line[0])<=2:
        pass
    else:
        list2=[]
        list2.append(''.join( line[0][2:-2].replace('\'','').split(',')).lower())
        list2.append(line[1])
        list1.append(list2)

file_name = 'D://dict_FrToCn//24s_translation//data//dict_enfant-f_accesoires.csv'
try:

    with open(file_name, "a", encoding='utf-8-sig') as csvfile:
        writer = csv.writer(csvfile)
        for each in list1:
            list2 = []
            list2.append(each[0])
            list2.append(each[1])
            writer.writerow(list2)
except Exception as err:
    with open(file_name, "w", encoding='utf-8-sig') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["word_fr", "word_cn"])
        for each in list1:
            list2 = []
            list2.append(each[1])
            list2.append(each[0])
            writer.writerow(list2)