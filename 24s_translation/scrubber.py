import json
import jieba
import difflib
from googletrans import Translator
import synonyms
import csv
import re

def translate(data):
    data = ''.join(data)
    translator = Translator()
    trans_data = translator.translate(data, src='fr', dest='zh-cn')
    return trans_data.text

def nettoyer(str1,str2):
    resultat1 = jieba.lcut(str1)
    resultat2 = jieba.lcut(str2)
    resultat = []
    resultat_cn = []
    resultat_fr = []
    for each in resultat2:
        ajouter = True
        for i in resultat1:
            if each.lower() == i.lower():
                ajouter = False
                break
        if ajouter:
            resultat_cn.append(each)
    combinaison1 = False
    combinaison2 = False
    for each in resultat_cn:
        if each == "人造皮":
            combinaison1 = True
        if combinaison1:
            if each == "草":
                resultat_cn.remove("人造皮")
                resultat_cn.remove("草")
                resultat_cn.append(("人造皮草"))

    for each in resultat1:
        ajouter = True
        for i in resultat2:
            if each.lower() == i.lower():
                ajouter = False
                break
        if ajouter:
            resultat_fr.append(each)
    resultat.append(''.join(resultat_fr).split(' '))
    resultat.append(resultat_cn)
    return resultat

def regroup_word_by_len(list):
    for each in list:
        if each[1][-1] == 'en' or each[1][-1] == 'à' or each[1][-1] == 'avec':
            each[1].remove(each[1][-1])

    list.sort(key = lambda i:len(i[1]),reverse= True)
    try:
        for each in list[-1][1]:
            if each == 'en':
                new_date=[]
                new_date.append(list[-1][1][0])
                list[-1][1] = new_date
                break
        for i in range(len(list)):
            if len(list) - i < 2: break
            list[i][1] = list[i][1][len(list[i + 1][1]):]
            try:
                list[i][1].remove('and')
            except Exception:
                pass
        return list
    except Exception as err:
        pass

list_docs = ['enfant-f_accesoires.json','enfant-f_chaussures.json','enfant-f_offre.json','enfant-f_vetements.json','enfant-g_accesoirs.json','enfant-g_chaussures.json','enfant-g_offre.json','enfant-g_vetements.json','femme_accesoires.json','femme_beaute.json','femme_bijoux.json','femme_chaussures.json','femme_offre.json','femme_sac.json','femme_vetements.json','homme_accesoires.json','homme_beaute.json','homme_chaussures.json','homme_offre.json','homme_sac.json','homme_sport.json','homme_vetements.json','maison_arts.json','maison_deco.json','maison_linge.json','maison_luminaires.json','maison_mobilier.json','maison_offre.json']

for data_original in list_docs:
    # file_path = 'D:\\dict_FrToCn\\24s_translation\\items_collection\\items_collection\\' + data_original
    file_path = '/root/dict_FrToCn/24s_translation/items_collection/items_collection/' + data_original
    with open(file_path,encoding='utf-8') as data_site:
        data = json.load(data_site)
        data1 = []
        for each in data:
            col = []
            col.append(each['name_fr'])
            col.append(each['name_zh'])
            data1.append(col)

    for i in range(len(data1)):
        resultat_nettoye = nettoyer(data1[i][0], data1[i][1])

        list_binome = []
        for each in resultat_nettoye[1]: #将中文原文中的每一个词取出来
            max_ratio = 0
            synonym_ratio = 0
            meilleur_trans = ''
            length = len(resultat_nettoye[0])
            binome = []

            for i in range(length):
                n = length-i
                google_trans = translate(resultat_nettoye[0][:n])
                radio = difflib.SequenceMatcher(None, each, google_trans).ratio()

                if radio >= max_ratio :
                    r = synonyms.compare(each, google_trans, seg=True)
                    if r >= synonym_ratio:
                        synonym_ratio = r
                        meilleur_trans = each
                        original_fr = resultat_nettoye[0][:n]
                        max_ratio = radio
            if max_ratio >= 0.0:
                binome.append(meilleur_trans)
                binome.append(original_fr)
                list_binome.append(binome)

        list1 = regroup_word_by_len(list_binome)
        print(list1)
        file_name = '/root/dict_FrToCn/24s_translation/items_collection/dict_' + data_original.split('.')[0] + '.csv'
        try:

            with open (file_name, "a", encoding='utf-8-sig') as csvfile:
                writer = csv.writer(csvfile)
                for each in list1:
                    list2 = []
                    list2.append(each[1])
                    list2.append(each[0])
                    writer.writerow(list2)
        except Exception as err:
            with open (file_name, "w", encoding='utf-8-sig') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["word_fr", "word_cn"])
                for each in list1:
                    list2 = []
                    list2.append(each[1])
                    list2.append(each[0])
                    writer.writerow(list2)
