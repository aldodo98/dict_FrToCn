import json
from googletrans import Translator
import re


# print("哪个词典？accessoires_dict.json,beaute_dict.json,bijoux_dict.json,chaussures_dict.json,pretaporter_dict.json,sac_dict.json")
dict_name=''
dict_name='accessoires_dict.json'
dict_repertoire = 'D:\dict_FrToCn\\24s_translation\\24s\\dict_24s\\'
dict_path = dict_repertoire+dict_name


def translate(data):
    data = ''.join(data)
    translator = Translator()
    trans_data = translator.translate(data, src='fr', dest='zh-cn')
    return trans_data.text

def data_pretraiter(data):
    data_fr = re.split(' ',data.lower())
    data_garde = ''
    try:
        with open(dict_repertoire+'motGarde_dict.json', encoding='utf-8') as motGarde_dict:
            motGarde_dict = json.load(motGarde_dict)
            new_data_fr = []
            for each in data_fr:
                have = True
                for every in motGarde_dict:
                    if each == every:
                        data_garde = each
                        have = False
                if have:
                    new_data_fr.append(each)
            return ' '.join(new_data_fr),data_garde
    except Exception:
        return ' '.join(data_fr),data_garde

with open(dict_path,encoding='utf-8') as accessoires_dict:
    data = json.load(accessoires_dict)
    emptyDict = {}
    frWord = 'Bob en nylon imprimé logo'
    for each in data:
        emptyDict[each['wordFr']] = each['wordCn']
    try:
        print(emptyDict[frWord])
    except Exception as err:
        if len(frWord.split(' '))>3:
            col = []
            data_apresTraitement, mot_garde = data_pretraiter(frWord)
            print(mot_garde+translate(data_apresTraitement))
        else:
            frWord = frWord.split(' ')[0]
            print(emptyDict[frWord])


# list=['big','pig','dolphin']
# with open(dict_repertoire + 'test.json', "a", encoding='utf-8-sig') as jsfile:
#     jsfile.write(json.dumps(list, indent=4, ensure_ascii=False))

