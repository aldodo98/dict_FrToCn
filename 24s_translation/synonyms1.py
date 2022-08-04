import json

list_docs = ['enfant-f_accesoires.json', 'enfant-f_chaussures.json', 'enfant-f_offre.json', 'enfant-f_vetements.json',
             'enfant-g_accesoirs.json', 'enfant-g_chaussures.json', 'enfant-g_offre.json', 'enfant-g_vetements.json',
             'femme_accesoires.json', 'femme_beaute.json', 'femme_bijoux.json', 'femme_chaussures.json',
             'femme_offre.json', 'femme_sac.json', 'femme_vetements.json', 'homme_accesoires.json', 'homme_beaute.json',
             'homme_chaussures.json', 'homme_offre.json', 'homme_sac.json', 'homme_sport.json', 'homme_vetements.json',
             'maison_arts.json', 'maison_deco.json', 'maison_linge.json', 'maison_luminaires.json',
             'maison_mobilier.json', 'maison_offre.json']
for each in list_docs:
    file_path = 'D:\\dict_FrToCn\\24s_translation\\items_collection\\items_collection\\' + each
    with open(file_path, encoding='utf-8') as data_site:
        data = json.load(data_site)
        print(data[0])
