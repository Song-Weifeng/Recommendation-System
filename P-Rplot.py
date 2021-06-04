from flask import Flask, jsonify, make_response
from flask import request
import pymongo
import pandas as pd
import findspark
from pyspark.sql import functions as F
from pyspark.sql import types as T
from pyspark.ml.feature import Word2Vec
import numpy as np
import json
from scipy.spatial import distance
import spacy
import heapq
import os
#
# findspark.init()
# from pyspark.sql import SparkSession

# 连接数据库
client = pymongo.MongoClient(host='123.57.239.180', port=27017, tz_aware=True)
# spark = SparkSession \
#     .builder \
#     .appName("PySpark flask") \
#     .getOrCreate()
# sc = spark.sparkContext
df = pd.read_csv("JS_exercise_embedding.csv")
df["word2vec"] = df["word2vec"].map(lambda x: np.array(json.loads(x)))
# print(df.head(20))
# word2vec_json = request.get_json()
# title_id = int(word2vec_json.get('title_id'))
title_id = 1
item_embedding = df.loc[df["id"] == title_id, "word2vec"].iloc[0]
# df["sim_value"] = df["word2vec"].map(lambda x: 1 - distance.cosine(item_embedding, x))
df["sim_value"] = df["word2vec"].map(lambda x: np.corrcoef(np.vstack([item_embedding, x]))[0][1])
recommend = df.sort_values(by="sim_value", ascending=False)
# print(df.sort_values(by="sim_value", ascending=False).head(10))
cols_list = client['JS_exercise'].list_collection_names()
fe = []
recommend.to_csv("PR2.csv")
# print(recommend.head(100))
for index in list(recommend['id']):
    for name in cols_list:
        info = client['JS_exercise'][name].find_one({'id': index})
        if info:
            fe.append(info)
            break
print(fe)
