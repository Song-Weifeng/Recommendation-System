import heapq
import pymongo
import spacy
import pandas as pd

nlp_zh = spacy.load("zh_core_web_md")
nlp_en = spacy.load('en_core_web_md')
client = pymongo.MongoClient(host='123.57.239.180', port=27017, tz_aware=True)
data = pd.read_csv('Course1.csv')
data_list = data['video_title'].values.tolist()
# print(data_list)
search_Course_similarity = []
for item in data_list:
    doc1 = nlp_zh(search_Course)
    doc2 = nlp_zh(item)
    search_Course_similarity.append(doc2.similarity(doc1))
print(heapq.nlargest(10, search_Course_similarity))
max_number = heapq.nlargest(3, search_Course_similarity)
max_index = []
for item in max_number:
    index = search_Course_similarity.index(item)
    max_index.append(index)
    search_Course_similarity[index] = 0
top_n = max_index
cols_list = client['Course'].list_collection_names()
fe = []
for index in top_n:
    for name in cols_list:
        info = client['Course'][name].find_one({'id': index})
        if info:
            fe.append(info)
