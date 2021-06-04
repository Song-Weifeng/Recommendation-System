import pandas as pd
import findspark
from pyspark.sql import functions as F
from pyspark.sql import types as T
from pyspark.ml.feature import Word2Vec
import numpy as np
import json
from scipy.spatial import distance
# from scipy.spatial.distance import pdist

findspark.init()
from pyspark.sql import SparkSession

# df = pd.read_csv("comment_level.csv")
# df_group = df.groupby(['item_titles'])['item_html'].apply(lambda x: ' '.join([str(m) for m in x])).reset_index()
# df_group.to_csv("./ml-latest-small/code_title-html.csv", index=False)

spark = SparkSession \
    .builder \
    .appName("PySpark word2Vec") \
    .getOrCreate()
sc = spark.sparkContext

df = spark.read.csv("../ml-latest-small/code_title-html.csv", header=True)
df = df.withColumn('words_title', F.split(df.exercise_title, ' '))
df.show(20)
word2Vec = Word2Vec(
    vectorSize=5,
    minCount=0,
    inputCol='words_title',
    outputCol='word2Vec')
model = word2Vec.fit(df)

# 得到整个doc的word embedding
df_word2Vec = model.transform(df)
df_word2Vec.printSchema()

df_word2Vec.select("word2Vec").show(3, truncate=False)
df_word2Vec.select("id", "exercise_title", "word2Vec") \
    .toPandas() \
    .to_csv('E:/React学习/cn42/61-Guided-Practice/src/ml-latest-small/code_html_embedding.csv', index=False)
df = pd.read_csv("E:/React学习/cn42/61-Guided-Practice/src/ml-latest-small/code_html_embedding.csv")

df["word2Vec"] = df["word2Vec"].map(lambda x: np.array(json.loads(x)))
item_html_id = 1
item_html_embedding = df.loc[df["id"] == item_html_id, "word2Vec"].iloc[0]

# df["sim_value"] = df["code2vec"].map(lambda x: 1 - distance.cosine(item_html_embedding, x))
# cos相似度
# df["sim_value"] = df["code2vec"].map(lambda x: 1 - distance.pdist(np.vstack([x, item_html_embedding]), 'cosine'))
# pearson相似度
df["sim_value"] = df["word2Vec"].map(lambda x: np.corrcoef(np.vstack([item_html_embedding, x]))[0][1])
print('根据Pearson相似度计算：')
print('与id为1的题目最相似的十道题id为：')
for id in list(df.sort_values(by="sim_value", ascending=False).head(10)['id']):
    print(id)

