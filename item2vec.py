import pandas as pd
import findspark
from pyspark.sql import functions as F
from pyspark.sql import types as T
from pyspark.ml.feature import Word2Vec
import numpy as np
import json
from scipy.spatial import distance

findspark.init()
from pyspark.sql import SparkSession

spark = SparkSession \
    .builder \
    .appName("PySpark Item2vec") \
    .getOrCreate()
sc = spark.sparkContext

df = pd.read_csv("../ml-latest-small/ratings.csv")

df["rating"].mean()
df = df[df["rating"] > df["rating"].mean()].copy()
df_group = df.groupby(['userId'])['movieId'].apply(lambda x: ' '.join([str(m) for m in x])).reset_index()
df_group.to_csv("./ml-latest-small/uid_mids.csv", index=False)

df = spark.read.csv("./ml-latest-small/uid_mids.csv", header=True)
df = df.withColumn('movie_ids', F.split(df.movieId, ' '))
df.show(5)

Word2Vec = Word2Vec(
    vectorSize=5,
    minCount=0,
    inputCol='movie_ids',
    outputCol='movie_2vec')

model = Word2Vec.fit(df)
model.getVectors().show(3, truncate=False)
model.getVectors().select("word", "vector") \
    .toPandas() \
    .to_csv("./ml-latest-small/movies_embedding.csv", index=False)
df_embedding = pd.read_csv('../ml-latest-small/movies_embedding.csv')
df_movie = pd.read_csv('../ml-latest-small/movies.csv')
df_merge = pd.merge(
    left=df_embedding,
    right=df_movie,
    left_on="word",
    right_on="movieId"
)
df_merge['vector'] = df_merge['vector'].map(lambda x: np.array(json.loads(x)))
movie_id = 4018
movie_embedding = df_merge.loc[df_merge["movieId"] == movie_id, "vector"].iloc[0]

df_merge["sim_value"] = df_merge["vector"].map(lambda x: 1 - distance.cosine(movie_embedding, x))
df_merge[['movieId', 'title', 'genres', 'sim_value']].head(3)
# 按照相似度查询前十条
df_merge.sort_values(by="sim_value", ascending=False)[['movieId', 'title', 'genres', 'sim_value']].head(10)
print(df_merge.sort_values(by="sim_value", ascending=False)[['movieId', 'title', 'genres', 'sim_value']].head(10))
