import pandas as pd
from snownlp import SnowNLP
from snownlp import sentiment
import matplotlib.pyplot as plt
from numpy import *

df = pd.read_csv('./tool_spider/mooc_comment.csv', header=None, usecols=[0])
contents = df.values.tolist()
score = []
for content in contents:
    try:
        s = SnowNLP(content[0])
        score.append(s.sentiments)

    except:
        print('Wrong!')
        score.append(0.5)
average = mean(score)