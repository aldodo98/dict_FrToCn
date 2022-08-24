from googletrans import Translator
import json
import difflib
from googletrans import Translator
import csv
import re

def translate(data):
    translator = Translator()
    trans_data = translator.translate(data, src='fr', dest='zh-cn')
    data2 = trans_data.text
    if data2.find("面具") != -1:
        data2 = data2.replace("面具", "口罩")

    return data2

def data_pretraiter(data):
    data_fr = re.split(' ',data['name_fr'].lower())
    data_garde = ''
    try:
        data_zh =re.match("[a-zA-Z]+", data['name_zh']).group().lower()
        new_data_fr = []
        for each in data_fr:
            if each == data_zh:
                data_garde = each
            else:
                new_data_fr.append(each)
        return ' '.join(new_data_fr),data_garde
    except Exception:
        return ' '.join(data_fr),data_garde



list_docs = ['enfant-f_accesoires.json','enfant-f_chaussures.json','enfant-f_offre.json','enfant-f_vetements.json','enfant-g_accesoirs.json','enfant-g_chaussures.json','enfant-g_offre.json','enfant-g_vetements.json','femme_accesoires.json','femme_beaute.json','femme_bijoux.json','femme_chaussures.json','femme_offre.json','femme_sac.json','femme_vetements.json','homme_accesoires.json','homme_beaute.json','homme_chaussures.json','homme_offre.json','homme_sac.json','homme_sport.json','homme_vetements.json','maison_arts.json','maison_deco.json','maison_linge.json','maison_luminaires.json','maison_mobilier.json','maison_offre.json']
str = ['enfant-f_accesoires.json']
for data_original in str:
        # file_path = 'D:\\dict_FrToCn\\24s_translation\\items_collection\\items_collection\\' + data_original
        file_position = 'D://dict_FrToCn//24s_translation//items_collection//items_collection//'
        file_path = file_position + data_original
        with open(file_path, encoding='utf-8') as data_site:
            data = json.load(data_site)
            data1 = []
            for each in data:
                col = []
                col.append(each['name_fr'])
                col.append(each['name_zh'])
                data_apresTraitement,mot_garde = data_pretraiter(each)
                col.append(mot_garde + translate(data_apresTraitement))

                print(col)
                data1.append(col)

                with open (file_position+'dict_'+data_original, "a", encoding='utf-8-sig') as jsfile:
                    jsfile.write(json.dumps(col, indent=4, ensure_ascii=False))

#整理出固定词汇不翻译
#已知：logo不翻译，’和‘变成&
#将&amp;删掉
#将输入的翻译先处理