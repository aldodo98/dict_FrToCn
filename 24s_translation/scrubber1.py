import json
import thulac
import re
import jieba
import difflib
from googletrans import Translator
from snownlp import SnowNLP
# from nltk import NLTKWordTokenizer
# import nltk
import synonyms

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
    # min_len = 99
    # new_list = []
    # for i in range(len(list)):
    #     for each in list:
    #         if len(each[1])<min_len:
    #             min_len = len(each[1])
    #             element = each[1]
    #     new_list.append(list.remove(element))

    for each in list:
        if each[1][-1] == 'en' or each[1][-1] == 'à' or each[1][-1] == 'avec':
            each[1].remove(each[1][-1])

    list.sort(key = lambda i: len(i[1]), reverse=True)
    for each in list[-1][1]: #最短的字符不能以介词结尾
        if each == 'en' or each == 'à' or each == 'avec':
            new_date=[]
            new_date.append(list[-1][1][0])
            list[-1][1] = new_date
            break
    # print(list)
    for i in range(len(list)):
        if len(list) - i < 2: break
        list[i][1] = list[i][1][len(list[i + 1][1]):]
        try:
            list[i][1].remove('and')
        except Exception:
            pass
    return list

with open('D:\scrapyProcesussscrapy\\24s_translation\items_collection\items_collection\enfant-f_accesoires.json',encoding='utf-8') as enfant_f_accesoires:
    data = json.load(enfant_f_accesoires)
    data1 = []
    for each in data:
        col = []
        col.append(each['name_fr'])
        col.append(each['name_zh'])
        data1.append(col)


    resultat_nettoye = nettoyer(data1[8][0], data1[8][1])

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
        # radio = synonyms.compare(each, google_trans, seg=True)
        # print('{0:1f} {1:2s} {2:3s}'.format(radio,each, google_trans))

        if radio >= max_ratio :
            r = synonyms.compare(each, google_trans, seg=True)
            if r >= synonym_ratio:
                synonym_ratio = r
                meilleur_trans = each
                original_fr = resultat_nettoye[0][:n]
                max_ratio = radio
    if max_ratio >= 0:
            binome.append(meilleur_trans)
            binome.append(original_fr)
            list_binome.append(binome)

print(regroup_word_by_len(list_binome))



