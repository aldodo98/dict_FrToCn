import csv

list1 = [['流苏', ['and', 'franges']], ['格纹', []], ['嵌花', ['intarsia', 'à', 'carreaux']], ['羊绒', ['en', 'cachemire']], ['围巾', ['Écharpe']]]

print(len(list1[1][1]))
for i in range(len(list1)):
    if len(list1)-i<2:break
    list1[i][1] = list1[i][1][len(list1[i+1][1]):]
    try:
        list1[i][1].remove('and')
    except Exception:
        pass

print(list1)
with open ("test.csv", "w", encoding='utf-8-sig') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["word_fr", "word_cn"])
    for each in list1:
        list2 = []
        list2.append(each[1])
        list2.append(each[0])

        writer.writerow(list2)
