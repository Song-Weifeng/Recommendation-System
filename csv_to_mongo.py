import pymongo
import pandas as pd

# 连接数据库
client = pymongo.MongoClient(host='123.57.239.180', port=27017, tz_aware=True)
col = client['Course']['Java']
df = pd.read_csv("../tool_flask/Course1.csv")
data = pd.DataFrame(df)