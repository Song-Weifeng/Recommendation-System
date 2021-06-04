import pymongo
import pandas as pd

# 连接数据库
client = pymongo.MongoClient(host='123.57.239.180', port=27017, tz_aware=True)

# 将数据库中725道题目生成一个csv文件
# cols_exercise_list = client['JS_exercise'].list_collection_names()
#
# for col_name in cols_exercise_list:
#     if col_name != 'system.indexes':
#         data = pd.DataFrame(list(client['JS_exercise'][col_name].find()))
#         if col_name != 'array':
#             data.to_csv("../tool_flask/js1.csv", index=False, header=False, mode='a+')
#         else:
#             data.to_csv("../tool_flask/js1.csv", index=False, mode='a+')

col = client['All']['all_exercise']
df = pd.read_csv("../tool_flask/js1.csv")
data = pd.DataFrame(df)
print(data)
for i in data:
    for x in data[i]:
        col.insert()

