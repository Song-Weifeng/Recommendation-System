import pymongo

# 连接数据库
client = pymongo.MongoClient(host='123.57.239.180', port=27017, tz_aware=True)

# 选择数据库
var_db = 'JS_exercise'
db = client[var_db]
# 切换库和集合
var_col = 'array'
col = client[var_db][var_col]
s = col.find_one({'id': 222})
print(s)
# print('====================================================================================')
# for item in list(col.find()):
#     print(item)
#     print('---------------------------------------------')
