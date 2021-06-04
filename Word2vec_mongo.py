import pymongo
import pandas as pd
import findspark
from pyspark.sql import functions as F
from pyspark.sql import types as T
from pyspark.ml.feature import Word2Vec
import numpy as np
import json
from flask import request
from scipy.spatial import distance
import spacy
import heapq

nlp_zh = spacy.load("zh_core_web_md")
nlp_en = spacy.load('en_core_web_md')

# 连接数据库
client = pymongo.MongoClient(host='123.57.239.180', port=27017, tz_aware=True)
user_id = '2'
data = pd.read_csv('Course1.csv')
data_list = data['video_title'].values.tolist()
course_score = data['score'].values.tolist()
course_id = data['id'].values.tolist()
x = client['User']['user_info'].find_one({"id": user_id})
search_Course_similarity = []
for item in data_list:
    doc1 = nlp_zh(x['tag'])
    doc2 = nlp_zh(item)
    search_Course_similarity.append(doc2.similarity(doc1))
print(search_Course_similarity)
max_number = heapq.nlargest(8, search_Course_similarity)
max_index = []
print(search_Course_similarity)
test1 = search_Course_similarity.copy()
for item in max_number:
    index = search_Course_similarity.index(item)
    max_index.append(index)
    search_Course_similarity[index] = 0
top_n = max_index
print(max_index)
for i in max_index:
    print(test1[i])
for i in max_index:
    print(str(data_list[i]) + ',' + str(test1[i]) + ',' + str(course_score[i]))
